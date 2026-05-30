"""Ponto de entrada do FluxBoard."""
from kanban.tui import main

if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\nEncerrado.")
