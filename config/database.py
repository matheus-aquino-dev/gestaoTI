from flask import g
import sqlite3
from datetime import datetime

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('ativos_ti.db')
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    c = db.cursor()
    
    # Criação das tabelas
    c.execute('''CREATE TABLE IF NOT EXISTS centros_custo (
        id INTEGER PRIMARY KEY, 
        nome TEXT NOT NULL UNIQUE
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS categorias (
        id INTEGER PRIMARY KEY, 
        nome TEXT NOT NULL UNIQUE
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY, 
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        departamento TEXT,
        password TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS ativos (
        id INTEGER PRIMARY KEY,
        nome TEXT NOT NULL,
        descricao TEXT,
        categoria_id INTEGER,
        centro_custo_id INTEGER,
        modelo TEXT,
        valor REAL,
        numero_serie TEXT,
        data_aquisicao DATE,
        status TEXT DEFAULT 'Disponivel',
        patrimonio TEXT,
        numero_chip TEXT,
        imei1 TEXT,
        imei2 TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id),
        FOREIGN KEY (centro_custo_id) REFERENCES centros_custo(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS alocacoes (
        id INTEGER PRIMARY KEY,
        ativo_id INTEGER,
        funcionario_nome TEXT,
        data_alocacao DATE,
        FOREIGN KEY (ativo_id) REFERENCES ativos(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS historico_alocacoes (
        id INTEGER PRIMARY KEY,
        ativo_id INTEGER,
        funcionario_nome TEXT,
        data_alocacao DATE,
        data_devolucao DATE,
        FOREIGN KEY (ativo_id) REFERENCES ativos(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS chips (
        id INTEGER PRIMARY KEY,
        numero TEXT NOT NULL UNIQUE,
        funcionario_nome TEXT,
        centro_custo_id INTEGER,
        funcao TEXT,
        valor REAL,
        vencimento_fatura INTEGER,
        status TEXT DEFAULT 'Ativo',
        FOREIGN KEY (centro_custo_id) REFERENCES centros_custo(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS demandas (
        id INTEGER PRIMARY KEY,
        nome_solicitante TEXT NOT NULL,
        departamento TEXT,
        descricao TEXT NOT NULL,
        urgencia TEXT,
        data_criacao DATE,
        status TEXT DEFAULT 'Aberta',
        responsavel TEXT,
        data_conclusao DATE
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS demandas_historico (
        id INTEGER PRIMARY KEY,
        demanda_id INTEGER,
        alteracao TEXT NOT NULL,
        autor TEXT,
        data DATETIME,
        FOREIGN KEY (demanda_id) REFERENCES demandas(id)
    )''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS notificacoes (
        id INTEGER PRIMARY KEY,
        mensagem TEXT NOT NULL,
        link TEXT,
        data_criacao DATETIME,
        lida BOOLEAN DEFAULT 0
    )''')
    
    db.commit()