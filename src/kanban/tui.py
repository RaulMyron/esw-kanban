"""Interface de texto (TUI) do ParaFazer."""
from . import services as svc
from . import metrics
from . import ui
from .db import init_db, reset_db, DB_PATH


def _input(msg):
    return input(msg).strip()


def _menu(msg):
    return input(ui.prompt()).strip()


def tela_login():
    print(ui.banner("Para Fazer"))
    print(ui.menu([("1", "Entrar"), ("2", "Criar conta"),
                   ("9", "Apagar tudo"), ("0", "Sair")]))
    op = _menu("")
    if op == "2":
        nome = _input("Nome: ")
        email = _input("E-mail: ")
        senha = _input("Senha: ")
        try:
            svc.criar_conta(nome, email, senha)
            print(ui.ok("Conta criada. Faça login."))
        except svc.RegraNegocioError as e:
            print(ui.erro(str(e)))
        return None
    if op == "1":
        email = _input("E-mail: ")
        senha = _input("Senha: ")
        u = svc.autenticar(email, senha)
        if u:
            return u
        print(ui.erro("Credenciais inválidas."))
        return None
    if op == "9":
        if _input("Tem certeza? Isso apaga TUDO (digite SIM): ") == "SIM":
            reset_db()
            print(ui.ok("Banco zerado."))
        return None
    if op == "0":
        return "SAIR"
    return None


def tela_projetos(usuario):
    while True:
        print(ui.titulo(f"Projetos de {usuario['nome']}"))
        for p in svc.projetos_do_usuario(usuario["id"]):
            print(f"  {ui.cyan('[' + str(p['id']) + ']')} {p['nome']}")
        print(ui.menu([("nº", "abrir"), ("n", "novo projeto"), ("q", "sair da conta")]))
        op = _menu("")
        if op == "q":
            return
        if op == "n":
            svc.criar_projeto(_input("Nome do projeto: "), "", usuario["id"])
            continue
        if op.isdigit():
            tela_quadros(usuario, int(op))


def tela_quadros(usuario, projeto_id):
    while True:
        print(ui.titulo(f"Quadros do projeto {projeto_id}"))
        for q in svc.listar_quadros(projeto_id):
            print(f"  {ui.cyan('[' + str(q['id']) + ']')} {q['nome']}")
        membros = svc.participantes_do_projeto(projeto_id)
        print(ui.dim("  Membros: " + ", ".join(
            f"{m['nome']} ({m['papel']})" for m in membros)))
        print(ui.menu([("nº", "abrir"), ("n", "novo quadro"), ("a", "add membro"),
                       ("x", "excluir quadro"), ("v", "voltar")]))
        op = _menu("")
        if op == "v":
            return
        if op == "n":
            svc.criar_quadro(projeto_id, _input("Nome do quadro: "))
            continue
        if op == "a":
            email = _input("E-mail do membro: ")
            papel = _input("Papel (membro/lider) [membro]: ") or "membro"
            try:
                u = svc.adicionar_membro_por_email(projeto_id, email, papel)
                print(ui.ok(f"{u['nome']} adicionado ao projeto."))
            except svc.RegraNegocioError as e:
                print(ui.erro(str(e)))
            continue
        if op == "x":
            qid = _input("ID do quadro a excluir: ")
            if qid.isdigit():
                svc.excluir_quadro(int(qid))
            continue
        if op.isdigit():
            tela_quadro(usuario, int(op))


def desenhar_quadro(quadro_id):
    print(ui.render_board(svc.colunas_do_quadro(quadro_id),
                          svc.listar_raias(quadro_id),
                          svc.listar_cartoes(quadro_id)))


def _escolhe_coluna(quadro_id):
    for c in svc.colunas_do_quadro(quadro_id):
        print(f"   {ui.cyan('[' + str(c['id']) + ']')} {c['nome']}")
    cid = _input("ID da coluna: ")
    return int(cid) if cid.isdigit() else None


def _escolhe_raia(quadro_id):
    for r in svc.listar_raias(quadro_id):
        print(f"   {ui.cyan('[' + str(r['id']) + ']')} {r['nome']}")
    rid = _input("ID da raia: ")
    return int(rid) if rid.isdigit() else None


