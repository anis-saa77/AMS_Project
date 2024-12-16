from state import State
from model import trimmer, messages, model
from tools import tools
from langchain_core.messages import HumanMessage
from langgraph.graph import START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

##############################################################
                        # Config #
##############################################################


####################################################
# Define the function that calls the model
####################################################

def call_model(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    response = agent_executor.invoke({"messages": trimmed_messages, "language": state["language"]})
    return {"messages": response["messages"]}


####################################################
# Define the function to send a message to the model
####################################################

def sendMessage(message, language, config):
    print("HumanMessage :", [HumanMessage(content=message)])
    state = {"messages": messages + [HumanMessage(content=message)], "language": language}
    output = app.invoke(state, config)
    response = output['messages'][-1]
    print(f"AI Message: {response.content}")
    print(f"ToolCalls: {response.tool_calls}")
    return response.content


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
agent_executor = create_react_agent(model, tools, checkpointer=memory)

app = workflow.compile(checkpointer=memory)

# Per user
config = {"configurable": {"thread_id": "abc123"}}


##############################################################