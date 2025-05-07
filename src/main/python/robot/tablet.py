import sys
import webview
from settings import *

def show_webview(url):
    """ Fonction pour afficher le webview """
    # Créer une fenêtre WebView
    webview.create_window("Image Viewer", url)
    webview.start()  # Démarre le processus de rendu de la fenêtre

# Test
#url = f"http://{SERVER_IP}:5000/getImage/aids/CAF.png"
#show_webview(url)

# Test Amélioration
url = f"http://{SERVER_IP}:5000/getView/true"
show_webview(url)
