import string
import json
from langchain.tools import Tool

from sql import *
from settings import DB_FILE_PATH, AIDS_EMBEDDING
from sentence_transformers import SentenceTransformer, util
import torch

# Charger le modèle
model = SentenceTransformer('all-MiniLM-L6-v2')

def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)


def load_index(json_path=AIDS_EMBEDDING):
    aid_embeddings_index = {}
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    for aid, values in raw_data.items():
        desc = values["desc"]
        embedding_tensor = torch.tensor(values["embedding"])
        aid_embeddings_index[aid] = (desc, embedding_tensor)
    return aid_embeddings_index


def build_and_save_index(json_path=AIDS_EMBEDDING):
    connection = sqlite3.connect(DB_FILE_PATH)
    cur = connection.cursor()
    aids = getAids(cur)

    data = {}
    for aid in aids:
        desc = getAidDescription(cur, aid)
        desc_clean = desc.lower()
        embedding = model.encode(desc_clean, convert_to_numpy=True).tolist()
        data[aid] = {"desc": desc, "embedding": embedding}

    connection.close()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

aid_embeddings_index = load_index()
def best_aid_finder(query):
    # Nettoyage de la requête
    query_cleaned = query.lower()
    query_embedding = model.encode(query_cleaned, convert_to_tensor=True)

    best_similarity = 0
    best_aid = None
    best_aid_info = ""

    for aid, (desc, emb) in aid_embeddings_index.items():
        similarity = util.cos_sim(query_embedding, emb).item()
        if similarity > best_similarity:
            best_similarity = similarity
            best_aid = aid
            best_aid_info = desc

    # Seuil minimal de similarité pour considérer une correspondance
    SIMILARITY_THRESHOLD = 0.4

    if best_similarity >= SIMILARITY_THRESHOLD:
        return best_aid_info, best_aid

    return "Désolé, je n'ai pas trouvé d'aide sociale correspondant à votre besoin.", None

# Création es embeddings dans
# build_and_save_index()
