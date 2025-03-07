from langchain.tools import Tool
from sql import *
import re

# Dictionnaire de corrections des erreurs courantes
CORRECTIONS = {
    "ça": "S1",
    "salsa": "salle S1",
    "c'est": "C",
    "blése":"blaise",
    "blèse":"blaise",

}
def apply_corrections(query):
    for incorrect, correct in CORRECTIONS.items():
        if incorrect in query:
            print(f"Correction : '{incorrect}' => '{correct}'")
            corrected_query = query.replace(incorrect, correct)
            return corrected_query
    return query
def direction_indication(query):
    print(query)
    query = apply_corrections(query.lower())

    connection = sqlite3.connect("../../../resources/database/data.db")
    cur = connection.cursor()

    if any(word in query.lower() for word in ["amphi", "amphithéâtre"]):
        if "ada" in query.lower():
            direction_to_room = getRoomDirection(cur, "AMPHI ADA")
            connection.close()
            return str(direction_to_room), "AMPHI ADA"
        if "blaise" in query.lower():
            direction_to_room = getRoomDirection(cur, "AMPHI BLAISE")
            connection.close()
            return str(direction_to_room), "AMPHI BLAISE"
        return "Vers quel amphithéâtre souhaitez-vous être dirigé", None

    if any(word in query.lower() for word in ["toilettes", "toilette", "wc"]):
        connection.close()
        return "Les toilettes les plus proches se trouve dans le couloir d'en face, à votre gauche", "WC"

    match = re.search(r'\bs\d+\b|\bstat\d+\b', query, re.IGNORECASE)
    if match:
        room = match.group().upper()
        if not roomExists(cur, room):
            return f"La salle '{room}' n'existe pas dans la base de données.", None
        direction_to_room = getRoomDirection(cur, room)
        connection.close()
        return str(direction_to_room), room
    match = re.search(r'\bc\d+\b', query, re.IGNORECASE)
    if match:
        room_number = match.group().upper()
        room = getRoomNameFromNumber(cur, room_number)
        if not roomExists(cur, room):
            connection.close()
            return f"La salle '{room_number}' n'existe pas dans la base de données.", None
        direction_to_room = getRoomDirection(cur, room)
        connection.close()
        return str(direction_to_room), room

    # Si aucune salle n'est trouvée
    connection.close()
    return "La salle n'est pas dans ma base de données.", None

# Création du Tool
direction_tool = Tool(
    name="direction_indication",
    func=direction_indication,
    description="Donne la direction vers une salle spécifiée ou vers la salle ça ou vers la salsa, ou vers les toilettes, ou vers un amphithéâtre ou vers un amphi."
)
