import pyaudio
import wave
import base64
import requests

from settings import AUDIO_OUTPUT_PATH, ROBOT_URL


##############################################################
# Functions #
##############################################################

###################################################
# wav_to_base64
###################################################
def wav_to_base64(audio_filename):
    with open(audio_filename, "rb") as audio_file:
        audio_data = audio_file.read()
        base64_audio = base64.b64encode(audio_data).decode("utf-8")
        return base64_audio


###################################################
# send_audio
###################################################
def send_audio(filename, route):
    audio_base64 = wav_to_base64(filename)

    with wave.open(filename, "rb") as wav_file:
        params = wav_file.getparams()
        params_tuple = (
            params.nchannels,
            params.sampwidth,
            params.framerate,
            params.nframes,
            params.comptype,
            params.compname
        )

    params_base64 = base64.b64encode(str(params_tuple).encode("utf-8")).decode("utf-8")

    url = ROBOT_URL + route
    headers = {"Content-Type": "application/json"}
    payload = {
        "audio_base64": audio_base64,
        "params_base64": params_base64
    }

    response = requests.post(url, json=payload, headers=headers)
    return response


###################################################
# record_audio_to_wav
###################################################
def record_audio_to_wav(filepath=AUDIO_OUTPUT_PATH, duration=15):
    FORMAT = pyaudio.paInt16  # Format du son (16 bits)
    CHANNELS = 1  # Mono
    RATE = 44100  # Taux d'échantillonnage (Hz)
    CHUNK = 1024  # Taille des morceaux de son
    DURATION = duration  # Durée de l'enregistrement en secondes
    OUTPUT_FILE = filepath  # Nom du fichier de sortie

    # Initialisation de PyAudio
    audio = pyaudio.PyAudio()

    # Ouverture du flux audio
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)

    print("Enregistrement en cours...")

    frames = []

    # Enregistre l'audio en lisant le flux par morceaux
    for _ in range(0, int(RATE / CHUNK * DURATION)):
        data = stream.read(CHUNK)
        frames.append(data)

    print("Enregistrement terminé.")

    # Fermeture du flux et de PyAudio
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # Sauvegarde du fichier WAV
    with wave.open(OUTPUT_FILE, "wb") as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b"".join(frames))

    #print(f"Fichier sauvegardé sous '{OUTPUT_FILE}'")
