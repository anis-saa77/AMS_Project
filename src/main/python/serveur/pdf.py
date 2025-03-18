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
    def add_page(self, orientation='', format=''):
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


####################################################
# create_pdf
####################################################
def create_pdf(messages):
    delete_all_pdf()

    pdf = CustomPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.add_font("Arial", "", FONTS_DIR_PATH + "/arial.ttf", uni=True)

    add_cover_page(pdf)

    pdf.add_page()
    pdf.set_font("Arial", size=12)

    i = 0
    color1 = [64, 142, 79]
    color2 = [25, 92, 148]
    while i < len(messages):
        write_message(messages[i], pdf, color1)
        write_message(messages[i + 1], pdf, color2, human=False)
        i += 2

    pdf.output(PDF_DIR_PATH + "conversation.pdf")


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
