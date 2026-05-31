"""Interface de texto (TUI) do ParaFazer."""
import os
from . import services as svc
from . import metrics
from .db import init_db, reset_db, DB_PATH


def _input(msg):
    return input(msg).strip()


def tela_login():
    print("\n=== ParaFazer ===")
    print("1) Entrar   2) Criar conta   9) Apagar TODOS os dados   0) Sair")
    op = _input("> ")
    if op == "2":
        nome = _input("Nome: ")
        email = _input("E-mail: ")
        senha = _input("Senha: ")
        try:
            svc.criar_conta(nome, email, senha)
            print("Conta criada. Faça login.")
        except svc.RegraNegocioError as e:
            print(f"[erro] {e}")
        return None
    if op == "1":
        email = _input("E-mail: ")
        senha = _input("Senha: ")
        u = svc.autenticar(email, senha)
        if u:
            return u
        print("[erro] Credenciais inválidas.")
        return None
    if op == "9":
        if _input("Tem certeza? Isso apaga TUDO (digite SIM): ") == "SIM":
            reset_db()
            print("Banco zerado.")
        return None
    if op == "0":
        return "SAIR"
    return None


def tela_projetos(usuario):
    while True:
        print(f"\n--- Projetos de {usuario['nome']} ---")
        for p in svc.projetos_do_usuario(usuario["id"]):
            print(f"  [{p['id']}] {p['nome']}")
        print("n) Novo projeto   q) Sair da conta")
        op = _input("> ")
        if op == "q":
            return
        if op == "n":
            svc.criar_projeto(_input("Nome do projeto: "), "", usuario["id"])
            continue
        if op.isdigit():
            tela_quadros(usuario, int(op))


def tela_quadros(usuario, projeto_id):
    while True:
        print(f"\n--- Quadros do projeto {projeto_id} ---")
        for q in svc.listar_quadros(projeto_id):
            print(f"  [{q['id']}] {q['nome']}")
        print("n) Novo quadro   x) Excluir quadro   v) Voltar")
        op = _input("> ")
        if op == "v":
            return
        if op == "n":
            svc.criar_quadro(projeto_id, _input("Nome do quadro: "))
            continue
        if op == "x":
            qid = _input("ID do quadro a excluir: ")
            if qid.isdigit():
                svc.excluir_quadro(int(qid))
            continue
        if op.isdigit():
            tela_quadro(usuario, int(op))


def desenhar_quadro(quadro_id):
    colunas = svc.colunas_do_quadro(quadro_id)
    raias = svc.listar_raias(quadro_id)
    cartoes = svc.listar_cartoes(quadro_id)
    ids_raias = {r["id"] for r in raias}
    print("\n" + "=" * 64)
    grupos = list(raias) + [{"id": None, "nome": "(sem raia)"}]
    for raia in grupos:
        no_grupo = [c for c in cartoes if c["raia_id"] == raia["id"]]
        if raia["id"] is None and not no_grupo:
            continue
        print(f"Raia: {raia['nome']}")
        for col in colunas:
            na_coluna = [c for c in no_grupo if c["coluna_id"] == col["id"]]
            wip = f"/{col['wip_limit']}" if col["wip_limit"] else ""
            cards = ", ".join(f"#{c['id']} {c['nome']}" for c in na_coluna) or "-"
            print(f"  {col['nome']} ({len(na_coluna)}{wip}): {cards}")
    print("=" * 64)


def _escolhe_coluna(quadro_id):
    cols = svc.colunas_do_quadro(quadro_id)
    for c in cols:
        print(f"   [{c['id']}] {c['nome']}")
    cid = _input("ID da coluna: ")
    return int(cid) if cid.isdigit() else None


def _escolhe_raia(quadro_id):
    raias = svc.listar_raias(quadro_id)
    for r in raias:
        print(f"   [{r['id']}] {r['nome']}")
    rid = _input("ID da raia: ")
    return int(rid) if rid.isdigit() else None


def tela_quadro(usuario, quadro_id):
    while True:
        desenhar_quadro(quadro_id)
        print("c) Criar  e) Editar  d) Excluir cartão | "
              "m) Mover coluna  s) Mover raia")
        print("r) Nova raia  w) Definir WIP  x) Métricas  v) Voltar")
        op = _input("> ")
        if op == "v":
            return
        elif op == "c":
            nome = _input("Nome do cartão: ")
            prio = _input("Prioridade (baixa/media/alta): ") or "media"
            prazo = _input("Data limite (AAAA-MM-DD): ") or None
            desc = _input("Descrição: ")
            svc.criar_cartao(quadro_id, nome, responsavel_id=usuario["id"],
                             data_limite=prazo, prioridade=prio, descricao=desc)
        elif op == "e":
            cid = _input("ID do cartão a editar: ")
            if not cid.isdigit():
                continue
            print("(deixe em branco para manter o valor atual)")
            campos = {}
            v = _input("Novo nome: ");        campos["nome"] = v if v else None
            v = _input("Nova prioridade: ");  campos["prioridade"] = v if v else None
            v = _input("Nova data limite: "); campos["data_limite"] = v if v else None
            v = _input("Nova descrição: ");   campos["descricao"] = v if v else None
            campos = {k: val for k, val in campos.items() if val is not None}
            svc.atualizar_cartao(int(cid), **campos)
            print("Cartão atualizado.")
        elif op == "d":
            cid = _input("ID do cartão a excluir: ")
            if cid.isdigit():
                svc.excluir_cartao(int(cid))
                print("Cartão excluído.")
        elif op == "m":
            cid = _input("ID do cartão: ")
            destino = _escolhe_coluna(quadro_id)
            if cid.isdigit() and destino:
                try:
                    svc.mover_cartao_coluna(int(cid), destino)
                except svc.RegraNegocioError as e:
                    print(f"[bloqueado] {e}")
        elif op == "s":
            cid = _input("ID do cartão: ")
            destino = _escolhe_raia(quadro_id)
            if cid.isdigit() and destino:
                try:
                    svc.mover_cartao_raia(int(cid), destino)
                    print("Cartão movido de raia.")
                except svc.RegraNegocioError as e:
                    print(f"[erro] {e}")
        elif op == "r":
            svc.criar_raia(quadro_id, _input("Nome da raia: "))
        elif op == "w":
            cols = svc.colunas_do_quadro(quadro_id)
            for c in cols:
                print(f"   [{c['id']}] {c['nome']} (WIP={c['wip_limit']})")
            cid = _input("ID da coluna: ")
            lim = _input("Novo limite (0 = sem limite): ")
            if cid.isdigit() and lim.isdigit():
                try:
                    svc.definir_wip(int(cid), int(lim))
                except svc.RegraNegocioError as e:
                    print(f"[erro] {e}")
        elif op == "x":
            m = metrics.metricas_quadro(quadro_id)
            print(f"\n  WIP atual ............. {m['wip']}")
            print(f"  Throughput (24h) ...... {m['throughput_24h']} cartões")
            print(f"  Lead time medio ....... {m['lead_time_medio_dias']} dias")
            print(f"  Cycle time medio ...... {m['cycle_time_medio_dias']} dias")


def main():
    init_db()
    print(f"(dados salvos em: {DB_PATH})")
    usuario = None
    while True:
        try:
            if usuario is None:
                r = tela_login()
                if r == "SAIR":
                    print("Ate logo!")
                    return
                usuario = r if isinstance(r, dict) else None
            else:
                tela_projetos(usuario)
                usuario = None
        except svc.RegraNegocioError as e:
            print(f"[erro] {e}")
        except ValueError:
            print("[erro] entrada inválida.")