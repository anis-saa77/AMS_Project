import sys
from PyQt5.QtCore import QUrl
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineProfile

class WebViewWindow(QMainWindow):
    def __init__(self, image_url):
        super().__init__()

        self.setWindowTitle("Simulation WebView")
        self.setGeometry(100, 100, 800, 600)

        # Créer un widget pour afficher la WebView
        self.webview = QWebEngineView(self)

        # Charger l'URL de l'image
        self.webview.setUrl(QUrl(image_url))

        # Configuration de la fenêtre
        self.setCentralWidget(self.webview)

    def show(self):
        super().show()

def show_webview(image_url):
    app = QApplication(sys.argv)
    window = WebViewWindow(image_url)
    window.show()
    sys.exit(app.exec_())

# Test
image_url = "http://192.168.81.33:5000/getImage/qrcode/qrcode.png"
show_webview(image_url)
