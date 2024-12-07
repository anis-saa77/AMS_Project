from datetime import datetime
from langchain.tools import Tool
from model import messages
from langchain_core.messages import SystemMessage

def check_weather(location: str) -> str:
    """
    Obtiens la météo actuelle pour une ville donnée.
    
    Args:
        location (str): Le nom de la ville pour laquelle obtenir la météo.

    Returns:
        str: Une chaîne contenant la météo simulée.
    """
    messages = [
            SystemMessage(content="you're a good assistant")
    ]
    return f"La météo actuelle à {location} est ensoleillée avec une température de 22°C."

weather_tool = Tool(
        name="check_weather",
        func=check_weather,
        description="Obtiens la météo actuelle pour une ville donnée."  # Description ici
    )
