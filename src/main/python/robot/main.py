import speech_recognition as sr
from functions import *

##############################################################
                        # Execution #
##############################################################

audio_filename = "output.wav"

while True:
    record_audio_to_wav(audio_filename, duration=10)
    response = send_audio(audio_filename, "upload")

    print("Vous avez dit :", response.json().get("message"))
    print("L'IA a répondu :", response.json().get("ai_response"))

    if response.json().get("conversation"):
        while True:
            record_audio_to_wav(audio_filename, duration=10)
            response = send_audio(audio_filename, "conversation")

            print("Vous avez dit :", response.json().get("message"))
            print("L'IA a répondu :", response.json().get("ai_response"))

            if not response.json().get("conversation"):
                print("Quitte la conversation.")
                break
    if response.json().get('image'):
        image_base64 = response.json().get("image")
        image_data = base64.b64decode(image_base64)
        with open("image.jpg", "wb") as img_file:  # Sauvegarde en JPEG
            img_file.write(image_data)

    if response.json().get("message") == "stoppe":
        break

print("Fin")


##############################################################
