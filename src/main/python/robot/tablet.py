import sys
import webview
from settings import *

def show_webview(image_url):
    """ Fonction pour afficher le webview avec une image donnée à une URL """
    # Créer une fenêtre WebView
    webview.create_window("Image Viewer", image_url)
    webview.start()  # Démarre le processus de rendu de la fenêtre
# Test
#image_url = f"http://{SERVER_IP}:5000/getImage/aids/CAF.png"
#show_webview(image_url)