# Projet AMS - Sujet 1 : Chatbot Vocal
---

## Structure du projet :

```commandline
+---main
    +---python
        +---robot       ### Emulateur du robot utilisé pour les tests
            |---settings.py                # Fichier de paramètrage
            |---functions.py               # Fonctions utilitaires
            |---tablet.py                  # Emulation de la tablette du robot
            |---main.py                    # Programme principal de l'émulateur
        +---serveur     ### Regroupe la partie serveur Flask et LLM du projet
            |---settings.py                # Fichier de paramètrage (paths + ip du serveur...)
            |---main.py                    # Lancement du programme
                                                                                        ─┐       
            |---pdf.py                     # Fonctions de création de pdf                |  
            |---audio.py                   # Enregistrement et transcription audio       | Fonctions utilitaires
            |---sql.py                     # Fonctions de requêtes à la BD               |
                                                                                        ─┘ 
                                                                                        ─┐
            |---app.py                     # Fichier app du serveur Flask                |
            |---config_server.py           # Fichier de configuration du serveur         | Serveur
            |---views.py                   # Fichier de routage                          |
                                                                                        ─┘
                                                                                        ─┐
            |---config_agent.py            # Configuration du modèle/agent               |    
            |---state.py                   # Etat du modèle                              | Mode assistant
            |---custom_agent_executor.py   # Agent exécuteur modifié                     |
            |---model.py                   # Fichier de définission du modèle            |
                                                                                        ─┘
                                                                                        ─┐
            |---tools.py                   # Les 'tools' utilisés par l'agent            |
            |---conversation_tool.py       # Outil pour démarrer le mode conversation    |
            |---social_ai_tool.py          # Outil de suggéstion d'aide sociale          |
            |---social_ai_tool_wrapper.py  # 'Wrapper' de social_aid_tool                |  Tools
            |---direction_tool.py          # Outil d'orientation vers les salles         |
            |---qr_code_tool.py            # Outil d'affichage du QR Code                |
            |---stop_tool.py               # Outil pour arrêter l'interaction            |
                                                                                        ─┘     
                                                                                        ─┐
            |---config_conv_model.py       # Configuration du modèle de conversation     |
            |---state_conv.py              # État du modèle de conversation              | Mode Conversation
            |---conv_model.py              # Modèle de conversation                      |
                                                                                        ─┘
                                                                                        ─┐
            |---test.py                   # Fichier de test des réponses                 |
            |---test_api.py               # Test des requête à l'API du LLM              | Test
            |---test_historic.py          # Test de la génération de l'historique        |
                                                                                        ─┘
+---resources    # Contient toutes les ressources utilisées (images, BD, pdf, templates...)
```    
    
    
## Exécution :

### 1. Créer un environment (python ou anaconda) et l'activer
### 2. Installer les librairies nécessaires
```commandline
pip install -r requirements.txt
```

### 3. Générer les clés API
- Générer la clé API pour Langchain
- Générer la clé API pour Fireworks
- Les copier dans un fichier .env à la source du projet :
  ````
    LANGCHAIN_API_KEY=
    FIREWORKS_API_KEY=
  ````
### 4. Lancer le serveur
```commandline
python src/main/python/serveur/main.py
```

### 5. Lancer l'émulateur du robot
```commandline
python src/main/python/robot/main.py
```
### Ou choregraphe si robot Pepper disponible.

---

par Anis SAA & Grégoire PIERROT
