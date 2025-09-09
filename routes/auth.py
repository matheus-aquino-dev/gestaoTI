from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime
from functools import wraps
import sqlite3
import jwt

auth_bp = Blueprint('auth', __name__)

def get_db():
    conn = sqlite3.connect('ativos_ti.db')
    conn.row_factory = sqlite3.Row
    return conn

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token ausente'}), 401
        try:
            token = token.split(' ')[1]  # Remove 'Bearer '
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = get_user_by_id(data['user_id'])
            if not current_user:
                return jsonify({'message': 'Token inválido'}), 401
            return f(current_user, *args, **kwargs)
        except:
            return jsonify({'message': 'Token inválido'}), 401
    return decorated

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not all(k in data for k in ['nome', 'email', 'senha', 'departamento']):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    # Verificar se o usuário já existe
    cursor.execute("SELECT id FROM usuarios WHERE email = ?", (data['email'],))
    if cursor.fetchone():
        db.close()
        return jsonify({'message': 'Email já cadastrado'}), 400
    
    hashed_pw = generate_password_hash(data['senha'])
    
    try:
        cursor.execute(
            "INSERT INTO usuarios (nome, email, departamento, password) VALUES (?, ?, ?, ?)",
            (data['nome'], data['email'], data['departamento'], hashed_pw)
        )
        db.commit()
        return jsonify({'message': 'Usuário registrado com sucesso'}), 201
    except Exception as e:
        db.rollback()
        return jsonify({'message': str(e)}), 500
    finally:
        db.close()

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not all(k in data for k in ['email', 'senha']):
        return jsonify({'message': 'Dados incompletos'}), 400
    
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute("SELECT * FROM usuarios WHERE email = ?", (data['email'],))
    user = cursor.fetchone()
    db.close()
    
    if user and check_password_hash(user['password'], data['senha']):
        token = jwt.encode({
            'user_id': user['id'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, app.config['SECRET_KEY'])
        
        return jsonify({
            'token': token,
            'user': {
                'id': user['id'],
                'nome': user['nome'],
                'email': user['email'],
                'departamento': user['departamento']
            }
        }), 200
    
    return jsonify({'message': 'Email ou senha inválidos'}), 401

def init_app(app):
    app.register_blueprint(auth_bp, url_prefix='/api/auth')