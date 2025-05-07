import threading
from settings import *  # Do not delete !
from functions import *
from tablet import show_webview

"""      ______Exécution______        """

while True:  # Boucle Principale
    record_audio_to_wav(AUDIO_OUTPUT_PATH, duration=10)
    response = send_audio(AUDIO_OUTPUT_PATH, "upload")

    print("Vous avez dit :", response.json().get("message"))
    print("L'IA a répondu :", response.json().get("ai_response"))

    if response.json().get("conversation"):
        while True:  # Boucle du Mode Conversation
            record_audio_to_wav(AUDIO_OUTPUT_PATH, duration=10)
            response = send_audio(AUDIO_OUTPUT_PATH, "conversation")

            print("Vous avez dit :", response.json().get("message"))
            print("L'IA a répondu :", response.json().get("ai_response"))

            if not response.json().get("conversation"):
                print("Quitte la conversation.")
                break

    if response.json().get('image_loc'):
        image_loc = response.json().get('image_loc')
        #image_url = f"http://{SERVER_IP}:{PORT}/getImage/{image_loc}"
        image_url = f"http://{SERVER_IP}:{PORT}/getView/true"
        show_webview(image_url)

    if response.json().get("ai_response") == "STOP":
        break

print("Fin")
