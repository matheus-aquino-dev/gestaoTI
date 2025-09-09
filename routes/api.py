from flask import Blueprint, request, jsonify
from config.database import get_db
from datetime import datetime

api_bp = Blueprint('api', __name__)

@api_bp.route('/ativos', methods=['GET'])
def listar_ativos():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT a.*, cat.nome as categoria, cc.nome as centro_custo
        FROM ativos a
        LEFT JOIN categorias cat ON a.categoria_id = cat.id
        LEFT JOIN centros_custo cc ON a.centro_custo_id = cc.id
    """)
    ativos = cursor.fetchall()
    return jsonify([dict(ativo) for ativo in ativos])

@api_bp.route('/categorias', methods=['GET'])
def listar_categorias():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM categorias ORDER BY nome")
    categorias = cursor.fetchall()
    return jsonify([dict(cat) for cat in categorias])

@api_bp.route('/centros-custo', methods=['GET'])
def listar_centros_custo():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM centros_custo ORDER BY nome")
    centros = cursor.fetchall()
    return jsonify([dict(cc) for cc in centros])

@api_bp.route('/demandas', methods=['GET'])
def listar_demandas():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM demandas ORDER BY data_criacao DESC")
    demandas = cursor.fetchall()
    return jsonify([dict(demanda) for demanda in demandas])

@api_bp.route('/chips', methods=['GET'])
def listar_chips():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("""
        SELECT c.*, cc.nome as centro_custo
        FROM chips c
        LEFT JOIN centros_custo cc ON c.centro_custo_id = cc.id
    """)
    chips = cursor.fetchall()
    return jsonify([dict(chip) for chip in chips])

@api_bp.route('/notificacoes', methods=['GET'])
def listar_notificacoes():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM notificacoes WHERE lida = 0 ORDER BY data_criacao DESC")
    notificacoes = cursor.fetchall()
    return jsonify([dict(notif) for notif in notificacoes])

def init_app(app):
    app.register_blueprint(api_bp, url_prefix='/api')