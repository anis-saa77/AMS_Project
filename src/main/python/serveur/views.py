import base64
from flask import request, jsonify
from app import app
from functions_server import mp3_to_wav, recognize_speech_from_wav, recognize_speech_sphinx
from config_agent import sendMessage, config

@app.route('/')
def homepage():
	return 'Home page'

@app.route('/upload', methods=['POST'])
def upload():
    try:
        data = request.get_json()
        
        audio_base64 = data.get('audio_base64')
        if not audio_base64:
            return jsonify({"error": "Aucun audio base64 fourni"}), 400

        audio_data = base64.b64decode(audio_base64)

        with open("received_audio.mp3", "wb") as audio_file:
            audio_file.write(audio_data)
        
        mp3_to_wav("received_audio.mp3", "audio.wav")
        message = recognize_speech_from_wav("audio.wav")
        ai_response = sendMessage(message, "French", config)
        #recognize_speech_sphinx("audio.wav")
        json = {
            'message' : message,
            'ai_reponse' : ai_response
        }
        return json, 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500