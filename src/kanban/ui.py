"""Helpers de apresentação da TUI (somente biblioteca padrão)."""
import os
import sys

WIDTH = 66
_color = (sys.stdout.isatty() and os.environ.get("NO_COLOR") is None) \
    or os.environ.get("FORCE_COLOR") is not None


def _c(text, code):
    return f"\033[{code}m{text}\033[0m" if _color else text


def bold(t):   return _c(t, "1")
def dim(t):    return _c(t, "2")
def cyan(t):   return _c(t, "96")
def blue(t):   return _c(t, "94")
def green(t):  return _c(t, "92")
def yellow(t): return _c(t, "93")
def red(t):    return _c(t, "91")


def banner(title):
    line = "═" * WIDTH
    meio = title.upper().center(WIDTH)
    return cyan(bold(f"╔{line}╗\n║{meio}║\n╚{line}╝"))


def titulo(txt):
    return blue(bold(f"\n▌ {txt}"))


def prompt(msg="❯ "):
    return cyan(msg)


def ok(msg):  return green("✓ " + msg)
def erro(msg): return red("✗ " + msg)
def aviso(msg): return yellow("• " + msg)


def menu(itens):
    """itens: lista de (tecla, descrição). Retorna string formatada."""
    partes = [f"{cyan(bold(t))} {dim(d)}" for t, d in itens]
    return "  ".join(partes)


def render_board(colunas, raias, cartoes):
    """Desenha o quadro com colunas lado a lado em caixas."""
    COLW = 21

    def linha(cells):
        return "│" + "│".join(str(c).ljust(COLW)[:COLW] for c in cells) + "│"

    topo  = "┌" + "┬".join("─" * COLW for _ in colunas) + "┐"
    meio  = "├" + "┼".join("─" * COLW for _ in colunas) + "┤"
    base  = "└" + "┴".join("─" * COLW for _ in colunas) + "┘"

    grupos = list(raias) + [{"id": None, "nome": "(sem raia)"}]
    out = []
    for raia in grupos:
        no_grupo = [c for c in cartoes if c["raia_id"] == raia["id"]]
        if raia["id"] is None and not no_grupo:
            continue
        out.append(titulo(f"Raia: {raia['nome']}"))
        out.append(topo)
        headers, cols_cards = [], []
        for col in colunas:
            cc = [c for c in no_grupo if c["coluna_id"] == col["id"]]
            wip = f"/{col['wip_limit']}" if col["wip_limit"] else ""
            headers.append(f" {col['nome']} ({len(cc)}{wip})")
            cols_cards.append(cc)
        out.append(bold(linha(headers)))
        out.append(meio)
        maxn = max((len(cc) for cc in cols_cards), default=0)
        for i in range(max(maxn, 1)):
            cells = [f" #{cc[i]['id']} {cc[i]['nome']}" if i < len(cc) else ""
                     for cc in cols_cards]
            out.append(linha(cells))
        out.append(base)
    return "\n".join(out)
