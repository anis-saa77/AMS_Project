from flask import Flask
from config_server import Configuration

app = Flask(__name__)

app.config.from_object(Configuration)
