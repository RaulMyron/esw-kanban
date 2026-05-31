"""Cria um banco de demonstração com dados de exemplo (útil para o vídeo)."""
import os
from kanban.db import init_db, DB_PATH
from kanban import services as svc
from kanban import metrics


def seed():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    init_db()

    # US01: contas
    raul = svc.criar_conta("Raul", "raul@exemplo.com", "123456")
    atila = svc.criar_conta("Atila", "atila@exemplo.com", "123456")

    # US02: autenticação
    assert svc.autenticar("raul@exemplo.com", "123456")
    assert svc.autenticar("raul@exemplo.com", "errada") is None

    # US03: projeto
    proj = svc.criar_projeto("ParaFazer", "Trabalho de ESW", raul)

    # US04: quadro (cria A FAZER/FAZENDO/FEITO automaticamente)
    quadro = svc.criar_quadro(proj, "Quadro Principal")

    # US05: raia
    svc.criar_raia(quadro, "Backend")

    colunas = {c["nome"]: c["id"] for c in svc.colunas_do_quadro(quadro)}

    # US09: limite de WIP em FAZENDO
    svc.definir_wip(colunas["FAZENDO"], 2)

    # US06: cartões
    c1 = svc.criar_cartao(quadro, "Implementar login", responsavel_id=atila,
                          data_limite="2026-05-31", prioridade="alta", descricao="Tela e validacao")
    c2 = svc.criar_cartao(quadro, "Modelar banco", responsavel_id=raul,
                          prioridade="media", descricao="DDL das tabelas")
    c3 = svc.criar_cartao(quadro, "Escrever visao", responsavel_id=raul, prioridade="alta")

    # US07: mover cartões (gera histórico p/ métricas)
    svc.mover_cartao_coluna(c1, colunas["FAZENDO"])
    svc.mover_cartao_coluna(c1, colunas["FEITO"])
    svc.mover_cartao_coluna(c2, colunas["FAZENDO"])

    print("Banco de demonstração criado em:", DB_PATH)
    print("Métricas iniciais:", metrics.metricas_quadro(quadro))


if __name__ == "__main__":
    seed()
