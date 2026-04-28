from flask import Flask
import os
from dotenv import load_dotenv

def create_app():
    load_dotenv()
    
    app = Flask(__name__)
    # 若環境變數未提供，則使用預設的金鑰 (僅供開發使用)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev_default_secret_key')

    # 註冊 Blueprints
    from app.routes.recipe import bp as recipe_bp
    app.register_blueprint(recipe_bp)

    return app
