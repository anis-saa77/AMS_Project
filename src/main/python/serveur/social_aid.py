import string
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from langchain.callbacks.manager import (
    AsyncCallbackManagerForToolRun,
    CallbackManagerForToolRun,
)
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)
class SocialAidInput(BaseModel):
    query: str = Field(description="Description du besoin de l'utilisateur pour l'aide sociale.")

class SocialAidTool(BaseTool):
    """Outil pour suggérer des aides sociales et répondre au problème de l'utilisateur."""
    name: str = "Social Aid Tool"
    description: str = "Suggère l'aide sociales appropriée."
    args_schema: Type[BaseModel] = SocialAidInput

    def _run(
            self, query: str, run_manager: Optional[CallbackManagerForToolRun] = None
    ) -> str:
        """Utilise l'outil pour suggérer une aide sociale."""

        # Dictionnaire d'aides sociales avec mots-clés
        aids = {
            "CAF": {
                "description": "Caisse d'Allocations Familiales : aide pour les familles, logement, etc.",
                "keywords": ["famille", "enfant", "logement", "aide logement", "allocations familiales"]
            },
            "RSA": {
                "description": "Revenu de Solidarité Active : aide financière pour les personnes sans revenus suffisants.",
                "keywords": ["revenu", "RSA", "sans emploi", "chômage", "sans revenus", "insertion"]
            },
            "ASPA": {
                "description": "Allocation de Solidarité aux Personnes Âgées : aide pour les retraités ayant de faibles revenus.",
                "keywords": ["retraite", "retraité", "personne âgée", "ASPA", "seniors", "aide financière"]
            },
            "APL": {
                "description": "Aide Personnalisée au Logement : aide au logement pour les personnes ayant de faibles ressources.",
                "keywords": ["logement", "APL", "aide logement", "loyer", "habitat"]
            },
        }

        # Convertir la requête en minuscules
        query = query.lower()
        query = remove_punctuation(query)

        #TODO Améliorer la vérification de la correspondance
        # Vérifier si des mots-clés correspondent à des aides
        for aid_name, aid_info in aids.items():
            query_words = query.split()
            if any(keyword in query_words for keyword in aid_info["keywords"]):
                return f"Aide suggérée : {aid_name} - {aid_info['description']}"

        # Si aucune aide n'est trouvée
        return "Désolé, je n'ai pas trouvé d'aide sociale correspondant à votre besoin."

    async def _arun(
            self, query: str, run_manager: Optional[AsyncCallbackManagerForToolRun] = None
    ) -> str:
        """Utilise l'outil de manière asynchrone."""
        raise NotImplementedError("SocialAidTool ne supporte pas l'asynchrone.")