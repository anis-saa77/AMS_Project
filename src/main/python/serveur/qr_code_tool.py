from langchain.tools import Tool
import os
def qr_code_func(query):
    if not os.listdir("../../../resources/qrcode"): #Si qrcode/ est vide  (pas de pdf ou de qrcode)
        return "La génération d'un QR Code est impossible pour le moment !"
    return "Voici le QR Code demandé."

qr_code_tool = Tool(
    name="qr_code_generation",
    func=qr_code_func,
    description="Affiche un QR Code permettant d'accéder à une version numérique d'une image affichée sur la tablette du robot. Peut être utilisé pour obtenir un lien vers un PDF, suivre un plan sur son téléphone, ou accéder à des informations détaillées à partir d'une image."
)
