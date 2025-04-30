from flask import request, jsonify, send_file, render_template, url_for, send_from_directory

from app import app
from audio import transcribe_audio_data
from pdf import *
from config_agent import sendMessage, config
from config_conv_model import sendConvMessage, configConv
from model_conv import init_conversation
from best_aid import best_aid_finder
from settings import *

#deb_conversation = ["commencer une conversation", "commencer une discution", "débuter une conversation", "débuter une discution", "démarrer une conversation", "démarrer une discution", "je veux parler avec toi"]
historic = []
create_qr_code(f"http://{SERVER_IP}:{PORT}/download")

@app.route('/')
def homepage():
	return 'Home page'

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        audio_data = request.get_json(force=True)
        human_message = transcribe_audio_data(audio_data, AUDIO_FILE_PATH)

        # Traitement du message par le model/agent
        ai_response, tool_name, entity = sendMessage(human_message, "French", config)

        if tool_name == "conversation_tool":
            json = {
                'message': human_message,
                'ai_response': ai_response,
                'conversation': True
            }
            print("Début d'une conversation ...")
            historic.clear()
            init_conversation()
            return json, 200

        # Modification du retour si appel à social_aid
        if tool_name == 'social_aid':  # Ne pas déplacer !
            ai_response, entity = best_aid_finder(human_message)

        # Débug prints
        print("AI Message : ", ai_response)
        print("Tool Call : ", tool_name)
        print("Entity : ", entity)

        if not entity:  # L'appel à la fonction tool n'a pas retourné d'entité (ex : 'CAF', 'APL', 'S2', 'Stat4'...)
            json = {
                'message': human_message,
                'ai_response': ai_response
            }                
            return json, 200
        entity = entity.upper()  # entity = 'CAF', 'APL', 'S2', 'Stat4'...

        if tool_name == 'social_aid':
            update_pdf(tool_name, entity)
            image_loc = "aids/"+entity+".png"

        elif tool_name == "direction_indication":
            update_pdf(tool_name, entity)
            image_loc = f"plans/{entity}.jpg"

        elif tool_name == "qr_code_generation":
            image_loc = "qrcode/qrcode.png"

        else:
            image_loc = None

        json = {
            'message': human_message,
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
        audio_data = request.get_json(force=True)
        message = transcribe_audio_data(audio_data, AUDIO_FILE_PATH)

        if message.lower() in ["stop", "stoppe"]:  # Condition d'arrêt de la conversation
            create_pdf(historic)
            print("Fin de la conversation.")
            return {
                'message': message,
                'ai_response': "Ok, je met fin à la conversation. Sannez le QR Code pour avoir un historique de notre conversation. Vous devez être connecté au réseau du CERI.",
                'conversation': False,
                'image_loc': "qrcode/qrcode.png"
            }, 200

        # Traitement du message par le model conversationnel
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
    file_path = PDF_DIR_PATH + names[0]
    return send_file(file_path, as_attachment=True)

@app.route('/resources/<path:filename>')
def resources(filename):
    print(f"Path to resource: {os.path.join(RESOURCES_DIR_PATH, filename)}")
    return send_from_directory(RESOURCES_DIR_PATH, filename)

@app.route('/getImage/<directory>/<filename>', methods=['GET'])
def get_image(directory, filename):
    print("Requête reçue pour :", request.url)
    image_url = url_for('resources', filename=f'{directory}/{filename}')
    is_qrcode = (filename == "qrcode.png")
    homepage_url = "http://"+str(SERVER_IP)+":"+str(PORT)+"/getImage/qrcode/qrcode.png"
    return render_template('display_image.html', image_url=image_url, is_qrcode=bool(is_qrcode), homepage_url=str(homepage_url))
