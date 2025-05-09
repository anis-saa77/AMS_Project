# pip install --upgrade langchain langchain-fireworks
import requests
import os
from dotenv import load_dotenv

racine = os.path.dirname(os.path.abspath(__file__))
env_path = "../../../resources/.env"
load_dotenv(os.path.join(racine, env_path))
langchain_api_key = os.getenv('LANGSMITH_API_KEY')
fireworks_api_key = os.getenv('FIREWORKS_API_KEY')
os.environ["LANGSMITH_TRACING"] = "true"
os.environ["LANGSMITH_API_KEY"] = langchain_api_key
os.environ["FIREWORKS_API_KEY"] = fireworks_api_key

url = "https://api.fireworks.ai/inference/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {fireworks_api_key}",
    "Content-Type": "application/json",
}
data = {
    "model": "accounts/fireworks/models/llama-v3p1-70b-instruct",
    "messages": [{"role": "user", "content": "Bonjour"}],
}

response = requests.post(url, headers=headers, json=data)
print(response.status_code)
print(response.json())