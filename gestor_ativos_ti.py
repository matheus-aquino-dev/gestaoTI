from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Função para criar o banco de dados e tabelas
def criar_banco():
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS categorias (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT NOT NULL UNIQUE
                 )''')add .
    c.execute('''CREATE TABLE IF NOT EXISTS ativos (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT NOT NULL,
                 descricao TEXT,
                 categoria_id INTEGER,
                 numero_serie TEXT UNIQUE,
                 data_aquisicao DATE,
                 status TEXT DEFAULT 'Disponivel',
                 localizacao TEXT,
                 FOREIGN KEY (categoria_id) REFERENCES categorias(id)
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nome TEXT NOT NULL,
                 departamento TEXT
                 )''')
    c.execute('''CREATE TABLE IF NOT EXISTS alocacoes (
                 id INTEGER PRIMARY KEY AUTOINCREMENT,
                 ativo_id INTEGER,
                 usuario_id INTEGER,
                 data_alocacao DATE,
                 data_devolucao DATE,
                 FOREIGN KEY (ativo_id) REFERENCES ativos(id),
                 FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
                 )''')
    conn.commit()
    conn.close()

# Funções de manipulação de dados
def adicionar_categoria(nome):
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO categorias (nome) VALUES (?)", (nome,))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def adicionar_ativo(nome, descricao, categoria_id, numero_serie, data_aquisicao, status='Disponivel', localizacao=''):
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    try:
        c.execute("INSERT INTO ativos (nome, descricao, categoria_id, numero_serie, data_aquisicao, status, localizacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
                  (nome, descricao, categoria_id, numero_serie, data_aquisicao, status, localizacao))
        conn.commit()
    except sqlite3.IntegrityError:
        pass
    conn.close()

def adicionar_usuario(nome, departamento):
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute("INSERT INTO usuarios (nome, departamento) VALUES (?, ?)", (nome, departamento))
    conn.commit()
    conn.close()

def alocar_ativo(ativo_id, usuario_id):
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    data_alocacao = datetime.now().date()
    c.execute("INSERT INTO alocacoes (ativo_id, usuario_id, data_alocacao) VALUES (?, ?, ?)", (ativo_id, usuario_id, data_alocacao))
    c.execute("UPDATE ativos SET status = 'Alocado' WHERE id = ?", (ativo_id,))
    conn.commit()
    conn.close()

def get_categorias():
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute("SELECT id, nome FROM categorias")
    categorias = c.fetchall()
    conn.close()
    return categorias

def get_ativos():
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute("SELECT ativos.id, ativos.nome, categorias.nome, ativos.numero_serie, ativos.status FROM ativos INNER JOIN categorias ON ativos.categoria_id = categorias.id")
    ativos = c.fetchall()
    conn.close()
    return ativos

def get_usuarios():
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute("SELECT id, nome FROM usuarios")
    usuarios = c.fetchall()
    conn.close()
    return usuarios

# Rotas do Flask
@app.route('/')
def index():
    criar_banco()
    ativos = get_ativos()
    return render_template('index.html', ativos=ativos)

@app.route('/adicionar_categoria', methods=['GET', 'POST'])
def adicionar_categoria_route():
    if request.method == 'POST':
        nome = request.form['nome']
        adicionar_categoria(nome)
        return redirect(url_for('index'))
    return render_template('adicionar_categoria.html')

@app.route('/adicionar_ativo', methods=['GET', 'POST'])
def adicionar_ativo_route():
    if request.method == 'POST':
        nome = request.form['nome']
        descricao = request.form['descricao']
        categoria_id = request.form['categoria_id']
        numero_serie = request.form['numero_serie']
        data_aquisicao = request.form['data_aquisicao']
        adicionar_ativo(nome, descricao, categoria_id, numero_serie, data_aquisicao)
        return redirect(url_for('index'))
    categorias = get_categorias()
    return render_template('adicionar_ativo.html', categorias=categorias)

@app.route('/adicionar_usuario', methods=['GET', 'POST'])
def adicionar_usuario_route():
    if request.method == 'POST':
        nome = request.form['nome']
        departamento = request.form['departamento']
        adicionar_usuario(nome, departamento)
        return redirect(url_for('index'))
    return render_template('adicionar_usuario.html')

@app.route('/alocar_ativo', methods=['GET', 'POST'])
def alocar_ativo_route():
    if request.method == 'POST':
        ativo_id = request.form['ativo_id']
        usuario_id = request.form['usuario_id']
        alocar_ativo(ativo_id, usuario_id)
        return redirect(url_for('index'))
    ativos = get_ativos()
    usuarios = get_usuarios()
    return render_template('alocar_ativo.html', ativos=ativos, usuarios=usuarios)

if __name__ == '__main__':
    app.run(debug=True)