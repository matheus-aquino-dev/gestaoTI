import sqlite3
import csv
import json
import io
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_file, jsonify
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
    c.execute('''CREATE TABLE IF NOT EXISTS chips (
                 id INTEGER PRIMARY KEY, numero TEXT NOT NULL UNIQUE, funcionario_nome TEXT, 
                 centro_custo_id INTEGER, funcao TEXT, valor REAL, vencimento_fatura INTEGER, status TEXT DEFAULT 'Ativo',
                 FOREIGN KEY (centro_custo_id) REFERENCES centros_custo(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS demandas (
                 id INTEGER PRIMARY KEY, nome_solicitante TEXT NOT NULL, departamento TEXT,
                 descricao TEXT NOT NULL, urgencia TEXT, data_criacao DATE, status TEXT DEFAULT 'Aberta',
                 responsavel TEXT, data_conclusao DATE)''')
    c.execute('''CREATE TABLE IF NOT EXISTS demandas_historico (
                 id INTEGER PRIMARY KEY, demanda_id INTEGER, alteracao TEXT NOT NULL, 
                 autor TEXT, data DATETIME,
                 FOREIGN KEY (demanda_id) REFERENCES demandas(id))''')
    c.execute('''CREATE TABLE IF NOT EXISTS notificacoes (
                 id INTEGER PRIMARY KEY, mensagem TEXT NOT NULL, link TEXT, 
                 data_criacao DATETIME, lida BOOLEAN DEFAULT 0)''')
    conn.commit()
    # Migração leve: garantir colunas esperadas na tabela 'chips' para bases antigas
    try:
        c.execute("PRAGMA table_info(chips)")
        existing_cols = {row[1] for row in c.fetchall()}
        migrations = [
            ("funcionario_nome", "TEXT"),
            ("centro_custo_id", "INTEGER"),
            ("funcao", "TEXT"),
            ("valor", "REAL"),
            ("vencimento_fatura", "INTEGER"),
            ("status", "TEXT DEFAULT 'Ativo'"),
        ]
        for col_name, col_type in migrations:
            if col_name not in existing_cols:
                c.execute(f"ALTER TABLE chips ADD COLUMN {col_name} {col_type}")
        conn.commit()
    except Exception:
        # Evitar falhar inicialização caso PRAGMA/ALTER tenha algum problema
        pass
    # Migração leve: garantir colunas esperadas na tabela 'demandas' para bases antigas
    try:
        c.execute("PRAGMA table_info(demandas)")
        existing_cols_dem = {row[1] for row in c.fetchall()}
        demand_migrations = [
            ("nome_solicitante", "TEXT NOT NULL"),
            ("departamento", "TEXT"),
            ("descricao", "TEXT NOT NULL"),
            ("urgencia", "TEXT"),
            ("data_criacao", "DATE"),
            ("status", "TEXT DEFAULT 'Aberta'"),
            ("responsavel", "TEXT"),
            ("data_conclusao", "DATE"),
        ]
        for col_name, col_type in demand_migrations:
            if col_name not in existing_cols_dem:
                c.execute(f"ALTER TABLE demandas ADD COLUMN {col_name} {col_type}")
        conn.commit()
    except Exception:
        pass
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

# --- FUNÇÃO PARA CRIAR NOTIFICAÇÕES ---
def criar_notificacao(mensagem, link=None):
    db_query("INSERT INTO notificacoes (mensagem, link, data_criacao) VALUES (?, ?, ?)",
             (mensagem, link, datetime.now()), commit=True)

