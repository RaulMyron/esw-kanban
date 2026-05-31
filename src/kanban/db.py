"""Camada de persistência: conexão e criação do esquema (SQLite)."""
import sqlite3
import os

DB_PATH = os.path.abspath(os.environ.get(
    "PARAFAZER_DB",
    os.path.join(os.path.dirname(__file__), "..", "parafazer.db")))

SCHEMA = """
CREATE TABLE IF NOT EXISTS usuario (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    senha_hash TEXT NOT NULL,
    criado_em TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS projeto (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    descricao TEXT,
    criado_em TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS participacao (
    usuario_id INTEGER NOT NULL REFERENCES usuario(id),
    projeto_id INTEGER NOT NULL REFERENCES projeto(id),
    papel TEXT NOT NULL DEFAULT 'membro',
    PRIMARY KEY (usuario_id, projeto_id)
);
CREATE TABLE IF NOT EXISTS quadro (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    projeto_id INTEGER NOT NULL REFERENCES projeto(id),
    nome TEXT NOT NULL,
    criado_em TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS coluna (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER NOT NULL REFERENCES quadro(id),
    nome TEXT NOT NULL,
    ordem INTEGER NOT NULL,
    wip_limit INTEGER NOT NULL DEFAULT 0
);
CREATE TABLE IF NOT EXISTS raia (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER NOT NULL REFERENCES quadro(id),
    nome TEXT NOT NULL,
    ordem INTEGER NOT NULL
);
CREATE TABLE IF NOT EXISTS cartao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quadro_id INTEGER NOT NULL REFERENCES quadro(id),
    coluna_id INTEGER NOT NULL REFERENCES coluna(id),
    raia_id INTEGER REFERENCES raia(id),
    nome TEXT NOT NULL,
    responsavel_id INTEGER REFERENCES usuario(id),
    data_limite TEXT,
    prioridade TEXT NOT NULL DEFAULT 'media',
    descricao TEXT,
    criado_em TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS movimentacao_cartao (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cartao_id INTEGER NOT NULL REFERENCES cartao(id),
    coluna_origem INTEGER REFERENCES coluna(id),
    coluna_destino INTEGER REFERENCES coluna(id),
    raia_origem INTEGER REFERENCES raia(id),
    raia_destino INTEGER REFERENCES raia(id),
    movido_em TEXT NOT NULL
);
"""

COLUNAS_PADRAO = ["A FAZER", "FAZENDO", "FEITO"]


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db():
    conn = get_connection()
    conn.executescript(SCHEMA)
    conn.commit()
    conn.close()


def reset_db():
    """Apaga TODAS as tabelas e recria o esquema vazio."""
    conn = get_connection()
    for t in ["movimentacao_cartao", "cartao", "raia", "coluna",
              "quadro", "participacao", "projeto", "usuario"]:
        conn.execute(f"DROP TABLE IF EXISTS {t}")
    conn.commit()
    conn.close()
    init_db()