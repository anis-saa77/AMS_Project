# Ajout du dossier python au chemin des modules
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

# Configuration serveur
def get_ipv4():
    import netifaces
    for interface in netifaces.interfaces():
        addrs = netifaces.ifaddresses(interface)
        if netifaces.AF_INET in addrs:
            for addr in addrs[netifaces.AF_INET]:
                if addr["addr"] != "127.0.0.1":  # Exclure localhost
                    return addr["addr"]
    return "127.0.0.1"

SERVER_IP = get_ipv4()
PORT = 5000

# Chemins vers les dossiers

# Chemins vers les fichiers
