## Tâches + ~Idée :
----
**Historique :**
- Qui commence à parler, l'ia ou l'humain ? (pour altérner les polices différement en fonction de la réponse)

**Aide Sociales :**
- Embedding
- Utilisation de "config" pour exécuter un nouveau thread et suggérer la requête via une utilisation du modèle avec un autre "prompt".
 **Compliqué** car signifierait passer sur de l'asyncrone / manque de temps

**Quiz**
- Affichage sur tablette, jouer un son ou faire geste confirmant la réponse...

**Tests**
- Avec et sans "Utilise uniquement les outils si possible." dans le prompt
- Avec et sans influence sur la prise de décision
- Avec et sans modif du tool_args / de inputs dans agent executor

**Corrections/Améliorations**
- ~Changement de modèle pour des query plus précise / des décisions plus juste / moins d'erreurs de réponses json?
- Détécter les parties les plus gourmandes en temps d'exécution et optimiser
- Système de demande 'informations supplémentaires pour une réponse correcte.
- Modifier le trimmer ?