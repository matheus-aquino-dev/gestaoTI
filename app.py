from flask import Flask, send_from_directory
from flask_cors import CORS
from config.config import config
from config.database import init_db, close_db
from routes.auth import init_app as init_auth
from routes.api import init_app as init_api
import os

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='src', static_url_path='')
    app.config.from_object(config[config_name])
    
    # Permitir CORS em desenvolvimento
    if app.debug:
        CORS(app)
    
    # Inicializar banco de dados
    with app.app_context():
        init_db()
    app.teardown_appcontext(close_db)
    
    # Inicializar rotas
    init_auth(app)
    init_api(app)
    
    # Rota para servir arquivos estáticos
    @app.route('/<path:path>')
    def send_static(path):
        return send_from_directory('src', path)
    
    # Rota principal que sempre retorna index.html
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        return send_from_directory('src', 'index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=8080)