# --- FUNÇÃO PARA REGISTAR HISTÓRICO DE DEMANDA ---
def registar_historico_demanda(demanda_id, alteracao, autor):
    db_query("INSERT INTO demandas_historico (demanda_id, alteracao, autor, data) VALUES (?, ?, ?, ?)",
             (demanda_id, alteracao, autor, datetime.now()), commit=True)

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
        SELECT a.id, a.nome, cat.nome as categoria, cc.nome as centro_custo, 
               a.modelo, a.valor, a.status, al.funcionario_nome
        FROM ativos a 
        LEFT JOIN categorias cat ON a.categoria_id = cat.id
        LEFT JOIN centros_custo cc ON a.centro_custo_id = cc.id
        LEFT JOIN alocacoes al ON a.id = al.ativo_id
    """
    notificacoes_recentes = db_query("SELECT * FROM notificacoes ORDER BY data_criacao DESC LIMIT 3")
    categorias = db_query("SELECT * FROM categorias ORDER BY nome")
    return render_template('index.html', ativos=db_query(query), notificacoes_recentes=notificacoes_recentes, categorias=categorias)

# --- ROTAS DE DEMANDAS ---
@app.route('/nova_demanda')
def nova_demanda():
    return render_template('nova_demanda.html')

@app.route('/enviar_demanda', methods=['POST'])
def enviar_demanda():
    dados = { 'nome_solicitante': request.form['nome'], 'departamento': request.form['departamento'], 'descricao': request.form['descricao'], 'urgencia': request.form['urgencia'], 'data_criacao': datetime.now().date(), 'status': 'Aberta' }
    colunas = ', '.join(dados.keys())
    placeholders = ', '.join(['?'] * len(dados))
    db_query(f"INSERT INTO demandas ({colunas}) VALUES ({placeholders})", list(dados.values()), commit=True)
    demanda_id = db_query("SELECT last_insert_rowid() as id", fetchone=True)['id']
    registar_historico_demanda(demanda_id, "Demanda criada.", dados['nome_solicitante'])
    criar_notificacao(f"Nova demanda de {dados['nome_solicitante']} (Urgência: {dados['urgencia']})", url_for('detalhes_demanda', id=demanda_id))
    flash('Demanda enviada com sucesso!', 'success')
    return redirect(url_for('nova_demanda'))

@app.route('/demandas')
@login_required
def listar_demandas():
    demandas_abertas = db_query("SELECT * FROM demandas WHERE status = 'Aberta' ORDER BY data_criacao DESC")
    demandas_andamento = db_query("SELECT * FROM demandas WHERE status = 'Em Andamento' ORDER BY data_criacao DESC")
    demandas_concluidas = db_query("SELECT * FROM demandas WHERE status = 'Concluída' ORDER BY data_conclusao DESC LIMIT 10")
    return render_template('listar_demandas.html', abertas=demandas_abertas, andamento=demandas_andamento, concluidas=demandas_concluidas)

@app.route('/demandas/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_demanda():
    if request.method == 'POST':
        dados = { 'nome_solicitante': request.form['nome_solicitante'], 'departamento': request.form['departamento'], 'descricao': request.form['descricao'], 'urgencia': request.form['urgencia'], 'data_criacao': datetime.now().date(), 'status': 'Aberta' }
        colunas = ', '.join(dados.keys())
        placeholders = ', '.join(['?'] * len(dados))
        db_query(f"INSERT INTO demandas ({colunas}) VALUES ({placeholders})", list(dados.values()), commit=True)
        demanda_id = db_query("SELECT last_insert_rowid() as id", fetchone=True)['id']
        registar_historico_demanda(demanda_id, "Demanda criada pela equipa de TI.", current_user.nome)
        criar_notificacao(f"Nova demanda interna criada por {current_user.nome}", url_for('detalhes_demanda', id=demanda_id))
        flash('Demanda adicionada com sucesso!', 'success')
        return redirect(url_for('listar_demandas'))
    return render_template('adicionar_demanda.html')

@app.route('/demandas/<int:id>')
@login_required
def detalhes_demanda(id):
    demanda = db_query("SELECT * FROM demandas WHERE id = ?", (id,), fetchone=True)
    historico = db_query("SELECT * FROM demandas_historico WHERE demanda_id = ? ORDER BY data ASC", (id,))
    return render_template('detalhes_demanda.html', demanda=demanda, historico=historico)

@app.route('/demandas/<int:id>/atualizar', methods=['GET', 'POST'])
@login_required
def atualizar_demanda(id):
    if request.method == 'GET':
        return redirect(url_for('detalhes_demanda', id=id))
    novo_status = request.form.get('status')
    if not novo_status:
        flash('Nenhum status informado para atualização.', 'danger')
        return redirect(url_for('detalhes_demanda', id=id))
    demanda = db_query("SELECT * FROM demandas WHERE id = ?", (id,), fetchone=True)
    if novo_status == 'Em Andamento':
        db_query("UPDATE demandas SET status = ?, responsavel = ? WHERE id = ?", (novo_status, current_user.nome, id), commit=True)
        registar_historico_demanda(id, f"Status alterado para 'Em Andamento'. {current_user.nome} assumiu a responsabilidade.", current_user.nome)
    elif novo_status == 'Concluída':
        db_query("UPDATE demandas SET status = ?, data_conclusao = ? WHERE id = ?", (novo_status, datetime.now().date(), id), commit=True)
        registar_historico_demanda(id, "Status alterado para 'Concluída'.", current_user.nome)
        criar_notificacao(f"Demanda #{id} para {demanda['nome_solicitante']} foi concluída.", url_for('detalhes_demanda', id=id))
    flash('Status da demanda atualizado.', 'success')
    return redirect(url_for('detalhes_demanda', id=id))

# --- ROTAS DE NOTIFICAÇÕES ---
@app.route('/notificacoes/json')
@login_required
def notificacoes_json():
    notificacoes = db_query("SELECT * FROM notificacoes WHERE lida = 0 ORDER BY data_criacao DESC")
    return jsonify([dict(ix) for ix in notificacoes])

@app.route('/notificacoes')
@login_required
def listar_notificacoes():
    db_query("UPDATE notificacoes SET lida = 1", commit=True)
    return render_template('notificacoes.html', notificacoes=db_query("SELECT * FROM notificacoes ORDER BY data_criacao DESC"))
    
# --- Rota de Download do CSV Modelo ---
@app.route('/download/modelo_csv')
@login_required
def download_modelo_csv():
    output = io.StringIO()
    writer = csv.writer(output, delimiter=';')
    header = ['Nome', 'Modelo', 'Categoria', 'Centro de Custo', 'Valor', 'DataAquisicao', 'Patrimonio', 'NumeroSerie', 'Descricao', 'NumeroChip', 'IMEI1', 'IMEI2']
    writer.writerow(header)
    example_row = ['Notebook Exemplo', 'Inspiron 15', 'Notebooks', 'TI São Paulo', '4500,50', '2025-01-15', 'PAT-00123', 'BRJ123XYZ', 'Notebook i5 com 8GB de RAM', '', '', '']
    writer.writerow(example_row)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode('utf-8-sig')), mimetype='text/csv', as_attachment=True, download_name='modelo_importacao.csv')

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
            valor_str = row.get('Valor', '').replace(',', '.')
            ativo_dados = {
                "nome": row.get('Nome'), "modelo": row.get('Modelo'), "categoria_id": categoria['id'],
                "centro_custo_id": cc['id'], "valor": valor_str or None,
                "data_aquisicao": row.get('DataAquisicao'), "patrimonio": row.get('Patrimonio'),
                "numero_serie": row.get('NumeroSerie'), "descricao": row.get('Descricao'),
                "numero_chip": row.get('NumeroChip'), "imei1": row.get('IMEI1'), "imei2": row.get('IMEI2'), "status": 'Disponivel'
            }
            ativo_dados_limpo = {k: v for k, v in ativo_dados.items() if v}
            colunas = ', '.join(ativo_dados_limpo.keys())
            placeholders = ', '.join(['?'] * len(ativo_dados_limpo))
            db_query(f"INSERT INTO ativos ({colunas}) VALUES ({placeholders})", list(ativo_dados_limpo.values()), commit=True)
        criar_notificacao(f"{len(data_to_import)} ativos foram importados com sucesso.", url_for('index'))
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
        criar_notificacao(f"Novo ativo adicionado: {dados['nome']}", url_for('index'))
        return redirect(url_for('index'))
    return render_template('adicionar_ativo.html', categorias=db_query("SELECT * FROM categorias ORDER BY nome"), centros_custo=db_query("SELECT * FROM centros_custo ORDER BY nome"))

@app.route('/ativo/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_ativo(id):
    if request.method == 'POST':
        dados = request.form.to_dict()
        set_clause = ', '.join([f"{key} = ?" for key in dados.keys()])
        db_query(f"UPDATE ativos SET {set_clause} WHERE id = ?", list(dados.values()) + [id], commit=True)
        criar_notificacao(f"Ativo '{dados['nome']}' foi atualizado.", url_for('detalhes_ativo', id=id))
        return redirect(url_for('index'))
    return render_template('editar_ativo.html', ativo=db_query("SELECT * FROM ativos WHERE id = ?", (id,), fetchone=True), categorias=db_query("SELECT * FROM categorias ORDER BY nome"), centros_custo=db_query("SELECT * FROM centros_custo ORDER BY nome"))

@app.route('/ativo/<int:id>')
@login_required
def detalhes_ativo(id):
    ativo = db_query(
        """
        SELECT a.*, cat.nome as categoria, cc.nome as centro_custo
        FROM ativos a
        LEFT JOIN categorias cat ON a.categoria_id = cat.id
        LEFT JOIN centros_custo cc ON a.centro_custo_id = cc.id
        WHERE a.id = ?
        """,
        (id,),
        fetchone=True,
    )
    historico = db_query(
        "SELECT * FROM historico_alocacoes WHERE ativo_id = ? ORDER BY data_alocacao DESC",
        (id,),
    )
    alocacao = db_query(
        "SELECT * FROM alocacoes WHERE ativo_id = ?",
        (id,),
        fetchone=True,
    )
    return render_template('detalhes_ativo.html', ativo=ativo, historico=historico, alocacao=alocacao)

@app.route('/ativo/<int:id>/excluir')
@login_required
def excluir_ativo(id):
    ativo = db_query("SELECT nome FROM ativos WHERE id = ?", (id,), fetchone=True)
    db_query("DELETE FROM ativos WHERE id = ?", (id,), commit=True)
    criar_notificacao(f"Ativo '{ativo['nome']}' foi excluído.")
    return redirect(url_for('index'))

# --- Rotas de Alocação ---
@app.route('/alocar', methods=['GET', 'POST'])
@login_required
def alocar_ativo():
    if request.method == 'POST':
        ativo_id = request.form['ativo_id']
        funcionario_nome = request.form['funcionario_nome']
        data = datetime.now().date()
        db_query("INSERT INTO alocacoes (ativo_id, funcionario_nome, data_alocacao) VALUES (?, ?, ?)", (ativo_id, funcionario_nome, data), commit=True)
        db_query("INSERT INTO historico_alocacoes (ativo_id, funcionario_nome, data_alocacao) VALUES (?, ?, ?)", (ativo_id, funcionario_nome, data), commit=True)
        db_query("UPDATE ativos SET status = 'Alocado' WHERE id = ?", (ativo_id,), commit=True)
        ativo = db_query("SELECT nome FROM ativos WHERE id = ?", (ativo_id,), fetchone=True)
        criar_notificacao(f"Ativo '{ativo['nome']}' alocado para {funcionario_nome}.", url_for('detalhes_ativo', id=ativo_id))
        return redirect(url_for('index'))
    return render_template('alocar_ativo.html', ativos=db_query("SELECT * FROM ativos WHERE status = 'Disponivel'"))

@app.route('/devolver', methods=['GET', 'POST'])
@login_required
def devolver_ativo():
    if request.method == 'POST':
        alocacao_id = request.form['alocacao_id']
        alocacao = db_query("SELECT ativo_id, funcionario_nome FROM alocacoes WHERE id = ?", (alocacao_id,), fetchone=True)
        ativo = db_query("SELECT nome FROM ativos WHERE id = ?", (alocacao['ativo_id'],), fetchone=True)
        db_query("UPDATE ativos SET status = 'Disponivel' WHERE id = ?", (alocacao['ativo_id'],), commit=True)
        db_query("UPDATE historico_alocacoes SET data_devolucao = ? WHERE ativo_id = ? AND data_devolucao IS NULL", (datetime.now().date(), alocacao['ativo_id']), commit=True)
        db_query("DELETE FROM alocacoes WHERE id = ?", (alocacao_id,), commit=True)
        criar_notificacao(f"Ativo '{ativo['nome']}' foi devolvido por {alocacao['funcionario_nome']}.", url_for('detalhes_ativo', id=alocacao['ativo_id']))
        return redirect(url_for('index'))
    alocacoes_query = "SELECT al.id, a.nome as ativo, al.funcionario_nome FROM alocacoes al JOIN ativos a ON al.ativo_id = a.id"
    return render_template('devolver_ativo.html', alocacoes=db_query(alocacoes_query))

# --- Rotas de Gestão de Chips ---
@app.route('/chips')
@login_required
def listar_chips():
    query = "SELECT c.id, c.numero, c.funcionario_nome, cc.nome as centro_custo, c.funcao, c.valor, c.vencimento_fatura, c.status FROM chips c LEFT JOIN centros_custo cc ON c.centro_custo_id = cc.id ORDER BY c.numero"
    return render_template('listar_chips.html', chips=db_query(query))

@app.route('/chips/adicionar', methods=['GET', 'POST'])
@login_required
def adicionar_chip():
    if request.method == 'POST':
        dados = {k: v for k, v in request.form.to_dict().items() if v}
        colunas = ', '.join(dados.keys())
        placeholders = ', '.join(['?'] * len(dados))
        db_query(f"INSERT INTO chips ({colunas}) VALUES ({placeholders})", list(dados.values()), commit=True)
        criar_notificacao(f"Novo chip adicionado: {dados['numero']}", url_for('listar_chips'))
        flash('Chip adicionado com sucesso!', 'success')
        return redirect(url_for('listar_chips'))
    return render_template('adicionar_editar_chip.html', titulo="Adicionar Chip", centros_custo=db_query("SELECT id, nome FROM centros_custo ORDER BY nome"))

@app.route('/chips/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_chip(id):
    if request.method == 'POST':
        dados = request.form.to_dict()
        set_clause = ', '.join([f"{key} = ?" for key in dados.keys()])
        db_query(f"UPDATE chips SET {set_clause} WHERE id = ?", list(dados.values()) + [id], commit=True)
        criar_notificacao(f"Chip {dados['numero']} foi atualizado.", url_for('listar_chips'))
        flash('Chip atualizado com sucesso!', 'success')
        return redirect(url_for('listar_chips'))
    return render_template('adicionar_editar_chip.html', titulo="Editar Chip", chip=db_query("SELECT * FROM chips WHERE id = ?", (id,), fetchone=True), centros_custo=db_query("SELECT id, nome FROM centros_custo ORDER BY nome"))

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
        nome = request.form['nome']
        db_query("INSERT INTO centros_custo (nome) VALUES (?)", (nome,), commit=True)
        criar_notificacao(f"Novo centro de custo criado: {nome}", url_for('listar_centros_custo'))
        return redirect(url_for('listar_centros_custo'))
    return render_template('adicionar_editar_generico.html', titulo="Adicionar Centro de Custo", endpoint_prefix="centros_custo")

@app.route('/centros_custo/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_centros_custo(id):
    if request.method == 'POST':
        nome = request.form['nome']
        db_query("UPDATE centros_custo SET nome = ? WHERE id = ?", (nome, id), commit=True)
        criar_notificacao(f"Centro de custo atualizado para: {nome}", url_for('listar_centros_custo'))
        return redirect(url_for('listar_centros_custo'))
    return render_template('adicionar_editar_generico.html', item=db_query("SELECT * FROM centros_custo WHERE id = ?", (id,), fetchone=True), titulo="Editar Centro de Custo", endpoint_prefix="centros_custo")

@app.route('/centros_custo/<int:id>/excluir')
@login_required
def excluir_centros_custo(id):
    item = db_query("SELECT nome FROM centros_custo WHERE id = ?", (id,), fetchone=True)
    db_query("DELETE FROM centros_custo WHERE id = ?", (id,), commit=True)
    criar_notificacao(f"Centro de custo '{item['nome']}' foi excluído.")
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
        nome = request.form['nome']
        db_query("INSERT INTO categorias (nome) VALUES (?)", (nome,), commit=True)
        criar_notificacao(f"Nova categoria criada: {nome}", url_for('listar_categorias'))
        return redirect(url_for('listar_categorias'))
    return render_template('adicionar_editar_generico.html', titulo="Adicionar Categoria", endpoint_prefix="categorias")

@app.route('/categorias/<int:id>/editar', methods=['GET', 'POST'])
@login_required
def editar_categoria(id):
    if request.method == 'POST':
        nome = request.form['nome']
        db_query("UPDATE categorias SET nome = ? WHERE id = ?", (nome, id), commit=True)
        criar_notificacao(f"Categoria atualizada para: {nome}", url_for('listar_categorias'))
        return redirect(url_for('listar_categorias'))
    return render_template('adicionar_editar_generico.html', item=db_query("SELECT * FROM categorias WHERE id = ?", (id,), fetchone=True), titulo="Editar Categoria", endpoint_prefix="categorias")

@app.route('/categorias/<int:id>/excluir')
@login_required
def excluir_categoria(id):
    item = db_query("SELECT nome FROM categorias WHERE id = ?", (id,), fetchone=True)
    db_query("DELETE FROM categorias WHERE id = ?", (id,), commit=True)
    criar_notificacao(f"Categoria '{item['nome']}' foi excluída.")
    return redirect(url_for('listar_categorias'))

# Alias de endpoints para compatibilidade com templates genéricos
app.add_url_rule('/categorias/adicionar', endpoint='adicionar_categorias', view_func=adicionar_categoria, methods=['GET', 'POST'])
app.add_url_rule('/categorias/<int:id>/editar', endpoint='editar_categorias', view_func=editar_categoria, methods=['GET', 'POST'])
app.add_url_rule('/categorias/<int:id>/excluir', endpoint='excluir_categorias', view_func=excluir_categoria)

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