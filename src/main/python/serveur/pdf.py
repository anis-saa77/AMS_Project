import qrcode
from fpdf import FPDF
from PIL import Image
from datetime import datetime
import shutil

from settings import *

##############################################################
                    # Fonctions_serveur #
##############################################################
class CustomPDF(FPDF):
    def __init__(self, orientation='P', unit='mm', format='A4'):
        super().__init__(orientation, unit, format)
        self.set_auto_page_break(auto=True, margin=15)
        # Ajout des polices
        # pdf.add_font("", CONSOLAS_FONT_PATH, uni=True)
        # pdf.add_font("", ARIAL_FONT_PATH, uni=True)
        # pdf.add_font("", SEGOE_UI_FONT_PATH, uni=True)
        # pdf.add_font("DejaVu", DEJA_VU_FONT_PATH, uni=True)
        # pdf.add_font("Roboto", ROBOTO_FONT_PATH, uni=True)

    def add_page(self, orientation='P', format='A4'):
        super().add_page()
        self.set_custom_background()

    def set_custom_background(self):
        self.set_fill_color(224, 228, 204)
        self.rect(0, 0, 210, 297, 'F')


####################################################
# create_qr_code
####################################################
def create_qr_code(url):
    qr = qrcode.make(url)
    qr.save(QR_CODE_PATH)

####################################################
# add_cover_page
####################################################
def add_cover_page(pdf):
    pdf.add_page()

    pdf.set_custom_background()

    pdf.set_font("Arial", style="B", size=24)
    pdf.set_text_color(0, 51, 102)
    pdf.ln(50)
    pdf.cell(0, 60, "Transcription de la Conversation", ln=True, align='C')

    pdf.set_font("Arial", size=12)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 10, f"Date: {datetime.today().strftime('%d/%m/%Y')}", ln=True, align='C')

    pdf.ln(20)

####################################################
# delete_all_pdf
####################################################
def delete_all_pdf():
    for file in os.listdir(PDF_DIR_PATH):
        if file.endswith(".pdf"):
            os.remove(f"{PDF_DIR_PATH}{file}")


####################################################
# get_all_pdf_names
####################################################
def get_all_pdf_names():
    pdf_names = []
    for file in os.listdir(PDF_DIR_PATH):
        if file.endswith(".pdf"):
            pdf_names.append(file)
    return pdf_names

def fix_encoding(text):
    replacements = {
        "œ": "oe",
        "Œ": "OE",
        "€": "EUR",
        "‘": "'", "’": "'", "“": '"', "”": '"',
        "–": "-", "—": "-",
        "…": "..."
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

####################################################
# create_pdf
####################################################
def create_pdf(messages):
    delete_all_pdf()

    pdf = CustomPDF()
    add_cover_page(pdf)

    pdf.add_page()

    i = 0
    pdf.set_font("Arial", size=12)
    color1 = [64, 142, 79]
    color2 = [25, 92, 148]
    while i < len(messages):
        msg1 = fix_encoding(messages[i])
        msg2 = fix_encoding(messages[i + 1])
        #pdf.set_font(HUMAN_FONT, size=12)
        write_message(msg1, pdf, color1)
        #pdf.set_font(AI_FONT, size=12)
        write_message(msg2, pdf, color2, human=False)
        i += 2

    pdf.output(PDF_DIR_PATH + "conversation.pdf")


####################################################
# write_message
####################################################
def write_message(message, pdf, color, human=True):
    if message.strip():
        pdf.set_text_color(color[0], color[1], color[2])

        width = min(120, pdf.get_string_width(message)) + 5
        pdf.set_y(pdf.get_y() + 10)
        if human:
            pdf.set_x(190 - width + 10)
        pdf.multi_cell(width, 10, message, align="L")

        x = pdf.get_x()
        if human:
            x = 190 - width
        y = pdf.get_y()

        pdf.set_draw_color(10, 10, 10)
        pdf.line(x, y, x + width + 10, y)

        pdf.ln(5)
def update_pdf(tool_name, entity):
    delete_all_pdf()
    if tool_name == 'social_aid':
        try:
            image_path = f'{AIDS_DIR_PATH}{entity}.pdf'
            destination_path = os.path.join(PDF_DIR_PATH, f'{entity}.pdf')
            shutil.copy(image_path, destination_path)
        except Exception as e:
            print(f"Erreur lors de la copie du PDF : {e}")

    elif tool_name == 'direction_indication':
        try:
            image_path = f'{PLANS_DIR_PATH}{entity}.jpg'
            image = Image.open(image_path)
            filepath = PDF_DIR_PATH + entity + ".pdf"
            image.convert('RGB').save(filepath, "PDF", resolution=100.0)
        except Exception as e:
            print(f"Erreur lors de la création du PDF : {e}")

create_pdf(["dsé\nnqfkçl", 'ls…dfq'])