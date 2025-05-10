from state_conv import State
from conv_model import prompt, model, trimmer, messages

from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph


##############################################################
                        # Configuration #
##############################################################



####################################################
# Define the function that calls the model
####################################################

def call_model(state: State):
    chain = prompt | model
    trimmed_messages = trimmer.invoke(state["messages"])
    response = chain.invoke(
        {"messages": trimmed_messages, "language": state["language"]}
    )
    return {"messages": [response]}


####################################################
# Define the function to send a message to the model
####################################################

def sendConvMessage(message, language, config):
    input_messages = messages + [HumanMessage(message)]
    
    output = app.invoke({"messages": input_messages, "language": language}, config)
    output["messages"][-1].pretty_print()  # output contains all messages in state
    return output["messages"][-1].content


####################################################
# Define some variables
####################################################

# Define a new graph
workflow = StateGraph(state_schema=State)

# Define the (single) node in the graph
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Add memory
memory = MemorySaver()
app = workflow.compile(checkpointer=memory)

# per user
configConv = {"configurable": {"thread_id": "abc123"}}

####################################################