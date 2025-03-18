from state import State
from model import trimmer, messages, model, prompt
from tools import tools
from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent
from langchain.agents import AgentExecutor, create_tool_calling_agent
import json
from langchain_core.messages import RemoveMessage

##############################################################
# Config #
##############################################################


####################################################
# Define the function that calls the model
####################################################
# Ajouter le prompt dans les messages
# final_prompt = prompt.format_messages(messages=trimmed_messages)
# response = agent_executor.invoke({"messages": final_prompt, "language": state["language"]})
def call_model(state: State):
    # Trim des messages
    trimmed_messages = trimmer.invoke(state["messages"])
    # Appel de l'agent avec le prompt formaté
    response = agent_executor.invoke({"messages": trimmed_messages, "language": state["language"]})
    # Log des étapes intermédiaires
    intermediate_steps = response.get("intermediate_steps", [])
    # print("Tool Call :", intermediate_steps)

    """ Baser le mode assisatant sur usage exclusive des tools ???????????? """
    #TODO Si l'agent n'a pas appelé de tool, lui dire de reformuler
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
            print("Réponse au format json non attendu : ", json_response)
            updated_messages = state["messages"] + [AIMessage(content="Je n'ai pas compris ta demande. Peux-tu reformuler ?")]
            return {"messages": updated_messages, "tool_call": intermediate_steps}
    except json.JSONDecodeError:
        pass

    # Cas normal : Le retour de l'agent n'est pas un json
    updated_messages = state["messages"] + [AIMessage(content=response["output"])]
    return {"messages": updated_messages, "tool_call": intermediate_steps}


####################################################
# Define the function to send a message to the model
####################################################

def sendMessage(message, language, config):
    state = {"messages": messages + [HumanMessage(content=message)], "language": language}
    output = app.invoke(state, config)
    response = output['messages'][-1]
    print("AI_Message : ", response.content)
    ai_message = response.content
    tool_call = output.get('tool_call')
    if tool_call:
        tool_agent_action = tool_call[0]
        tool_name = tool_agent_action[0].tool
        tool_return = tool_agent_action[-1]
        #print("tool_return : ", tool_return)
        if isinstance(tool_return, tuple):
            entity = tool_return[1]
        elif isinstance(tool_return, str):
            tool_return = json.loads(tool_return)
            entity = tool_return.get('entity')
        return ai_message, tool_name, entity
    return ai_message, None, None


####################################################
# Define some variables
####################################################
# Define the graph
workflow = StateGraph(state_schema=State)

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()

# Create the agent
agent = create_tool_calling_agent(model, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, return_intermediate_steps=True, verbose=False)  # verbose= True

app = workflow.compile(checkpointer=memory)

# Per user
config = {"configurable": {"thread_id": "abc123"}}

##############################################################
