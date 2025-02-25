import os
from dotenv import load_dotenv
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages, SystemMessage

##############################################################
# Model #
##############################################################

racine = os.path.dirname(os.path.abspath(__file__))
env_path = "../../../resources/.env"
load_dotenv(os.path.join(racine, env_path))
langchain_api_key = os.getenv('LANGCHAIN_API_KEY')
fireworks_api_key = os.getenv('FIREWORKS_API_KEY')
tavily_api_key = os.getenv('TAVILY_API_KEY')

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = langchain_api_key
os.environ["FIREWORKS_API_KEY"] = fireworks_api_key
os.environ["TAVILY_API_KEY"] = tavily_api_key

####################################################
# Define the model
####################################################

model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            """
            Tu es un assistant intelligent pour le CERI. Utilise les outils disponibles pour répondre précisément aux questions. Voici les outils que tu peux utiliser :

            - **check_weather** : Obtiens la météo actuelle pour une ville donnée.
            - **social_aid** : Suggère une aide sociale pour répondre aux difficultés.

            Réponds toujours en français.
            """
        ),
        MessagesPlaceholder(variable_name="messages"),
        ("system", "Scratchpad pour l'agent: {agent_scratchpad}"),
    ]
)

trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)

messages = [
    SystemMessage(content="you're a good assistant")
]

####################################################