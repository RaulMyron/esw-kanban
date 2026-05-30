"""US10: cálculo das métricas de fluxo (cycle time, lead time, throughput, WIP)."""
from datetime import datetime, timedelta, timezone

from .db import get_connection


def _parse(ts):
    return datetime.fromisoformat(ts)


def _id_coluna(conn, quadro_id, nome):
    r = conn.execute("SELECT id FROM coluna WHERE quadro_id=? AND nome=?", (quadro_id, nome)).fetchone()
    return r["id"] if r else None


def _instante_entrada(conn, cartao_id, coluna_id):
    r = conn.execute(
        "SELECT MIN(movido_em) m FROM movimentacao_cartao WHERE cartao_id=? AND coluna_destino=?",
        (cartao_id, coluna_id)).fetchone()
    return _parse(r["m"]) if r and r["m"] else None


def metricas_quadro(quadro_id):
    """Retorna dict com wip, throughput_hoje, lead_time_medio_dias, cycle_time_medio_dias."""
    conn = get_connection()
    id_afazer = _id_coluna(conn, quadro_id, "A FAZER")
    id_fazendo = _id_coluna(conn, quadro_id, "FAZENDO")
    id_feito = _id_coluna(conn, quadro_id, "FEITO")

    # WIP: cartões fora da coluna final
    wip = conn.execute(
        "SELECT COUNT(*) c FROM cartao WHERE quadro_id=? AND coluna_id != ?",
        (quadro_id, id_feito)).fetchone()["c"]

    # Throughput: cartões que chegaram a FEITO nas últimas 24h
    limite = (datetime.now(timezone.utc) - timedelta(days=1)).isoformat()
    throughput = conn.execute(
        "SELECT COUNT(DISTINCT cartao_id) c FROM movimentacao_cartao "
        "WHERE coluna_destino=? AND movido_em >= ?", (id_feito, limite)).fetchone()["c"]

    # Lead/cycle time dos cartões concluídos
    concluidos = conn.execute("SELECT id FROM cartao WHERE quadro_id=? AND coluna_id=?",
                              (quadro_id, id_feito)).fetchall()
    leads, cycles = [], []
    for row in concluidos:
        cid = row["id"]
        t_feito = _instante_entrada(conn, cid, id_feito)
        t_afazer = _instante_entrada(conn, cid, id_afazer)
        t_fazendo = _instante_entrada(conn, cid, id_fazendo)
        if t_feito and t_afazer:
            leads.append((t_feito - t_afazer).total_seconds())
        if t_feito and t_fazendo:
            cycles.append((t_feito - t_fazendo).total_seconds())
    conn.close()

    def media_dias(segundos):
        return round(sum(segundos) / len(segundos) / 86400, 2) if segundos else 0.0

    return {
        "wip": wip,
        "throughput_24h": throughput,
        "lead_time_medio_dias": media_dias(leads),
        "cycle_time_medio_dias": media_dias(cycles),
    }
