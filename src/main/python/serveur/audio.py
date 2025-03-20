import speech_recognition as sr
from pydub import AudioSegment
import base64
import wave
from flask import jsonify
from ast import literal_eval
import os

from settings import AUDIO_FILE_PATH

####################################################
# mp3_to_wav
####################################################
def mp3_to_wav(mp3_filename, wav_filename):
    audio = AudioSegment.from_mp3(mp3_filename)
    audio.export(wav_filename, format="wav")

    os.remove(mp3_filename)


####################################################
# recognize_speech_from_wav
####################################################
def recognize_speech_from_wav(wav_filename):
    recognizer = sr.Recognizer()

    with sr.AudioFile(wav_filename) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language="fr-FR")
        print("Contenu de l'audio :", text)
        return text
    except sr.UnknownValueError:
        print("Google Speech Recognition n'a pas pu comprendre l'audio")
    except sr.RequestError as e:
        print(f"Erreur de la requête au service Google Speech Recognition : {e}")


####################################################
# recognize_speech_sphinx
####################################################
def recognize_speech_sphinx(wav_filename):
    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_filename) as source:
        audio = recognizer.record(source)
    try:
        # Utilisation de CMU Sphinx, qui est local
        text = recognizer.recognize_sphinx(audio, language="fr-FR")
        print("Contenu de l'audio (Sphinx) :", text)
        return text
    except sr.UnknownValueError:
        print("CMU Sphinx n'a pas pu comprendre l'audio")
    except sr.RequestError as e:
        print(f"Erreur de la requête au moteur Sphinx : {e}")

def transcribe_audio_data(audio_data, filepath):
    audio_base64 = audio_data.get('audio_base64')
    params_base64 = audio_data.get('params_base64')

    if not audio_base64:
        return jsonify({"error": "Aucun audio base64 fourni"}), 400

    audio_data = base64.b64decode(audio_base64)

    if not params_base64:
        return jsonify({"error": "Aucun paramètre fourni"}), 400

    params = base64.b64decode(params_base64)
    params = literal_eval(params.decode("utf-8"))

    with wave.open(AUDIO_FILE_PATH, "wb") as wav_file:
        wav_file.setparams(params)
        wav_file.writeframes(audio_data)

    message = recognize_speech_from_wav(filepath)
    return message