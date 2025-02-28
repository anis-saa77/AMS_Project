import speech_recognition as sr
import os
import qrcode
from pydub import AudioSegment
from fpdf import FPDF


##############################################################
                    # Fonctions_serveur #
##############################################################


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

####################################################
# create_qr_code
####################################################
def create_qr_code(url):
    qr = qrcode.make(url)
    qr.save("qrcode/qrcode.png")

####################################################
# delete_all_pdf
####################################################
def delete_all_pdf():
    for file in os.listdir("pdf"):
        if file.endswith(".pdf"):
            os.remove(f"pdf/{file}")

####################################################
# get_all_pdf_names
####################################################
def get_all_pdf_names():
    pdf_names = []
    for file in os.listdir("pdf"):
        if file.endswith(".pdf"):
            pdf_names.append(file)
    return pdf_names
    
####################################################
# create_pdf
####################################################
def create_pdf(messages):
    delete_all_pdf()

    pdf = FPDF()
    pdf.add_page()
    pdf.add_font("Arial", "", "fonts/arial.ttf", uni=True)
    pdf.set_font("Arial", size=12)

    i = 0
    print(len(messages))
    color1 = [255, 0, 0]
    color2 = [0, 0, 255]
    while i < len(messages):
        print(messages[i])
        print(messages[i+1])
        write_message(messages[i], pdf, color1)
        write_message(messages[i+1], pdf, color2)
        i += 2

    pdf.output("pdf/conversation.pdf")
    
####################################################
# write_message
####################################################
def write_message(message, pdf, color):
    if message.strip():
        pdf.set_text_color(color[0], color[1], color[2])
        pdf.multi_cell(0, 10, message)
        pdf.ln()
