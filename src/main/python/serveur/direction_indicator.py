import string
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
import re

class DirectionInput(BaseModel):
    query: str = Field(description="Salle ou toilettes dont on veut connaître la direction.")

class DiretionIndicationTool(BaseTool):
    """Outil pour donner la direction vers une salle."""
    name: str = "Direction Indicator Tool"
    description: str = "Donne la direction en fonction de la salle voulue."
    args_schema: Type[BaseModel] = DirectionInput

    def _run(self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None) -> str:
        """Utilise l'outil pour donner la direction vers une salle."""
        if "toilettes" in query:
            return "Les toilettes se trouvent à gauche.", "toilettes"

        match = re.search(r'\bs\d+\b', query, re.IGNORECASE)
        if match:
            salle = match.group()
            return f"La salle {salle} se trouve au fond du couloir à gauche.", salle

        # Si aucune salle n'est trouvée
        return "Je ne trouve pas la salle demandée."