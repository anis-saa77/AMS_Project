from langchain.tools import Tool
def conversation_func(query):
    return "Trés bien, démarrons une conversation ! Pour l'arreter dites moi : stop."

conversation_tool = Tool(
    name="conversation_tool",
    func=conversation_func,
    description="Commence un conversation quand l'utilisateur demande ou souhaite commencer ou démarrer ou débuter une conversation.",
    return_direct=True
)