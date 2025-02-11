import string
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class DirectionInput(BaseModel):
    query: str = Field(description="Salle ou toilettes dont on veut connaître la direction.")

class DiretionIndicationTool(BaseTool):
    """Outil pour donner la direction vers une salle."""
    name: str = "Direction Indicator Tool"
    description: str = "Donne la direction en fonction de la salle voulue."
    args_schema: Type[BaseModel] = DirectionInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Utilise l'outil pour donner la dierction vers une salle."""
        if "toilettes" in query:
            return "Les toilettes se trouvent à gauche."
        # Si aucune aide n'est trouvée
        return "La salle se trouve au fond du couloir à gauche."