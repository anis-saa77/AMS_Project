from config_agent import sendMessage, config
from settings import TEST_FILE_PATH, TEST_OUTPUT_PATH, LOG_FILE_PATH
import time
import sys
from social_aid_tool import best_aid_finder
# TODO Modifier le threa_id pour ignorer la mémoire ?

if __name__ == '__main__':
    """ Test des résultats du modèle sur un ensemble de phrases """

    tool_not_used = 0
    start_time = time.time()
    LIMIT = 6  # Limite le nombre de phrases à tester (et de requêtes à l'api)

    with open(TEST_FILE_PATH, "r", encoding="utf-8") as input_file:
        #with open(TEST_OUTPUT_PATH, "w", encoding="utf-8") as output_file:
        for index, line in enumerate(input_file, start=1):
            message = line.strip()  # Enlever les espaces blancs en début et fin de ligne
            if message:
                try:
                    # Génération de la réponse
                    config['configurable']["thread_id"] = f"abc{index}"
                    ai_message, tool_name, entity = sendMessage(message, "French", config)

                    # Modification du retour si appel à social_aid
                    if tool_name == 'social_aid':
                        ai_message, entity = best_aid_finder(message)
                        print("Human Message : ", message)
                        print("AI Message :", ai_message)
                        print("Tool Call : ", tool_name)
                        print("Aid :", entity)

                    if not tool_name:
                         tool_not_used += 1

                    # Enregistrer les résultats dans out.txt (commenté ici)
                    # output_file.write(f"Message: {message}\n")
                    # output_file.write(f"AI Response: {ai_message}\n")
                    # if tool_name:
                    #     output_file.write(f"Tool Used: {tool_name}\n")
                    # if entity:
                    #     output_file.write(f"Entity: {entity}\n")
                    # output_file.write("\n" + "=" * 50 + "\n")

                except Exception as e:
                    # En cas d'erreur, afficher l'indice de l'itération et l'exception
                    sys.stderr.write(f"Erreur lors du traitement de la ligne {index}: {e}\n")
                    exit(0)
            if index == LIMIT:
                break

    with open(LOG_FILE_PATH, "w", encoding="utf-8") as log_file:
        log_file.write(f"Tool not used : {tool_not_used}%\n")
        execution_time = time.time() - start_time
        log_file.write(f"Temps d'exécution : {execution_time}\n")
