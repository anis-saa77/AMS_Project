import string
from langchain.tools import Tool
from sql import *


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def social_aid_suggestion(query):
    # Convertir la requête en minuscules
    query = query.lower()
    query = remove_punctuation(query)

    connection = sqlite3.connect("../../../resources/database/data.db")
    cur = connection.cursor()

    aids = getAids(cur)
    # TODO Améliorer la vérification de la correspondance
    # Vérifier si des mots-clés correspondent à des aides
    query_words = query.split()
    for aid in aids:
        aid_info = getAidInfo(cur, aid)
        aid_keywords = getAidKeywords(cur, aid)
        # TODO un certain seuil de mot-clés au lieu de 'any'
        if any(keyword in query_words for keyword in aid_keywords):
            connection.close()
            return f"Aide suggéré : {aid_info}", aid

    # Si aucune aide n'est trouvée
    connection.close()
    return "Désolé, je n'ai pas trouvé d'aide sociale correspondant à votre besoin.", None

social_aid_tool = Tool(
    name="social_aid",
    func=social_aid_suggestion,
    description="Suggère une aide sociale pour une personne en difficulté."
)
