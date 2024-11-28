import os

##############################################################
                        # Model #
##############################################################


####################################################
# Define some variables
####################################################

racine = os.path.dirname(os.path.abspath(__file__))


####################################################
# Read the Langchain API key 
####################################################
def getLangchain_API_Key():
    print(racine)
    try:
        with open(os.path.join(racine, "../../resources/langchain_api_key.txt"), "r", encoding="utf-8") as file:
            content = file.read()
            if content == "":
                print("Votre clé API Langchain n'a pas encore été renseignée.")
                exit(1)
            return content
    except FileNotFoundError:
        print("Le fichier langchain_api_key.txt n'a pas été trouvé.")
        exit(1)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier langchain_api_key.txt : {e}")
        exit(1)


####################################################
# Read the Fireworks API key
####################################################

def getFireworks_API_Key():
    try:
        with open(os.path.join(racine, "../../resources/fireworks_api_key.txt"), "r", encoding="utf-8") as file:
            content = file.read()
            if content == "":
                print("Votre clé API Fireworks n'a pas encore été renseignée.")
                exit(1)
            return content
    except FileNotFoundError:
        print("Le fichier fireworks_api_key.txt n'a pas été trouvé.")
        exit(1)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier fireworks_api_key.txt : {e}")
        exit(1)

##############################################################

def getTavily_API_Key():
    try:
        with open(os.path.join(racine, "../../resources/tavily_search_api_key.txt"), "r", encoding="utf-8") as file:
            content = file.read()
            if content == "":
                print("Votre clé API TavilySearch n'a pas encore été renseignée.")
                exit(1)
            return content
    except FileNotFoundError:
        print("Le fichier tavily_search_api_key.txt n'a pas été trouvé.")
        exit(1)
    except Exception as e:
        print(f"Une erreur s'est produite lors de la lecture du fichier fireworks_api_key.txt : {e}")
        exit(1)