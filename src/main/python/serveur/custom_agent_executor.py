from langchain.agents import AgentExecutor
from langchain_core.messages import HumanMessage, AIMessage
import json

class AgentExecutorCustom(AgentExecutor):
    def __init__(self, agent, tools, return_intermediate_steps=True, verbose=False):
        super().__init__(agent=agent, tools=tools, return_intermediate_steps=return_intermediate_steps, verbose=verbose)

    def invoke(self, inputs):
        # On récupère directement le dernier message complet (sans le tronquer)
        human_message = next((msg for msg in inputs["messages"] if isinstance(msg, HumanMessage)), None)
        if human_message is None:
            raise ValueError("No HumanMessage found in the input messages.")

        # Ajouter tout le message de l'utilisateur dans les arguments des tools
        for tool in self.tools:
            tool.args["messages"] = inputs["messages"]

        # On appelle ensuite le modèle de manière classique
        response = super().invoke(inputs)
        return response