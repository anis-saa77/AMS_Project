import sys
import webview

def show_webview(image_url):
    """ Fonction pour afficher le webview avec une image donnée à une URL """

    if webview.active_window():
        update_webview(image_url)
    else :
        # Créer une fenêtre WebView
        window = webview.create_window("Image Viewer", image_url)
        webview.start()  # Démarre le processus de rendu de la fenêtre

def update_webview(image_url):
    """Met à jour l'URL dans la fenêtre WebView existante"""
    webview.load_url(image_url)

# Test
image_url = "http://192.168.81.33:5000/getImage/qrcode/qrcode.png"
#show_webview(image_url)