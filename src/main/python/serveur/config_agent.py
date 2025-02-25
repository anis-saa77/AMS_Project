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
    try:
        json.loads(response['output'])
        print("La réponse est au format json")
        updated_messages = state["messages"] + [AIMessage(content="Je n'ai pas compris votre demande. Veuillez répéter.")]
        return {"messages": updated_messages, "tool_call": intermediate_steps}
    except json.JSONDecodeError:
        pass
    #print(response)
    updated_messages = state["messages"] + [AIMessage(content=response["output"])]
    return {"messages": updated_messages, "tool_call":intermediate_steps}


####################################################
# Define the function to send a message to the model
####################################################

def sendMessage(message, language, config):
    state = {"messages": messages + [HumanMessage(content=message)], "language": language}
    #print("Message envoyé : ", state)
    output = app.invoke(state, config)
    response = output['messages'][-1]
    print("AI_Message : ", response.content)
    ai_message = response.content
    # A tester
    tool_call = output.get('tool_call')
    if tool_call : # Supprimer le dernier AIMessage et HumanMessagex
        #print(output)
        tool_agent_action = tool_call[0]
        tool_name = tool_agent_action[0].tool
        #print(f"Fonction appelée : {tool_name}")
        #print(tool_agent_action[-1])
        result = tool_agent_action[-1][1]
        #print("result : ", result)
        return ai_message, tool_name, result
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