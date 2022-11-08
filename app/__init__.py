from flask import Flask
from config import Config
from .api.routes import api
from .site.routes import site
from .authentication.routes import auth

app = Flask(__name__)

