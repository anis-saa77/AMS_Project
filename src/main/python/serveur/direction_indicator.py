from langchain.tools import Tool
import re

from sql import *
from settings import DB_FILE_PATH

# Dictionnaire de corrections des erreurs courantes
CORRECTIONS = {
    "ça": "s1",
    "salsa": "salle s1",
    "c'est": "c",
    "c-": "c",
    "blése": "blaise",
    "blèse": "blaise",
    "stade": "stat",
    "States": "stat",
    "stats": "stat",
    "s2-bis": "s2bis",
    "s2_bis": "s2bis",

}

def apply_corrections(query):
    for incorrect, correct in CORRECTIONS.items():
        if incorrect in query:
            print(f"Correction : '{incorrect}' => '{correct}'")
            corrected_query = query.replace(incorrect, correct)
            return corrected_query
    return query
import json

def direction_indication(query):
    print("Query in tool_call : " + query)
    query = apply_corrections(query.lower())
    print("Query corrected : " + query)

    connection = sqlite3.connect(DB_FILE_PATH)
    cur = connection.cursor()

    if any(word in query.lower() for word in ["amphi", "amphithéâtre", "ada", "blaise"]):
        if "ada" in query.lower():
            direction_to_room = getRoomDirection(cur, "AMPHI ADA")
            connection.close()
            return json.dumps({"tool_response": str(direction_to_room), "entity": "AMPHI ADA"})
        if "blaise" in query.lower():
            direction_to_room = getRoomDirection(cur, "AMPHI BLAISE")
            connection.close()
            return json.dumps({"tool_response": str(direction_to_room), "entity": "AMPHI BLAISE"})
        return json.dumps({"tool_response": "Vers quel amphithéâtre souhaitez-vous être dirigé", "entity": None})

    if any(word in query.lower() for word in ["toilettes", "toilette", "wc"]):
        connection.close()
        return json.dumps({"tool_response": "Les toilettes les plus proches se trouvent dans le couloir d'en face, à votre gauche", "entity": "WC"})

    match = re.search(r'\bs2bis\b|\bs\d+\b|\bstat\d\b|\bstat \d+\b', query, re.IGNORECASE)
    if match:
        room = match.group().upper().replace(" ", "")
        if not roomExists(cur, room):
            return json.dumps({"tool_response": f"La salle '{room}' n'existe pas dans la base de données.", "entity": None})
        direction_to_room = getRoomDirection(cur, room)
        connection.close()
        return json.dumps({"tool_response": str(direction_to_room), "entity": room})

    match = re.search(r'\bc\d+\b', query, re.IGNORECASE)
    if match:
        room_number = match.group().upper()
        room = getRoomNameFromNumber(cur, room_number)
        if not roomExists(cur, room):
            connection.close()
            return json.dumps({"tool_response": f"La salle '{room_number}' n'existe pas dans la base de données.", "entity": None})
        direction_to_room = getRoomDirection(cur, room)
        connection.close()
        return json.dumps({"tool_response": str(direction_to_room), "entity": room})

    connection.close()
    return json.dumps({"tool_response": "La salle n'est pas dans ma base de données.", "entity": None})


# Création du Tool
direction_tool = Tool(
    name="direction_indication",
    func=direction_indication,
    #description="Donne la direction vers une salle spécifiée ou vers des salles 'States' ou vers la salle ça ou vers la salsa, ou vers les toilettes, ou vers l'amphithéâtre ou vers un les amphi blaise ou ada.",
    description="Donne la direction vers une salle spécifiée ou vers les toilettes, ou vers les amphithéâtres Blaise et Ada.",
    return_direct=True
)
