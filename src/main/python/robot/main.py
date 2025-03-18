# Ajouter le dossier python au chemin des modules
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *  # Do not delete !

import matplotlib.pyplot as plt
from PIL import Image
import time
from functions import *
from webview import show_webview


##############################################################
                        # Execution #
##############################################################


audio_filepath = "temp/output.wav"

while True:
    record_audio_to_wav(audio_filepath, duration=10)
    response = send_audio(audio_filepath, "upload")

    print("Vous avez dit :", response.json().get("message"))
    print("L'IA a répondu :", response.json().get("ai_response"))

    if response.json().get("conversation"):
        while True:
            record_audio_to_wav(audio_filepath, duration=10)
            response = send_audio(audio_filepath, "conversation")

            print("Vous avez dit :", response.json().get("message"))
            print("L'IA a répondu :", response.json().get("ai_response"))

            if not response.json().get("conversation"):
                print("Quitte la conversation.")
                break
    if response.json().get('image'):
        image_base64 = response.json().get("image")
        image_data = base64.b64decode(image_base64)

        with open("temp/image.jpg", "wb") as img_file:  # Sauvegarde en JPEG
            img_file.write(image_data)
        time.sleep(1)
        #Affichage de l'image reçu
        image = Image.open("temp/image.jpg")
        plt.imshow(image)
        plt.axis("off")  # Cacher les axes
        plt.show()

    if response.json().get('image_url'):
        image_url = response.json().get('image_url')
        show_webview(f"http://{SERVER_IP}:5000/getImage/"+image_url)

    if response.json().get('qrcode'):
        image_base64 = response.json().get("qrcode")
        image_data = base64.b64decode(image_base64)
        with open("temp/image.jpg", "wb") as img_file:  # Sauvegarde en JPEG
            img_file.write(image_data)
        time.sleep(1)
        #Affichage de l'image reçu
        image = Image.open("temp/image.jpg")
        plt.imshow(image)
        plt.axis("off")  # Cacher les axes
        plt.show()

    if response.json().get("ai_response") == "STOP":
        break

print("Fin")

##############################################################