def tela_quadro(usuario, quadro_id):
    while True:
        desenhar_quadro(quadro_id)
        print(ui.menu([("c", "criar"), ("e", "editar"), ("d", "excluir"),
                       ("m", "mover coluna"), ("s", "mover raia")]))
        print(ui.menu([("r", "nova raia"), ("w", "definir WIP"),
                       ("x", "métricas"), ("v", "voltar")]))
        op = _menu("")
        try:
            if op == "v":
                return
            elif op == "c":
                nome = _input("Nome do cartão: ")
                prio = _input("Prioridade (baixa/media/alta): ") or "media"
                prazo = _input("Data limite (AAAA-MM-DD): ") or None
                desc = _input("Descrição: ")
                svc.criar_cartao(quadro_id, nome, responsavel_id=usuario["id"],
                                 data_limite=prazo, prioridade=prio, descricao=desc)
                print(ui.ok("Cartão criado."))
            elif op == "e":
                cid = _input("ID do cartão a editar: ")
                if not cid.isdigit():
                    continue
                print(ui.dim("(deixe em branco para manter o valor atual)"))
                campos = {}
                v = _input("Novo nome: ");        campos["nome"] = v or None
                v = _input("Nova prioridade: ");  campos["prioridade"] = v or None
                v = _input("Nova data limite: "); campos["data_limite"] = v or None
                v = _input("Nova descrição: ");   campos["descricao"] = v or None
                svc.atualizar_cartao(int(cid), **{k: val for k, val in campos.items() if val})
                print(ui.ok("Cartão atualizado."))
            elif op == "d":
                cid = _input("ID do cartão a excluir: ")
                if cid.isdigit():
                    svc.excluir_cartao(int(cid))
                    print(ui.ok("Cartão excluído."))
            elif op == "m":
                cid = _input("ID do cartão: ")
                destino = _escolhe_coluna(quadro_id)
                if cid.isdigit() and destino:
                    svc.mover_cartao_coluna(int(cid), destino)
                    print(ui.ok("Cartão movido de coluna."))
            elif op == "s":
                cid = _input("ID do cartão: ")
                destino = _escolhe_raia(quadro_id)
                if cid.isdigit() and destino:
                    svc.mover_cartao_raia(int(cid), destino)
                    print(ui.ok("Cartão movido de raia."))
            elif op == "r":
                svc.criar_raia(quadro_id, _input("Nome da raia: "))
            elif op == "w":
                for c in svc.colunas_do_quadro(quadro_id):
                    print(f"   {ui.cyan('[' + str(c['id']) + ']')} {c['nome']} (WIP={c['wip_limit']})")
                cid = _input("ID da coluna: ")
                lim = _input("Novo limite (0 = sem limite): ")
                if cid.isdigit() and lim.isdigit():
                    svc.definir_wip(int(cid), int(lim))
                    print(ui.ok("Limite de WIP definido."))
            elif op == "x":
                m = metrics.metricas_quadro(quadro_id)
                print(ui.titulo("Métricas"))
                print(f"  WIP atual ............. {ui.bold(str(m['wip']))}")
                print(f"  Throughput (24h) ...... {ui.bold(str(m['throughput_24h']))} cartões")
                print(f"  Lead time médio ....... {ui.bold(str(m['lead_time_medio_dias']))} dias")
                print(f"  Cycle time médio ...... {ui.bold(str(m['cycle_time_medio_dias']))} dias")
        except svc.RegraNegocioError as e:
            print(ui.erro(str(e)))
        except ValueError:
            print(ui.erro("Entrada inválida."))


def main():
    init_db()
    print(ui.dim(f"(dados salvos em: {DB_PATH})"))
    usuario = None
    while True:
        try:
            if usuario is None:
                r = tela_login()
                if r == "SAIR":
                    print("Até logo!")
                    return
                usuario = r if isinstance(r, dict) else None
            else:
                tela_projetos(usuario)
                usuario = None
        except svc.RegraNegocioError as e:
            print(ui.erro(str(e)))
        except ValueError:
            print(ui.erro("Entrada inválida."))