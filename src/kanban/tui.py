"""Interface de texto (TUI) do ParaFazer."""
from . import services as svc
from . import metrics
from .db import init_db


def _input(msg):
    return input(msg).strip()


def tela_login():
    print("\n=== ParaFazer ===")
    print("1) Entrar   2) Criar conta   0) Sair")
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
    if op == "0":
        return "SAIR"
    return None


def tela_projetos(usuario):
    while True:
        print(f"\n--- Projetos de {usuario['nome']} ---")
        projetos = svc.projetos_do_usuario(usuario["id"])
        for p in projetos:
            print(f"  [{p['id']}] {p['nome']}")
        print("n) Novo projeto   q) Sair da conta")
        op = _input("> ")
        if op == "q":
            return
        if op == "n":
            nome = _input("Nome do projeto: ")
            svc.criar_projeto(nome, "", usuario["id"])
            continue
        if op.isdigit():
            tela_quadros(usuario, int(op))


def tela_quadros(usuario, projeto_id):
    while True:
        quadros = svc.listar_quadros(projeto_id)
        print(f"\n--- Quadros do projeto {projeto_id} ---")
        for q in quadros:
            print(f"  [{q['id']}] {q['nome']}")
        print("n) Novo quadro   v) Voltar")
        op = _input("> ")
        if op == "v":
            return
        if op == "n":
            nome = _input("Nome do quadro: ")
            svc.criar_quadro(projeto_id, nome)
            continue
        if op.isdigit():
            tela_quadro(usuario, int(op))


def desenhar_quadro(quadro_id):
    colunas = svc.colunas_do_quadro(quadro_id)
    raias = svc.listar_raias(quadro_id)
    cartoes = svc.listar_cartoes(quadro_id)
    print("\n" + "=" * 60)
    for raia in raias:
        print(f"Raia: {raia['nome']}")
        for col in colunas:
            na_coluna = [c for c in cartoes if c["coluna_id"] == col["id"] and c["raia_id"] == raia["id"]]
            wip = f"/{col['wip_limit']}" if col["wip_limit"] else ""
            print(f"  {col['nome']} ({len(na_coluna)}{wip}): ", end="")
            print(", ".join(f"#{c['id']} {c['nome']}" for c in na_coluna) or "-")
    print("=" * 60)


def tela_quadro(usuario, quadro_id):
    while True:
        desenhar_quadro(quadro_id)
        print("c) Criar cartão   m) Mover cartão   r) Nova raia   "
              "w) Definir WIP   x) Métricas   v) Voltar")
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
        elif op == "m":
            cid = _input("ID do cartão: ")
            colunas = svc.colunas_do_quadro(quadro_id)
            for c in colunas:
                print(f"   [{c['id']}] {c['nome']}")
            destino = _input("ID da coluna destino: ")
            try:
                svc.mover_cartao_coluna(int(cid), int(destino))
            except svc.RegraNegocioError as e:
                print(f"[bloqueado] {e}")
        elif op == "r":
            svc.criar_raia(quadro_id, _input("Nome da raia: "))
        elif op == "w":
            colunas = svc.colunas_do_quadro(quadro_id)
            for c in colunas:
                print(f"   [{c['id']}] {c['nome']} (WIP={c['wip_limit']})")
            cid = _input("ID da coluna: ")
            lim = _input("Novo limite (0 = sem limite): ")
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
    usuario = None
    while True:
        if usuario is None:
            r = tela_login()
            if r == "SAIR":
                print("Ate logo!")
                return
            usuario = r if isinstance(r, dict) else None
        else:
            tela_projetos(usuario)
            usuario = None
