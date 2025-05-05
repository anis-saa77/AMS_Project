import json
from langchain.tools import Tool
def conversation_func(query):
    tool_response = "Trés bien, démarrons une conversation ! Pour l'arreter dites moi : Arrêter la conversation."
    return json.dumps({"tool_response": tool_response, "entity": None})

conversation_tool = Tool(
    name="conversation_tool",
    func=conversation_func,
    description="Commence un conversation quand l'utilisateur demande ou souhaite commencer ou démarrer ou débuter une conversation.",
    return_direct=True
)