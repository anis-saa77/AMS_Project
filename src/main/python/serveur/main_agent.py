import speech_recognition as sr
from config_agent import sendMessage, config

##############################################################
                        # Execution #
##############################################################
if __name__ == '__main__':
    while True:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            print("Parle maintenant...")
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)

        message = None
        try:
            message = recognizer.recognize_google(audio, language="fr-FR")
            print("Human message: " + message)
        except sr.UnknownValueError:
            print("Je n'ai pas pu comprendre ce qui a été dit.")
        except sr.RequestError:
            print("Erreur avec le service de reconnaissance vocale.")

        if message:
            sendMessage(message, "French", config)

##############################################################