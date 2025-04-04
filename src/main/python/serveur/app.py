from flask import Flask
from config_server import Configuration
import os

TEMPLATES_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'resources', 'templates'))

app = Flask(__name__, template_folder=TEMPLATES_PATH)

app.config.from_object(Configuration)
