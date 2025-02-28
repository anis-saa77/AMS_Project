import string
from langchain.tools import Tool
from functions_server import create_qr_code
import os
def qr_code_func(query):
    if not os.listdir("qrcode"): #Si il n'y a pas de pdf
        return "La génération d'un QR Code est impossible"
    create_qr_code("http://172.20.10.2:5000/download")
    return "Voici le QR Code demandé."

qr_code_tool = Tool(
    name="qr_code_generation",
    func=qr_code_func,
    description="Génère un QR Code permettant d'accéder à une version numérique d'une image affichée sur la tablette du robot. Peut être utilisé pour obtenir un lien vers un PDF, suivre un plan sur son téléphone, ou accéder à des informations détaillées à partir d'une image."
)
