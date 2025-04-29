import os

# Chemins vers les dossiers
RESOURCES_DIR_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources'))
PLANS_DIR_PATH = "../../../resources/plans/"
PDF_DIR_PATH = "../../../resources/pdf/"
AIDS_DIR_PATH = "../../../resources/aids/"

# Chemins vers les fichiers
AUDIO_FILE_PATH = "temp/audio.wav"
DB_FILE_PATH = "../../../resources/database/data.db"
QR_CODE_PATH = "../../../resources/qrcode/qrcode.png"
TEST_FILE_PATH = "../../../resources/test_data/inputs.txt"
TEST_OUTPUT_PATH = "../../../resources/test_data/out.txt"
LOG_FILE_PATH = "../../../resources/test_data/log_file.txt"


# Chemins vers les polices d'écriture
# ARIAL_FONT_PATH = os.path.abspath("../../../resources/fonts/Arial/arial.ttf")
# DEJA_VU_FONT_PATH = os.path.abspath("../../../resources/fonts/DejaVu/DejaVuSansCondensed.ttf")
# CONSOLAS_FONT_PATH = "../../../resources/fonts/Consolas/CONSOLA.TTF"
# SEGOE_UI_FONT_PATH = os.path.abspath("../../../resources/fonts/Segoe-UI/segoeuithis.ttf")
# ROBOTO_FONT_PATH = os.path.abspath("../../../resources/fonts/Roboto/static/Roboto-SemiBold.ttf")

# Fonts (Arial | DejaVu | Segoe_UI | Consolas | Roboto)
HUMAN_FONT = "Segoe_UI"
AI_FONT = "Consolas"

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