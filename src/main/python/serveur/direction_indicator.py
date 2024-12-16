import string
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class DirectionInput(BaseModel):
    query: str = Field(description="Description du besoin de l'utilisateur pour trouver son chemin.")


class DiretionIndicationTool(BaseTool):
    """Outil pour donner la direction vers une salle."""
    name: str = "Direction Indicator Tool"
    description: str = "Donne la direction en fonction du besoin de l'utilisateur."
    args_schema: Type[BaseModel] = DirectionInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Utilise l'outil pour suggérer donner la dierction vers une salle."""
        # Si aucune aide n'est trouvée
        return "L'outil utilisé est DirectionIndicatorInput"