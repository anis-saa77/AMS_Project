from flask import request, jsonify, send_file, render_template, url_for, send_from_directory

from app import app
from audio import transcribe_audio_data
from pdf import *
from config_agent import sendMessage, config
from config_conv_model import sendConvMessage, configConv
from conv_model import init_conversation
from social_aid_tool import best_aid_finder
from settings import *

historic = []
create_qr_code(f"http://{SERVER_IP}:{PORT}/download")

current_image = "webview/homepage.png"
show_qr_button = False

@app.route('/')
def homepage():
    return 'Home page'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    global current_image, show_qr_button
    try:
        audio_data = request.get_json(force=True)
        human_message = transcribe_audio_data(audio_data, AUDIO_FILE_PATH)

        # Traitement du message par le model/agent
        ai_response, tool_name, entity = sendMessage(human_message, "French", config)

        if tool_name == "conversation_tool":
            print("Début d'une conversation ...")
            json = {
                'message': human_message,
                'ai_response': ai_response,
                'conversation': True
            }
            historic.clear()
            init_conversation()
            current_image = "webview/conv_mode.png"
            show_qr_button = False
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
            image_loc = "aids/" + entity + ".png"
            show_qr_button = True

        elif tool_name == "direction_indication":
            update_pdf(tool_name, entity)
            image_loc = f"plans/{entity}.jpg"
            show_qr_button = True

        elif tool_name == "qr_code_generation":
            image_loc = "qrcode/qrcode.png"
            show_qr_button = False

        else:
            image_loc = "webview/assist_mode.png"
            show_qr_button = False

        current_image = image_loc

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
    global current_image, show_qr_button
    try:
        audio_data = request.get_json(force=True)
        message = transcribe_audio_data(audio_data, AUDIO_FILE_PATH)

        if message.lower().strip() == "arrêter la conversation":  # Condition d'arrêt de la conversation
            create_pdf(historic)
            print("Fin de la conversation.")
            current_image = "qrcode/qrcode.png"
            show_qr_button = False
            return {
                'message': message,
                'ai_response': "Ok, je met fin à la conversation. Sannez le QR Code pour avoir un historique de notre conversation. Vous devez être connecté au réseau du CERI.",
                'conversation': False,
                'image_loc': "qrcode/qrcode.png"
            }, 200

        # Traitement du message par le model conversationnel
        ai_response = str(sendConvMessage(message, "French", configConv))
        current_image = "webview/conv_mode.png"
        show_qr_button = False

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

@app.route('/getView/<listening>', methods=['GET'])
def get_view(listening):
    image = url_for('resources', filename=current_image)
    is_listening = listening.lower() == "true"
    # print("Current image:", current_image)
    # print("Image URL:", image)
    # print("Listening : ", is_listening)
    qrcode_url = "http://" + str(SERVER_IP) + ":" + str(PORT) + "/getQRCode/false"
    return render_template('current_image.html', image=image, listening=is_listening,
                           show_qr_button=show_qr_button,
                           qrcode_url=qrcode_url)

@app.route('/getQRCode/<listening>', methods=['GET'])
def get_qrcode(listening):
    global current_image, show_qr_button
    current_image, show_qr_button = "qrcode/qrcode.png", False
    return get_view(listening)