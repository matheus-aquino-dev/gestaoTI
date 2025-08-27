import sqlite3
import csv
import json
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

# --- 1. CONFIGURAÇÃO DO APP E LOGIN ---
app = Flask(__name__)
app.secret_key = 'sua-chave-secreta-aqui'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin):
    def __init__(self, id, nome):
        self.id = id
        self.nome = nome

@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute("SELECT id, nome FROM usuarios WHERE id = ?", (user_id,))
    user_data = c.fetchone()
    conn.close()
    if user_data:
        return User(id=user_data[0], nome=user_data[1])
    return None

# --- 2. BANCO DE DADOS ---
def criar_banco():
    conn = sqlite3.connect('ativos_ti.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS centros_custo (id INTEGER PRIMARY KEY, nome TEXT NOT NULL UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS categorias (id INTEGER PRIMARY KEY, nome TEXT NOT NULL UNIQUE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, nome TEXT NOT NULL UNIQUE, departamento TEXT, password TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS ativos (
                 id INTEGER PRIMARY KEY, nome TEXT NOT NULL, descricao TEXT, categoria_id INTEGER, 
                 centro_custo_id INTEGER, modelo TEXT, valor REAL, numero_serie TEXT, 
                 data_aquisicao DATE, status TEXT DEFAULT 'Disponivel', patrimonio TEXT, 
                 numero_chip TEXT, imei1 TEXT, imei2 TEXT,
                 FOREIGN KEY (categoria_id) REFERENCES categorias(id),
                 FOREIGN KEY (centro_custo_id) REFERENCES centros_custo(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS alocacoes (id INTEGER PRIMARY KEY, ativo_id INTEGER, funcionario_nome TEXT, data_alocacao DATE,
                 FOREIGN KEY (ativo_id) REFERENCES ativos(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS historico_alocacoes (id INTEGER PRIMARY KEY, ativo_id INTEGER, funcionario_nome TEXT, data_alocacao DATE, data_devolucao DATE,
                 FOREIGN KEY (ativo_id) REFERENCES ativos(id))''')
    conn.commit()
    conn.close()

# --- 3. FUNÇÃO GENÉRICA DE CONSULTA AO BANCO ---
def db_query(query, params=(), fetchone=False, commit=False):
    conn = sqlite3.connect('ativos_ti.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    c.execute(query, params)
    result = c.fetchone() if fetchone else c.fetchall()
    if commit:
        conn.commit()
    conn.close()
    return result

# --- Rotas de Autenticação ---
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = db_query("SELECT * FROM usuarios WHERE nome = ?", (request.form['nome'],), fetchone=True)
        if user and check_password_hash(user['password'], request.form['password']):
            login_user(User(id=user['id'], nome=user['nome']))
            return redirect(url_for('index'))
        flash('Usuário ou senha inválidos.', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        nome = request.form['nome']
        if db_query("SELECT id FROM usuarios WHERE nome = ?", (nome,), fetchone=True):
            flash('Este nome de usuário já existe.', 'danger')
        else:
            hashed_pw = generate_password_hash(request.form['password'])
            db_query("INSERT INTO usuarios (nome, departamento, password) VALUES (?, ?, ?)",
                     (nome, request.form['departamento'], hashed_pw), commit=True)
            flash('Registro realizado com sucesso! Faça o login.', 'success')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# --- Rotas Principais ---
@app.route('/')
@login_required
def index():
    query = """
        SELECT a.id, a.nome, cat.nome as categoria, cc.nome as centro_custo, a.modelo, a.valor, a.status
        FROM ativos a 
        LEFT JOIN categorias cat ON a.categoria_id = cat.id
        LEFT JOIN centros_custo cc ON a.centro_custo_id = cc.id
    """
    return render_template('index.html', ativos=db_query(query))

# --- Rota de Download do CSV Modelo ---
@app.route('/download/modelo_csv')
@login_required
def download_modelo_csv():
    output = io.StringIO()
    # CORREÇÃO: Usar ponto e vírgula como delimitador
    writer = csv.writer(output, delimiter=';')
    
    header = [
        'Nome', 'Modelo', 'Categoria', 'Centro de Custo', 'Valor', 'DataAquisicao',
        'Patrimonio', 'NumeroSerie', 'Descricao', 'NumeroChip', 'IMEI1', 'IMEI2'
    ]
    writer.writerow(header)
    
    example_row = [
        'Notebook Exemplo', 'Inspiron 15', 'Notebooks', 'TI São Paulo', '4500,50', '2025-01-15',
        'PAT-00123', 'BRJ123XYZ', 'Notebook i5 com 8GB de RAM', '', '', ''
    ]
    writer.writerow(example_row)
    
    output.seek(0)
    
    return send_file(
        io.BytesIO(output.getvalue().encode('utf-8-sig')), # Usar utf-8-sig para melhor compatibilidade com Excel
        mimetype='text/csv',
        as_attachment=True,
        download_name='modelo_importacao.csv'
    )

# --- Rotas de Importação ---
@app.route('/importar', methods=['GET', 'POST'])
@login_required
def importar_csv():
    if request.method == 'POST':
        arquivo = request.files.get('arquivo')
        if not arquivo or arquivo.filename == '':
            flash('Nenhum ficheiro selecionado.', 'danger')
            return redirect(request.url)

        if not arquivo.filename.endswith('.csv'):
            flash('Formato de ficheiro inválido. Por favor, envie um .csv', 'danger')
            return redirect(request.url)

        try:
            stream = arquivo.stream.read().decode("utf-8")
            # Tenta detetar o delimitador
            delimiter = ';' if ';' in stream.splitlines()[0] else ','
            csv_data = csv.reader(stream.splitlines(), delimiter=delimiter)
            
            headers = next(csv_data)
            preview_data = [dict(zip(headers, row)) for row in csv_data]

            session['preview_data'] = json.dumps(preview_data)
            
            return render_template('preview_importacao.html', headers=headers, data=preview_data)

        except Exception as e:
            flash(f'Ocorreu um erro ao processar o ficheiro: {e}', 'danger')
            return redirect(request.url)

    return render_template('importar_csv.html')

@app.route('/importar/confirmar', methods=['POST'])
@login_required
def confirmar_importacao():
    preview_data_json = session.pop('preview_data', None)
    if not preview_data_json:
        flash('Nenhum dado para importar.', 'danger')
        return redirect(url_for('importar_csv'))

    data_to_import = json.loads(preview_data_json)
    
    try:
        for row in data_to_import:
            cat_nome = row.get('Categoria', '').strip()
            cc_nome = row.get('Centro de Custo', '').strip()

            if not cat_nome or not cc_nome: continue

            categoria = db_query("SELECT id FROM categorias WHERE nome = ?", (cat_nome,), fetchone=True)
            if not categoria:
                db_query("INSERT INTO categorias (nome) VALUES (?)", (cat_nome,), commit=True)
                categoria = db_query("SELECT id FROM categorias WHERE nome = ?", (cat_nome,), fetchone=True)
            
            cc = db_query("SELECT id FROM centros_custo WHERE nome = ?", (cc_nome,), fetchone=True)
            if not cc:
                db_query("INSERT INTO centros_custo (nome) VALUES (?)", (cc_nome,), commit=True)
                cc = db_query("SELECT id FROM centros_custo WHERE nome = ?", (cc_nome,), fetchone=True)
            
            # Substitui vírgula por ponto no valor
            valor_str = row.get('Valor', '').replace(',', '.')
            
            ativo_dados = {
                "nome": row.get('Nome'), "modelo": row.get('Modelo'), "categoria_id": categoria['id'],
                "centro_custo_id": cc['id'], "valor": valor_str or None,
                "data_aquisicao": row.get('DataAquisicao'), "patrimonio": row.get('Patrimonio'),
                "numero_serie": row.get('NumeroSerie'), "descricao": row.get('Descricao'),
                "numero_chip": row.get('NumeroChip'), "imei1": row.get('IMEI1'), "imei2": row.get('IMEI2'),
                "status": 'Disponivel'
            }
            
            ativo_dados_limpo = {k: v for k, v in ativo_dados.items() if v}
            colunas = ', '.join(ativo_dados_limpo.keys())
            placeholders = ', '.join(['?'] * len(ativo_dados_limpo))
            db_query(f"INSERT INTO ativos ({colunas}) VALUES ({placeholders})", list(ativo_dados_limpo.values()), commit=True)

        flash('Ativos importados com sucesso!', 'success')
    except Exception as e:
        flash(f'Ocorreu um erro na importação final: {e}', 'danger')

    return redirect(url_for('index'))

# --- Rotas de Ativos ---
@app.route('/ativo/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_ativo():
    if request.method == 'POST':
        dados = {k: v for k, v in request.form.to_dict().items() if v}
        dados['status'] = 'Disponivel'
        colunas = ', '.join(dados.keys())
        placeholders = ', '.join(['?'] * len(dados))
        db_query(f"INSERT INTO ativos ({colunas}) VALUES ({placeholders})", list(dados.values()), commit=True)
        return redirect(url_for('index'))
    return render_template('adicionar_ativo.html', 
                           categorias=db_query("SELECT * FROM categorias ORDER BY nome"), 
                           centros_custo=db_query("SELECT * FROM centros_custo ORDER BY nome"))

@app.route('/ativo/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ativo(id):
    if request.method == 'POST':
        dados = request.form.to_dict()
        set_clause = ', '.join([f"{key} = ?" for key in dados.keys()])
        db_query(f"UPDATE ativos SET {set_clause} WHERE id = ?", list(dados.values()) + [id], commit=True)
        return redirect(url_for('index'))
    return render_template('editar_ativo.html', 
                           ativo=db_query("SELECT * FROM ativos WHERE id = ?", (id,), fetchone=True),
                           categorias=db_query("SELECT * FROM categorias ORDER BY nome"), 
                           centros_custo=db_query("SELECT * FROM centros_custo ORDER BY nome"))

@app.route('/ativo/<int:id>/excluir')
@login_required
def excluir_ativo(id):
    db_query("DELETE FROM ativos WHERE id = ?", (id,), commit=True)
    return redirect(url_for('index'))

@app.route('/ativo/<int:id>/detalhes')
@login_required
def detalhes_ativo(id):
    ativo_query = "SELECT a.*, cat.nome as categoria, cc.nome as centro_custo FROM ativos a LEFT JOIN categorias cat ON a.categoria_id = cat.id LEFT JOIN centros_custo cc ON a.centro_custo_id = cc.id WHERE a.id = ?"
    historico_query = "SELECT * FROM historico_alocacoes WHERE ativo_id = ? ORDER BY data_alocacao DESC"
    return render_template('detalhes_ativo.html', 
                           ativo=db_query(ativo_query, (id,), fetchone=True),
                           historico=db_query(historico_query, (id,)))

# --- Rotas de Alocação ---
@app.route('/alocar', methods=['GET', 'POST'])
@login_required
def alocar_ativo():
    if request.method == 'POST':
        ativo_id = request.form['ativo_id']
        funcionario_nome = request.form['funcionario_nome']
        data = datetime.now().date()
        db_query("INSERT INTO alocacoes (ativo_id, funcionario_nome, data_alocacao) VALUES (?, ?, ?)", 
                 (ativo_id, funcionario_nome, data), commit=True)
        db_query("INSERT INTO historico_alocacoes (ativo_id, funcionario_nome, data_alocacao) VALUES (?, ?, ?)", 
                 (ativo_id, funcionario_nome, data), commit=True)
        db_query("UPDATE ativos SET status = 'Alocado' WHERE id = ?", (ativo_id,), commit=True)
        return redirect(url_for('index'))
    return render_template('alocar_ativo.html',
                           ativos=db_query("SELECT * FROM ativos WHERE status = 'Disponivel'"))

@app.route('/devolver', methods=['GET', 'POST'])
@login_required
def devolver_ativo():
    if request.method == 'POST':
        alocacao_id = request.form['alocacao_id']
        alocacao = db_query("SELECT ativo_id FROM alocacoes WHERE id = ?", (alocacao_id,), fetchone=True)
        db_query("UPDATE ativos SET status = 'Disponivel' WHERE id = ?", (alocacao['ativo_id'],), commit=True)
        db_query("UPDATE historico_alocacoes SET data_devolucao = ? WHERE ativo_id = ? AND data_devolucao IS NULL", 
                 (datetime.now().date(), alocacao['ativo_id']), commit=True)
        db_query("DELETE FROM alocacoes WHERE id = ?", (alocacao_id,), commit=True)
        return redirect(url_for('index'))
    alocacoes_query = "SELECT al.id, a.nome as ativo, al.funcionario_nome FROM alocacoes al JOIN ativos a ON al.ativo_id = a.id"
    return render_template('devolver_ativo.html', alocacoes=db_query(alocacoes_query))

# --- Rotas de Gerenciamento ---
# CENTROS DE CUSTO
@app.route('/centros_custo')
@login_required
def listar_centros_custo():
    return render_template('listar_generico.html', items=db_query("SELECT * FROM centros_custo ORDER BY nome"), titulo="Centros de Custo", endpoint_prefix="centros_custo")

@app.route('/centros_custo/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_centros_custo():
    if request.method == 'POST':
        db_query("INSERT INTO centros_custo (nome) VALUES (?)", (request.form['nome'],), commit=True)
        return redirect(url_for('listar_centros_custo'))
    return render_template('adicionar_editar_generico.html', titulo="Adicionar Centro de Custo", endpoint_prefix="centros_custo")

@app.route('/centros_custo/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_centros_custo(id):
    if request.method == 'POST':
        db_query("UPDATE centros_custo SET nome = ? WHERE id = ?", (request.form['nome'], id), commit=True)
        return redirect(url_for('listar_centros_custo'))
    return render_template('adicionar_editar_generico.html', item=db_query("SELECT * FROM centros_custo WHERE id = ?", (id,), fetchone=True), titulo="Editar Centro de Custo", endpoint_prefix="centros_custo")

@app.route('/centros_custo/<int:id>/excluir')
@login_required
def excluir_centros_custo(id):
    db_query("DELETE FROM centros_custo WHERE id = ?", (id,), commit=True)
    return redirect(url_for('listar_centros_custo'))

# CATEGORIAS
@app.route('/categorias')
@login_required
def listar_categorias():
    return render_template('listar_generico.html', items=db_query("SELECT * FROM categorias ORDER BY nome"), titulo="Categorias", endpoint_prefix="categorias")

@app.route('/categorias/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_categoria():
    if request.method == 'POST':
        db_query("INSERT INTO categorias (nome) VALUES (?)", (request.form['nome'],), commit=True)
        return redirect(url_for('listar_categorias'))
    return render_template('adicionar_editar_generico.html', titulo="Adicionar Categoria", endpoint_prefix="categorias")

@app.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    if request.method == 'POST':
        db_query("UPDATE categorias SET nome = ? WHERE id = ?", (request.form['nome'], id), commit=True)
        return redirect(url_for('listar_categorias'))
    return render_template('adicionar_editar_generico.html', item=db_query("SELECT * FROM categorias WHERE id = ?", (id,), fetchone=True), titulo="Editar Categoria", endpoint_prefix="categorias")

@app.route('/categorias/<int:id>/excluir')
@login_required
def excluir_categoria(id):
    db_query("DELETE FROM categorias WHERE id = ?", (id,), commit=True)
    return redirect(url_for('listar_categorias'))

# USUÁRIOS
@app.route('/usuarios')
@login_required
def listar_usuarios():
    return render_template('listar_usuarios.html', items=db_query("SELECT id, nome, departamento FROM usuarios"))

@app.route('/usuarios/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        if db_query("SELECT id FROM usuarios WHERE nome = ?", (nome,), fetchone=True):
            flash('Este nome de usuário já existe.', 'danger')
        else:
            hashed_pw = generate_password_hash("changeme")
            db_query("INSERT INTO usuarios (nome, departamento, password) VALUES (?, ?, ?)", (nome, request.form['departamento'], hashed_pw), commit=True)
            flash(f'Usuário {nome} criado com senha padrão "changeme".', 'success')
            return redirect(url_for('listar_usuarios'))
    return render_template('adicionar_usuario.html')

@app.route('/usuarios/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_usuario(id):
    if request.method == 'POST':
        db_query("UPDATE usuarios SET nome = ?, departamento = ? WHERE id = ?", (request.form['nome'], request.form['departamento'], id), commit=True)
        return redirect(url_for('listar_usuarios'))
    return render_template('editar_usuario.html', item=db_query("SELECT * FROM usuarios WHERE id=?", (id,), fetchone=True))

@app.route('/usuarios/<int:id>/excluir')
@login_required
def excluir_usuario(id):
    db_query("DELETE FROM usuarios WHERE id = ?", (id,), commit=True)
    return redirect(url_for('listar_usuarios'))

if __name__ == '__main__':
    criar_banco()
    app.run(debug=True)