import string
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
from sql import getAids, getAidKeywords, getAidInfo
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)
class SocialAidInput(BaseModel):
    query: str = Field(description="Description du besoin de l'utilisateur pour l'aide sociale.")

class SocialAidTool(BaseTool):
    """Outil suggérant des aides sociales."""
    name: str = "Social Aid Tool"
    description: str = "Suggère l'aide sociales appropriée."
    args_schema: Type[BaseModel] = SocialAidInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Utilise l'outil pour suggérer une aide sociale."""

        # Convertir la requête en minuscules
        query = query.lower()
        query = remove_punctuation(query)

        aids = getAids()
        #TODO Améliorer la vérification de la correspondance
        # Vérifier si des mots-clés correspondent à des aides
        query_words = query.split()
        for aid in aids :
            aid_info = getAidInfo(aid)
            aid_keywords = getAidKeywords(aid)
            #TODO un certain seuil de mot-clés au lieu de 'any'
            if any(keyword in query_words for keyword in aid_keywords):
                return f"Aide suggérée : {aid_info}"
        # Si aucune aide n'est trouvée
        return "Désolé, je n'ai pas trouvé d'aide sociale correspondant à votre besoin."

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Utilise l'outil de manière asynchrone."""
        raise NotImplementedError("SocialAidTool ne supporte pas l'asynchrone.")