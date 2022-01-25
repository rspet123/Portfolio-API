from flask import Flask

app = Flask(__name__)

from . import flask_routes
