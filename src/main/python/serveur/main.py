# Ajouter le dossier python au chemin des modules
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import *  # Do not delete !
from views import *   # Do not delete !
from app import app   # Do not delete !

if __name__ == '__main__':
    app.run(host='0.0.0.0', port="5000")