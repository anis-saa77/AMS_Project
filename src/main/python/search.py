import string
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)


class SearchInput(BaseModel):
    query: str = Field(description="Description du besoin de l'utilisateur pour effectuer une recherche.")


class SearchTool(BaseTool):
    """Outil pour effectuer une recherche en fonction de l'utilisateur."""
    name: str = "Search Tool"
    description: str = "Effectuer une recherche en fonction du besoin de l'utilisateur."
    args_schema: Type[BaseModel] = SearchInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Utilise l'outil pour suggérer effectuer une recherche et répondre au besoin de l'utilsateur."""
        # Si aucune aide n'est trouvée
        return "L'outil utilisé est SearchTool"