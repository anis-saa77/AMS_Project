from state import State
from model import trimmer, messages, model, prompt
from tools import tools
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langchain.agents import create_tool_calling_agent
import json
from custom_agent_executor import AgentExecutorCustom
def call_model(state: State):
    # Trim des messages
    trimmed_messages = trimmer.invoke(state["messages"])
    # Appel de l'agent avec le prompt formaté
    response = agent_executor.invoke({"messages": trimmed_messages, "language": state["language"]})
    # Log des étapes intermédiaires
    intermediate_steps = response.get("intermediate_steps", [])
    #print("Intermediate Steps :", intermediate_steps)

    """ Baser le mode assistant sur usage exclusive des tools ?! (Mauvaise idée)"""
    #TODO Si l'agent n'a pas appelé de tool, demander un reformulation
    # if not intermediate_steps:
    #     updated_messages = state["messages"] + [
    #         AIMessage(content="Je ne peux répondre qu'en utilisant un outil. Peux-tu reformuler ta demande ?")]
    #     return {"messages": updated_messages, "tool_call": []}

    # Cas anormal : Le retour de l'agent est un json
    try:
        json_response = json.loads(response['output'])
        if json_response.get('tool_response'):  # Si un Json valide est envoyé
            tool_response = json_response.get('tool_response')
            updated_messages = state["messages"] + [AIMessage(content=tool_response)]
            return {"messages": updated_messages, "tool_call": intermediate_steps}

        else: # Si le Json n'est pas valide
            # TODO
            #   json_response = {"type": "function", "name": "direction_indication", "parameters": {"__arg1": "S3"}}
            #  Utiliser json_response pour réitérer l'appel
            print("Réponse au format json non attendu : ", json_response)
            updated_messages = state["messages"] + [AIMessage(content="Je n'ai pas compris ta demande. Peux-tu reformuler ?")]
            return {"messages": updated_messages, "tool_call": intermediate_steps}
    except json.JSONDecodeError:
        pass

    # Cas normal : Le retour de l'agent n'est pas un json
    updated_messages = state["messages"] + [AIMessage(content=response["output"])]
    return {"messages": updated_messages, "tool_call": intermediate_steps}

def sendMessage(message, language, config):
    state = {"messages": messages + [HumanMessage(content=message)], "language": language}
    output = app.invoke(state, config)
    response = output['messages'][-1]
    #print("AI_Message : ", response.content)
    ai_message = response.content
    tool_call = output.get('tool_call')
    if tool_call:
        tool_agent_action = tool_call[0]
        tool_name = tool_agent_action[0].tool
        #print("Tool Call : ", tool_name)
        tool_return = tool_agent_action[-1]
        #print("tool_return : ", tool_return)
        if isinstance(tool_return, tuple):
            entity = tool_return[1]
        elif isinstance(tool_return, str):
            tool_return = json.loads(tool_return)
            entity = tool_return.get('entity')
        return ai_message, tool_name, entity
    return ai_message, None, None


# Defininir le graphe
workflow = StateGraph(state_schema=State)

workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Ajout de la mémoire
memory = MemorySaver()

# Création de l'agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutorCustom(agent=agent, tools=tools, return_intermediate_steps=True, verbose=False)  # verbose= True

app = workflow.compile(checkpointer=memory)

# Config
config = {"configurable": {"thread_id": "abc123"}}