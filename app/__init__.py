# init.py file 
from flask import Flask
from dotenv import load_dotenv
import os

from .auth import auth_blueprint
from .routes import main

def create_app():
    load_dotenv()

    app = Flask(__name__)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SUPABASE_URL'] = os.getenv('SUPABASE_URL')
    app.config['SUPABASE_KEY'] = os.getenv('SUPABASE_KEY')

    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    app.register_blueprint(main)

    return app
