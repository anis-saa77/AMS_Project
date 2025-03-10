from langchain.tools import Tool
def stop_func(query):
    return "STOP"

stop_tool = Tool(
    name="stop",
    func=stop_func,
    description="Dit : 'STOP', quand l'utilisateur souhaite arrêter la conversation, ou arrêter la discution, si l'utilisateur souhaîte partir, si l'utilisateur veux partir, si l'utilisateur dit qu'il s'en va, ou si l'utilisateur dit : 'aurevoir'."
)