import os
from langchain_fireworks import ChatFireworks
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, StateGraph
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from typing import Sequence
from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage
from langchain_core.messages import trim_messages
import speech_recognition as sr
from langchain_community.tools.tavily_search import TavilySearchResults
from langgraph.prebuilt import create_react_agent
from typing_extensions import Annotated, TypedDict
from langgraph.graph.message import add_messages

# Configuration des clés d'API
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = "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"
os.environ["FIREWORKS_API_KEY"] = "fw_3Zdp27tVsoJ5B13uME2UDCWw"
os.environ["TAVILY_API_KEY"] = "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"

# Modèle
model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")

# Outils
search = TavilySearchResults(max_results=2)
tools = [search]

# Mémoire
memory = MemorySaver()

# Configuration de l'agent
agent_executor = create_react_agent(model, tools, checkpointer=memory)
config = {"configurable": {"thread_id": "abc123"}}

# Définition du prompt
prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are an assistive AI for students in the CERI reception hall. Use the available tools to provide answers, especially for real-time information like the weather. Answer all questions to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
    ]
)

# Fonction de troncature
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

# Messages initiaux
messages = [
    SystemMessage(content="you're a good assistant")
]

# Définition de l'état
class State(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    language: str

# Fonction pour appeler le modèle
def call_model(state: State):
    trimmed_messages = trimmer.invoke(state["messages"])
    response = agent_executor.invoke({"messages": trimmed_messages, "language": state["language"]})
    return {"messages": response["messages"]}

# Création du graphique d'état
workflow = StateGraph(state_schema=State)
workflow.add_edge(START, "model")
workflow.add_node("model", call_model)

# Compilation avec mémoire
app = workflow.compile(checkpointer=memory)

# Fonction pour envoyer un message au modèle
def sendMessage(message, language, config):
    state = {"messages": messages + [HumanMessage(content=message)], "language": language}
    output = app.invoke(state, config)
    response = output['messages'][-1]
    print(f"AI Message: {response.content}")

# Exécution
while True:
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Parle maintenant...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    message = None
    try:
        message = recognizer.recognize_google(audio, language="fr-FR")
        print("Human message: " + message)
    except sr.UnknownValueError:
        print("Je n'ai pas pu comprendre ce qui a été dit.")
    except sr.RequestError:
        print("Erreur avec le service de reconnaissance vocale.")

    if message:
        sendMessage(message, "French", config)
