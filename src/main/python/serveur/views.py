import base64
import wave
import json as JSON
from flask import request, jsonify, send_file, render_template, url_for, send_from_directory
from app import app
from functions_server import *
from config_agent import sendMessage, config
from config_conv_model import sendConvMessage, configConv
from model_conv import init_conversation
from ast import literal_eval
from sql import *
from main import SERVER_IP

historic = []
deb_conversation = ["commencer une conversation", "commencer une discution", "débuter une conversation", "débuter une discution", "démarrer une conversation", "démarrer une discution", "je veux parler avec toi"]
create_qr_code(f"http://{SERVER_IP}:5000/download")

RESOURCES_DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources'))
TEMPLATES_PATH = "../../../resources/templates/"
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

        with wave.open("audio.wav", "wb") as wav_file:
            wav_file.setparams(params)
            wav_file.writeframes(audio_data)
            
        message = recognize_speech_from_wav("audio.wav")
        ai_response, tool_name, query = sendMessage(message, "French", config)

        if tool_name == "conversation_tool" :
            json = {
                'message': message,
                'ai_response': ai_response,
                'conversation': True
            }
            print("Début d'une conversation ...")
            historic = []
            init_conversation()
            return json, 200
        
        image_encoded = None
        if not query : #L'appel à la fonction tool n'a pas retourné le 2ème argument (nom de salle ou d'aide)
            json = {
                'message': message,
                'ai_response': ai_response,
                'image': image_encoded
            }                
            return json, 200

        connection = sqlite3.connect("../../../resources/database/data.db")
        cur = connection.cursor()
        if tool_name == 'social_aid':
            image_url = str(getAidImage(cur, query))
            filename = query
            create_pdf_from_image(image_url, filename)
            try:
                response = requests.get(image_url)
                image = response.content
                if response.status_code == 200:
                    image_encoded = base64.b64encode(image).decode('utf-8')
                else:
                    print(f"Erreur lors du téléchargement de l'image: {response.status_code}")
            except Exception as e:
                print(f"Erreur lors de la récupération de l'image: {str(e)}")
        elif tool_name == "direction_indication":
            salle = query
            query = query.upper()
            image_path = "../../../resources/plans/" + salle + ".jpg"
            print(image_path)
            filename = query
            create_pdf_from_image(image_path, filename)
            try:
                with open(image_path, "rb") as img_file:
                    image_encoded = base64.b64encode(img_file.read()).decode('utf-8')
            except FileNotFoundError:
                image_encoded = None  # Pas d'image disponible
        elif tool_name == "qr_code_generation":
            print("Génération du qr_code")
            image_path = "../../../resources/qrcode/qrcode.png"
            try:
                with open(image_path, "rb") as img_file:
                    image_encoded = base64.b64encode(img_file.read()).decode('utf-8')
            except FileNotFoundError:
                image_encoded = None  # Pas d'image disponible
        json = {
            'message': message,
            'ai_response': ai_response,
            'image': image_encoded
        }
        return json, 200
    except Exception as e:
        print("error:", str(e))
        print("ai_response : Je n'ai pas compris. Veuillez répéter.")
        return jsonify({'ai_response' : "Je n'ai pas compris. Veuillez répéter."}), 200

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
        if message.lower() in ["stop", "stoppe"] :
            create_pdf(historic)
            print("Fin de la conversation.")
            image_path = "../../../resources/qrcode/qrcode.png"
            try:
                with open(image_path, "rb") as img_file:
                    image_encoded = base64.b64encode(img_file.read()).decode('utf-8')
            except FileNotFoundError:
                image_encoded = None  # Pas d'image disponible
            return {
                'message': message,
                'ai_response': "Ok, je met fin à la conversation. Voulez vous un historique de la conversation ?",
                'conversation': False,
                'qrcode': image_encoded
            }, 200
        ai_response = str(sendConvMessage(message, "French", configConv))
        json = {
            'message' : message,
            'ai_response' : ai_response,
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
    #TODO Utiliser filename
    bof = filename
    return render_template('display_image.html', image_url=url_for('resources', filename=f'{directory}/qrcode.png'))
    #return render_template('display_image.html', image_url=url_for('static', filename=f'.../{filename}'))