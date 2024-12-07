import speech_recognition as sr
import os
from pydub import AudioSegment

def mp3_to_wav(mp3_filename, wav_filename):
    audio = AudioSegment.from_mp3(mp3_filename)
    audio.export(wav_filename, format="wav")
    
    os.remove(mp3_filename)
    
def recognize_speech_from_wav(wav_filename):
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_filename) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="fr-FR")
        print("Contenu de l'audio :", text)
    except sr.UnknownValueError:
        print("Google Speech Recognition n'a pas pu comprendre l'audio")
    except sr.RequestError as e:
        print(f"Erreur de la requête au service Google Speech Recognition : {e}")
        
def recognize_speech_sphinx(wav_filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        audio = recognizer.record(source)
    try:
        # Utilisation de CMU Sphinx, qui est local
        text = recognizer.recognize_sphinx(audio)
        print("Contenu de l'audio (Sphinx) :", text)
        return text
    except sr.UnknownValueError:
        print("CMU Sphinx n'a pas pu comprendre l'audio")
    except sr.RequestError as e:
        print(f"Erreur de la requête au moteur Sphinx : {e}")
