"""Camada de serviços: casos de uso e regras de negócio do FluxBoard."""
import hashlib
import os
from datetime import datetime, timezone

from .db import get_connection, COLUNAS_PADRAO


def _agora():
    return datetime.now(timezone.utc).isoformat()


def _hash_senha(senha, salt=None):
    salt = salt or os.urandom(16).hex()
    h = hashlib.pbkdf2_hmac("sha256", senha.encode(), bytes.fromhex(salt), 100_000)
    return f"{salt}${h.hex()}"


def _verifica_senha(senha, senha_hash):
    try:
        salt, _ = senha_hash.split("$")
    except ValueError:
        return False
    return _hash_senha(senha, salt) == senha_hash


class RegraNegocioError(Exception):
    """Erro de violação de regra de negócio (ex.: limite de WIP excedido)."""


# ---------- US01/US02: contas e autenticação ----------
def criar_conta(nome, email, senha):
    conn = get_connection()
    try:
        cur = conn.execute(
            "INSERT INTO usuario (nome, email, senha_hash, criado_em) VALUES (?,?,?,?)",
            (nome, email, _hash_senha(senha), _agora()),
        )
        conn.commit()
        return cur.lastrowid
    except Exception:
        raise RegraNegocioError("E-mail já cadastrado.")
    finally:
        conn.close()


def autenticar(email, senha):
    conn = get_connection()
    row = conn.execute("SELECT * FROM usuario WHERE email = ?", (email,)).fetchone()
    conn.close()
    if row and _verifica_senha(senha, row["senha_hash"]):
        return dict(row)
    return None


# ---------- US03: projetos e participação ----------
def criar_projeto(nome, descricao, usuario_id):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO projeto (nome, descricao, criado_em) VALUES (?,?,?)",
        (nome, descricao, _agora()),
    )
    projeto_id = cur.lastrowid
    conn.execute(
        "INSERT INTO participacao (usuario_id, projeto_id, papel) VALUES (?,?,?)",
        (usuario_id, projeto_id, "lider"),
    )
    conn.commit()
    conn.close()
    return projeto_id


