import sys,os

# Chemins vers les dossiers
RESOURCES_DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources'))
PLANS_DIR_PATH = "../../../resources/plans/"
PDF_DIR_PATH = "../../../resources/pdf/"
FONTS_DIR_PATH = "../../../resources/fonts/"

# Chemins vers les fichiers
AUDIO_FILE_PATH = "temp/audio.wav"
DB_FILE_PATH = "../../../resources/database/data.db"
QR_CODE_PATH = "../../../resources/qrcode/qrcode.png"

def get_ipv4():
    import netifaces
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if addr["addr"] != "127.0.0.1":  # Exclure localhost
                    return addr["addr"]
    return "127.0.0.1"

# Configuration serveur
SERVER_IP = get_ipv4()
PORT = 5000