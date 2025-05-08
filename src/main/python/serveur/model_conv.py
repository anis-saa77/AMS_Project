import os
from dotenv import load_dotenv
from langchain_fireworks import ChatFireworks
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import SystemMessage, trim_messages


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
# Reinitialize messages
####################################################
def init_conversation():
    messages = [
        SystemMessage(content="you're a good assistant")
    ]


####################################################
# Define the model
####################################################

model = ChatFireworks(model="accounts/fireworks/models/llama-v3p1-70b-instruct")

prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are the robot of a chatbot. You must answer concisely and accurately. Always respond to the best of your ability in {language}.",
        ),
        MessagesPlaceholder(variable_name="messages"),
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