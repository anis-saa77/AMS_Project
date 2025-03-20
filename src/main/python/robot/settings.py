# Chemins vers les fichiers
AUDIO_OUTPUT_PATH = "temp/output.wav"
TEMP_IMAGE_PATH = "temp/image.jpg"

# URL

def get_ipv4():
    import netifaces
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if addr["addr"] != "127.0.0.1":  # Exclure localhost
                    return addr["addr"]
    return "127.0.0.1"

# Configuration du serveur
SERVER_IP = get_ipv4()
PORT = 5000

ROBOT_URL = f"http://{SERVER_IP}:{PORT}/"
