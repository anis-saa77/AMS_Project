import string
from typing import Optional, Type
from langchain_core.tools import BaseTool
from pydantic import Field, BaseModel
from langchain.tools import Tool
from langchain_core.messages import SystemMessage
from sql import *


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def social_aid_suggestion(query):
    # Convertir la requête en minuscules
    query = query.lower()
    query = remove_punctuation(query)

    aids = getAids()
    # TODO Améliorer la vérification de la correspondance
    # Vérifier si des mots-clés correspondent à des aides
    query_words = query.split()
    for aid in aids:
        aid_info = getAidInfo(aid)
        aid_keywords = getAidKeywords(aid)
        # TODO un certain seuil de mot-clés au lieu de 'any'
        if any(keyword in query_words for keyword in aid_keywords):
            return f"Aide suggérée : {aid_info}"

    # Si aucune aide n'est trouvée
    return "Désolé, je n'ai pas trouvé d'aide sociale correspondant à votre besoin."

social_aid_tool = Tool(
    name="social_aid",
    func=social_aid_suggestion,
    description="Suggère une aide sociale pour une personne en difficulté."
)
