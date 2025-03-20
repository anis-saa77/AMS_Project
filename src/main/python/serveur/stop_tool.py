import json
from langchain.tools import Tool

def stop_func(query):
    return json.dumps({"tool_response": "STOP", "entity": None})

stop_tool = Tool(
    name="stop_tool",
    func=stop_func,
    description="L'utilisateur utilisateur souhaite arrêter la conversation, ou arrêter la discution, si l'utilisateur souhaîte partir, si l'utilisateur veux partir, si l'utilisateur dit qu'il s'en va, ou si l'utilisateur dit : 'aurevoir'.",
    return_direct=True
)