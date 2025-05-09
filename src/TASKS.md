## Tâches + ~Idée :

Refaire requirments
----
**Historique :**
- Qui commence à parler, l'ia ou l'humain ? (pour altérner les polices différement en fonction de la réponse)

**Aide Sociales :**
- Embedding
- Utilisation de "config" pour exécuter un nouveau thread et suggérer la requête via une utilisation du modèle avec un autre "prompt".
 **Compliqué** car signifierait passer sur de l'asyncrone / manque de temps

**Direction Tool**
- Fournir un plan du CERI

**Choregraph**
- Afficher sur la tablette "Mode Assistant" / "Mode conv"
- (Quiz) / Affichage, Jouer un son, geste confirmant la réponse...

**Tests**
- Avec et sans "Utilise uniquement les outils si possible." dans le prompt
- Avec et sans influence sur la prise de décision
- Avec et sans modif du tool_args / de inputs dans agent executor
- Commande pour lancer les test en ignorant les prints : python test.py > $null

**Corrections/Améliorations**
- ~Changement de modèle pour des query plus précise / des décisions plus juste / moins d'erreurs de réponses json?
- Régler le problème --> La réponse est au format json :  {"type": "function", "name": "direction_indication", "parameters": {"__arg1": "S3"}}

- Détécter les parties les plus gourmandes en temps d'exécution et optimiser
- Demander des informations supplémentaires pour une réponse correcte.
- Modifier les paramètres suivant ?


```
trimmer = trim_messages(
    max_tokens=65,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)
```

