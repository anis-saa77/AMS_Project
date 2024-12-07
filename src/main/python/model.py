import os
from functions import getLangchain_API_Key, getFireworks_API_Key, getTavily_API_Key
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import trim_messages, SystemMessage

##############################################################
                        # Model #
##############################################################

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = getLangchain_API_Key()
os.environ["FIREWORKS_API_KEY"] = getFireworks_API_Key()
os.environ["TAVILY_API_KEY"] = getTavily_API_Key()


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