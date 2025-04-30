import string
import json
import re
from sentence_transformers import SentenceTransformer, CrossEncoder, util
import torch
import os
os.environ["TF_CPP_MIN_LOG_LEVEL"] = "3"
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

from sql import *
from settings import DB_FILE_PATH, AIDS_EMBEDDING

# Charger le modèle
model = SentenceTransformer('all-MiniLM-L6-v2')
# TODO Tester :
#model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# Charger le cross-encoder
#cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-6-v2')

def tokenize(text):
    # Séparer en mots simples (alphabet uniquement, sans ponctuation)
    return re.findall(r'\b\w+\b', text.lower())
def remove_punctuation(text):
    translator = str.maketrans('', '', string.punctuation)
    return text.translate(translator)

def build_and_save_index(json_path=AIDS_EMBEDDING):
    connection = sqlite3.connect(DB_FILE_PATH)
    cur = connection.cursor()
    aids = getAids(cur)

    data = {}
    for aid in aids:
        info = getAidInfo(cur, aid)  # Informations utilisé pour l'embedding
        desc = getAidDescription(cur, aid) # Description fournie à l'utilisateur
        desc_clean = info.lower()
        embedding = model.encode(desc_clean, convert_to_numpy=True).tolist()
        data[aid] = {"info": info, "embedding": embedding, "desc": desc}

    connection.close()

    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_index(json_path=AIDS_EMBEDDING):
    aid_embeddings_index = {}
    with open(json_path, "r", encoding="utf-8") as f:
        raw_data = json.load(f)

    for aid, values in raw_data.items():
        desc = values["desc"]
        embedding_tensor = torch.tensor(values["embedding"])
        aid_embeddings_index[aid] = (desc, embedding_tensor)
    return aid_embeddings_index

# Création des embeddings dans un json
build_and_save_index()  # Utilisation unique !
# Chargement des embeddings
aid_embeddings_index = load_index()

CRITICAL_KEYWORDS = {
    "CAF": ["caf", "allocation", "famille", "enfant", "aides sociales"],
    "RSA": ["rsa", "salaire", "argent", "revenu", "sans emploi", "précarité", "stable", "stabilité"],
    "ASPA": ["aspa", "retraite", "retraite", "âgé", "âgée", "senior", "vieux", "vieillesse", "minimum vieillesse"],
    "APL": ["apl", "loyer", "logement", "appartement", "payer", "aide au logement"],
    "ETUDIANT": ["étudiant", "étudiante", "étudiants", "études", "bourse", "bourses", "université", "scolarité", "fac"],
    "FSL": ["fsl", "expulsion", "impayé", "impayés", "maintien", "urgence", "soutien", "expulsé", "expulser"],
    "HANDICAP": ["handicap", "hanidcapé", "invalidité", "accessibilité", "mobilité"],
    "LOCA-PASS": ["loca-pass", "caution", "dépôt de garantie", "emménager", "location", "avance"],
    "SANTE": ["santé", "médical", "médicaux", "médicament", "médicaments", "mutuelle", "soin", "soins", "médecin", "maladie"]
}

SIMILARITY_THRESHOLD = 0.5
TOP_N = 4
KEYWORD_BONUS = 0.15  # à ajuster si nécessaire

def best_aid_finder(query):
    query_cleaned = query.lower()
    query_embedding = model.encode(query_cleaned, convert_to_tensor=True)

    # Etape 1 : Similarité Bi-encoder
    similarities = []
    for aid, (desc, emb) in aid_embeddings_index.items():
        similarity = util.cos_sim(query_embedding, emb).item()
        similarities.append((aid, desc, similarity))

    # Sélection des top-N (par similarité brute)
    top_candidates = sorted(similarities, key=lambda x: x[2], reverse=True)

    print("[Étape 1 - Similarités Bi-encoder]")
    for aid, _, sim in top_candidates[:TOP_N]:
        print(f"{aid}: {sim:.4f}")

    # Etape 2 : Ajout de bonus par mot-clés
    boosted_candidates = []
    query_tokenized = tokenize(query_cleaned)
    for aid, desc, sim in top_candidates:
        bonus = KEYWORD_BONUS * sum(1 for kw in CRITICAL_KEYWORDS.get(aid, []) if kw in query_tokenized)
        boosted_score = sim + bonus
        boosted_candidates.append((aid, desc, boosted_score))

    # Re-trier après bonus
    reranked = sorted(boosted_candidates, key=lambda x: x[2], reverse=True)[:TOP_N]

    print("[Étape 2 - Ajout du bonus]")
    for aid, _, score in reranked:
        print(f"{aid}: {score:.4f}")

    # Etape 3 : Appliquer Cross-Encoder sur top-k boostés
    # pairs = [(query, desc) for (_, desc, _) in boosted_candidates]
    # cross_scores = cross_encoder.predict(pairs)
    #
    # # Normalisation des scores Cross-Encoder
    # min_score = min(cross_scores)
    # max_score = max(cross_scores)
    # normalized_scores = [(score - min_score) / (max_score - min_score + 1e-8) for score in cross_scores]
    #
    # print("\n[Étape 3 - Scores normalisés après CrossEncoder]")
    # reranked = []
    # for (aid, _, desc), norm_score in zip(boosted_candidates, normalized_scores):
    #     reranked.append((aid, desc, norm_score))
    #     print(f"{aid}: {norm_score:.4f}")

    # Trier par score final Cross-Encoder
    #reranked.sort(key=lambda x: x[2], reverse=True)

    best_aid, best_desc, best_score = reranked[0]
    if best_score >= SIMILARITY_THRESHOLD:
        return best_desc, best_aid

    return "Désolé, je n'ai pas trouvé d'aide sociale correspondant à votre besoin.", None
