import base64
import wave
from flask import request, jsonify, send_file, render_template, url_for, send_from_directory
from ast import literal_eval

from app import app
from audio import *
from pdf import *
from config_agent import sendMessage, config
from config_conv_model import sendConvMessage, configConv
from model_conv import init_conversation
from settings import *

historic = []
deb_conversation = ["commencer une conversation", "commencer une discution", "débuter une conversation", "débuter une discution", "démarrer une conversation", "démarrer une discution", "je veux parler avec toi"]
create_qr_code(f"http://{SERVER_IP}:{PORT}/download")

@app.route('/')
def homepage():
	return 'Home page'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        data = request.get_json(force=True)
        
        audio_base64 = data.get('audio_base64')
        params_base64 = data.get('params_base64')
        
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
            
        message = recognize_speech_from_wav(AUDIO_FILE_PATH)
        ai_response, tool_name, entity = sendMessage(message, "French", config)

        if tool_name == "conversation_tool":
            json = {
                'message': message,
                'ai_response': ai_response,
                'conversation': True
            }
            print("Début d'une conversation ...")
            historic.clear()
            init_conversation()
            return json, 200

        if not entity:  # L'appel à la fonction tool n'a pas retourné d'entité (ex : 'CAF', 'APL', 'S2', 'Stat4'...)
            json = {
                'message': message,
                'ai_response': ai_response
            }                
            return json, 200
        entity = entity.upper()  # entity = 'CAF', 'APL', 'S2', 'Stat4'...

        if tool_name == 'social_aid':
            update_pdf(tool_name, entity)
            image_loc = AIDS_DIR_PATH+entity+".png"

        elif tool_name == "direction_indication":
            update_pdf(tool_name, entity)
            image_loc = f"plans/{entity}.jpg"

        elif tool_name == "qr_code_generation":
            image_loc = "qrcode/qrcode.png"

        else:
            image_loc = None

        json = {
            'message': message,
            'ai_response': ai_response,
            'image_loc': image_loc,
        }
        return json, 200

    except Exception as e:
        print("error:", str(e))
        return jsonify({'ai_response': "Je n'ai pas compris. Veuillez répéter."}), 200

@app.route('/conversation', methods=['GET', 'POST'])
def conversation():
    try:
        data = request.get_json(force=True)
        
        audio_base64 = data.get('audio_base64')
        params_base64 = data.get("params_base64")
        
        if not audio_base64:
            return jsonify({"error": "Aucun audio base64 fourni"}), 400

        audio_data = base64.b64decode(audio_base64)
        
        if not params_base64:
            return jsonify({"error": "Aucun paramètre fourni"}), 400
        
        params = base64.b64decode(params_base64)
        params = literal_eval(params.decode("utf-8"))

        with wave.open("audio.wav", "wb") as wav_file:
            wav_file.setparams(params)
            wav_file.writeframes(audio_data)
            
        message = recognize_speech_from_wav("audio.wav")
        if message.lower() in ["stop", "stoppe"]:
            create_pdf(historic)
            print("Fin de la conversation.")
            return {
                'message': message,
                'ai_response': "Ok, je met fin à la conversation. Voulez vous un historique de la conversation ?",
                'conversation': False,
                'image_loc': "qrcode/qrcode.png"
            }, 200
        ai_response = str(sendConvMessage(message, "French", configConv))
        json = {
            'message': message,
            'ai_response': ai_response,
            'conversation': True
        }
        historic.append(message)
        historic.append(ai_response)
        return json, 200
    except Exception as e:
        print("error:", str(e))
        print("ai_response : Je n'ai pas compris. Veuillez répéter.")
        return jsonify({'ai_response': "Je n'ai pas compris. Veuillez répéter."}), 200
    
@app.route('/test', methods=['GET', 'POST'])
def test():
    json = {
        'ai_response': "Ceci est un test, je fonctionne bien."
    }
    return json, 200

@app.route('/download', methods=['GET'])
def download():
    names = get_all_pdf_names()
    if len(names) == 0:
        return jsonify({"error": "Aucun fichier PDF disponible"}), 400
    file_path = "pdf/" + names[0]
    return send_file(file_path, as_attachment=True)

@app.route('/resources/<path:filename>')
def resources(filename):
    print(f"Path to resource: {os.path.join(RESOURCES_DIR_PATH, filename)}")
    return send_from_directory(RESOURCES_DIR_PATH, filename)

@app.route('/getImage/<directory>/<filename>', methods=['GET'])
def get_image(directory, filename):
    return render_template('display_image.html', image_url=url_for('resources', filename=f'{directory}/{filename}'))
