""" 
application.py
- Creates a Flask app instance
"""

from flask import Flask
from flask_cors import CORS


def create_app(app_name='LIGHTS_API'):
    app = Flask(app_name)
    app.config["DEBUG"] = True
    # Enable CORS
    CORS(app, resources={r'/*': {'origins': '*'}})

    return app
