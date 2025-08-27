import csv
from flask import Flask, render_template, request, redirect, url_for # type: ignore
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
                 )''')
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
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute("SELECT categorias.nome, COUNT(ativos.id) AS total FROM ativos INNER JOIN categorias ON ativos.categoria_id = categorias.id GROUP BY categorias.nome")
    relatorio = c.fetchall()
    conn.close()
    categorias = [row[0] for row in relatorio] if relatorio else []
    totais = [row[1] for row in relatorio] if relatorio else []
    return render_template('index.html', ativos=ativos, categorias=categorias, totais=totais)

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

@app.route('/importar_csv', methods=['GET', 'POST'])
def importar_csv_route():
    if request.method == 'POST':
        arquivo = request.files['arquivo']
        if arquivo:
            arquivo.save('temp.csv')
            conn = sqlite3.connect('ativos_ti.db')
            c = conn.cursor()
            with open('temp.csv', 'r') as f:
                reader = csv.reader(f)
                next(reader)  # Pular header
                for row in reader:
                    nome, descricao, categoria_nome, numero_serie, data_aquisicao, status, localizacao = row
                    c.execute("SELECT id FROM categorias WHERE nome = ?", (categoria_nome,))
                    categoria_id = c.fetchone()
                    if categoria_id is None:
                        c.execute("INSERT INTO categorias (nome) VALUES (?)", (categoria_nome,))
                        categoria_id = c.lastrowid
                    else:
                        categoria_id = categoria_id[0]
                    try:
                        c.execute("INSERT INTO ativos (nome, descricao, categoria_id, numero_serie, data_aquisicao, status, localizacao) VALUES (?, ?, ?, ?, ?, ?, ?)",
                                (nome, descricao, categoria_id, numero_serie, data_aquisicao, status, localizacao))
                    except sqlite3.IntegrityError:
                        pass
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('importar_csv.html')

@app.route('/exportar_csv')
def exportar_csv_route():
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute("SELECT nome, descricao, categorias.nome, numero_serie, data_aquisicao, status, localizacao FROM ativos INNER JOIN categorias ON ativos.categoria_id = categorias.id")
    ativos = c.fetchall()
    conn.close()
    with open('exportados.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Nome', 'Descrição', 'Categoria', 'Número de Série', 'Data de Aquisição', 'Status', 'Localização'])
        writer.writerows(ativos)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)