def projetos_do_usuario(usuario_id):
    conn = get_connection()
    rows = conn.execute(
        "SELECT p.* FROM projeto p JOIN participacao pa ON pa.projeto_id = p.id "
        "WHERE pa.usuario_id = ? ORDER BY p.id",
        (usuario_id,),
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def _usuario_participa(conn, usuario_id, projeto_id):
    r = conn.execute(
        "SELECT 1 FROM participacao WHERE usuario_id=? AND projeto_id=?",
        (usuario_id, projeto_id),
    ).fetchone()
    return r is not None


# ---------- US04: quadro (CRUD) ----------
def criar_quadro(projeto_id, nome):
    conn = get_connection()
    cur = conn.execute(
        "INSERT INTO quadro (projeto_id, nome, criado_em) VALUES (?,?,?)",
        (projeto_id, nome, _agora()),
    )
    quadro_id = cur.lastrowid
    for ordem, nome_col in enumerate(COLUNAS_PADRAO):
        conn.execute(
            "INSERT INTO coluna (quadro_id, nome, ordem, wip_limit) VALUES (?,?,?,0)",
            (quadro_id, nome_col, ordem),
        )
    conn.execute(
        "INSERT INTO raia (quadro_id, nome, ordem) VALUES (?,?,0)",
        (quadro_id, "Geral"),
    )
    conn.commit()
    conn.close()
    return quadro_id


def listar_quadros(projeto_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM quadro WHERE projeto_id=? ORDER BY id", (projeto_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def renomear_quadro(quadro_id, novo_nome):
    conn = get_connection()
    conn.execute("UPDATE quadro SET nome=? WHERE id=?", (novo_nome, quadro_id))
    conn.commit()
    conn.close()


def excluir_quadro(quadro_id):
    conn = get_connection()
    conn.execute("DELETE FROM movimentacao_cartao WHERE cartao_id IN "
                 "(SELECT id FROM cartao WHERE quadro_id=?)", (quadro_id,))
    conn.execute("DELETE FROM cartao WHERE quadro_id=?", (quadro_id,))
    conn.execute("DELETE FROM coluna WHERE quadro_id=?", (quadro_id,))
    conn.execute("DELETE FROM raia WHERE quadro_id=?", (quadro_id,))
    conn.execute("DELETE FROM quadro WHERE id=?", (quadro_id,))
    conn.commit()
    conn.close()


def colunas_do_quadro(quadro_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM coluna WHERE quadro_id=? ORDER BY ordem", (quadro_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


# ---------- US05: raia (CRUD) ----------
def criar_raia(quadro_id, nome):
    conn = get_connection()
    ordem = conn.execute("SELECT COALESCE(MAX(ordem),-1)+1 o FROM raia WHERE quadro_id=?",
                         (quadro_id,)).fetchone()["o"]
    cur = conn.execute("INSERT INTO raia (quadro_id, nome, ordem) VALUES (?,?,?)",
                       (quadro_id, nome, ordem))
    conn.commit()
    conn.close()
    return cur.lastrowid


def listar_raias(quadro_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM raia WHERE quadro_id=? ORDER BY ordem", (quadro_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def excluir_raia(raia_id):
    conn = get_connection()
    conn.execute("UPDATE cartao SET raia_id=NULL WHERE raia_id=?", (raia_id,))
    conn.execute("DELETE FROM raia WHERE id=?", (raia_id,))
    conn.commit()
    conn.close()


# ---------- US09: limite de WIP ----------
def definir_wip(coluna_id, limite):
    if limite < 0:
        raise RegraNegocioError("Limite de WIP não pode ser negativo.")
    conn = get_connection()
    conn.execute("UPDATE coluna SET wip_limit=? WHERE id=?", (limite, coluna_id))
    conn.commit()
    conn.close()


# ---------- US06: cartão (CRUD) ----------
def criar_cartao(quadro_id, nome, responsavel_id=None, data_limite=None,
                 prioridade="media", descricao="", raia_id=None):
    conn = get_connection()
    col = conn.execute("SELECT id FROM coluna WHERE quadro_id=? ORDER BY ordem LIMIT 1",
                       (quadro_id,)).fetchone()
    if raia_id is None:
        r = conn.execute("SELECT id FROM raia WHERE quadro_id=? ORDER BY ordem LIMIT 1",
                         (quadro_id,)).fetchone()
        raia_id = r["id"] if r else None
    cur = conn.execute(
        "INSERT INTO cartao (quadro_id, coluna_id, raia_id, nome, responsavel_id, "
        "data_limite, prioridade, descricao, criado_em) VALUES (?,?,?,?,?,?,?,?,?)",
        (quadro_id, col["id"], raia_id, nome, responsavel_id, data_limite,
         prioridade, descricao, _agora()),
    )
    cartao_id = cur.lastrowid
    conn.execute(
        "INSERT INTO movimentacao_cartao (cartao_id, coluna_origem, coluna_destino, movido_em) "
        "VALUES (?,?,?,?)",
        (cartao_id, None, col["id"], _agora()),
    )
    conn.commit()
    conn.close()
    return cartao_id


def listar_cartoes(quadro_id):
    conn = get_connection()
    rows = conn.execute("SELECT * FROM cartao WHERE quadro_id=? ORDER BY id", (quadro_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]


def atualizar_cartao(cartao_id, **campos):
    permitidos = {"nome", "responsavel_id", "data_limite", "prioridade", "descricao"}
    campos = {k: v for k, v in campos.items() if k in permitidos}
    if not campos:
        return
    conn = get_connection()
    sets = ", ".join(f"{k}=?" for k in campos)
    conn.execute(f"UPDATE cartao SET {sets} WHERE id=?", (*campos.values(), cartao_id))
    conn.commit()
    conn.close()


def excluir_cartao(cartao_id):
    conn = get_connection()
    conn.execute("DELETE FROM movimentacao_cartao WHERE cartao_id=?", (cartao_id,))
    conn.execute("DELETE FROM cartao WHERE id=?", (cartao_id,))
    conn.commit()
    conn.close()


# ---------- US07: mover cartão entre colunas (respeitando WIP) ----------
def mover_cartao_coluna(cartao_id, coluna_destino_id):
    conn = get_connection()
    cartao = conn.execute("SELECT * FROM cartao WHERE id=?", (cartao_id,)).fetchone()
    destino = conn.execute("SELECT * FROM coluna WHERE id=?", (coluna_destino_id,)).fetchone()
    if cartao is None or destino is None:
        conn.close()
        raise RegraNegocioError("Cartão ou coluna inexistente.")
    if destino["wip_limit"] and destino["wip_limit"] > 0:
        atual = conn.execute("SELECT COUNT(*) c FROM cartao WHERE coluna_id=?",
                             (coluna_destino_id,)).fetchone()["c"]
        if atual >= destino["wip_limit"]:
            conn.close()
            raise RegraNegocioError(
                f"Limite de WIP da coluna '{destino['nome']}' atingido ({destino['wip_limit']})."
            )
    origem = cartao["coluna_id"]
    conn.execute("UPDATE cartao SET coluna_id=? WHERE id=?", (coluna_destino_id, cartao_id))
    conn.execute(
        "INSERT INTO movimentacao_cartao (cartao_id, coluna_origem, coluna_destino, movido_em) "
        "VALUES (?,?,?,?)", (cartao_id, origem, coluna_destino_id, _agora()))
    conn.commit()
    conn.close()


# ---------- US08: mover cartão entre raias ----------
def mover_cartao_raia(cartao_id, raia_destino_id):
    conn = get_connection()
    cartao = conn.execute("SELECT * FROM cartao WHERE id=?", (cartao_id,)).fetchone()
    if cartao is None:
        conn.close()
        raise RegraNegocioError("Cartão inexistente.")
    origem = cartao["raia_id"]
    conn.execute("UPDATE cartao SET raia_id=? WHERE id=?", (raia_destino_id, cartao_id))
    conn.execute(
        "INSERT INTO movimentacao_cartao (cartao_id, raia_origem, raia_destino, movido_em) "
        "VALUES (?,?,?,?)", (cartao_id, origem, raia_destino_id, _agora()))
    conn.commit()
    conn.close()
