import string
from langchain.tools import Tool


def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def social_aid_suggestion(query: str) -> str:
    # Dictionnaire d'aides sociales avec mots-clés
    aids = {
        "CAF": {
            "description": "Caisse d'Allocations Familiales : aide pour les familles, logement, etc.",
            "keywords": ["famille", "enfant", "logement", "aide logement", "allocations familiales", "CAF"]
        },
        "RSA": {
            "description": "Revenu de Solidarité Active : aide financière pour les personnes sans revenus suffisants.",
            "keywords": ["revenu", "RSA", "sans emploi", "chômage", "sans revenus", "insertion"]
        },
        "ASPA": {
            "description": "Allocation de Solidarité aux Personnes Âgées : aide pour les retraités ayant de faibles revenus.",
            "keywords": ["retraite", "retraité", "retraitée", "personne âgée", "personne retraitée", "ASPA", "seniors", "aide financière"]
        },
        "APL": {
            "description": "Aide Personnalisée au Logement : aide au logement pour les personnes ayant de faibles ressources.",
            "keywords": ["logement", "APL", "aide logement", "loyer", "habitat"]
        },
    }

    # Convertir la requête en minuscules
    query = query.lower()
    query = remove_punctuation(query)

    # TODO Améliorer la vérification de la correspondance
    # Vérifier si des mots-clés correspondent à des aides
    for aid_name, aid_info in aids.items():
        query_words = query.split()
        if any(keyword in query_words for keyword in aid_info["keywords"]):
            return f"Aide suggérée : {aid_name} - {aid_info['description']}"
    # Si aucune aide n'est trouvée
    return "Désolé, je n'ai pas trouvé d'aide sociale correspondant à votre besoin."


social_aid_tool = Tool(
    name="social_aid",
    func=social_aid_suggestion,
    description="Suggère une aide sociale pour une personne en fonction de la situation."
)
