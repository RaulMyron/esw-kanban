# ParaFazer — Sistema de Gestão de Projetos com método Kanban

Trabalho prático da disciplina de **Engenharia de Software**.

## Equipe

| Nome | Matrícula | Papel principal |
| --- | --- | --- |
| Raul Myron Silva Amorim | 200049712 | Arquitetura, requisitos não-funcionais, infraestrutura, back-end do protótipo |
| Atila Sousa Fernandes | 231013510 | Histórias de usuário, projeto de UI, projeto físico do BD, front-end do protótipo |

## O que é

ParaFazer é um sistema de software para gestão de projetos baseada no **método Kanban**.
Cada usuário cria conta, autentica-se e participa de um ou mais projetos. Em cada projeto há
quadros compostos pelas colunas **A FAZER**, **FAZENDO** e **FEITO**, organizados em raias
(swimlanes), com cartões de atividade, limite de WIP por coluna e cálculo das métricas
*cycle time*, *lead time*, *throughput* e *work-in-progress*.

## Processo de desenvolvimento

Processo Unificado (iterativo e incremental). A gestão deste próprio trabalho é feita por um
quadro Kanban — descrito em `docs/01-processo-gerencia.md`.

## Estrutura do repositório

```
docs/    Artefatos textuais (.md fonte + .pdf entregável)
src/     Protótipo (Python + SQLite)
infra/   Descrição da infraestrutura de implantação
video/   Vídeo do teste de sistema (link/arquivo)
```

## Como rodar o protótipo

```bash
cd src
python3 seed.py        # cria banco de demonstração (opcional)
python3 main.py        # inicia a interface de texto
```

Requer apenas Python 3.10+ (somente biblioteca padrão).

## Como gerar os PDFs a partir dos Markdown

```bash
./build_pdfs.sh
```

## Entrega

Arquivo final: `ESW-200049712-231013510.ZIP` (após inserir o vídeo em `video/`).
