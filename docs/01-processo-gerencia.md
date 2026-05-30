# FluxBoard

## Descrição do Processo de Gerenciamento do Projeto

### 1. Introdução

O gerenciamento deste trabalho adota o **método Kanban**, em coerência com o domínio do
sistema desenvolvido. O objetivo é visualizar o fluxo de trabalho, limitar o trabalho em
progresso e entregar os artefatos de forma incremental dentro do prazo. O quadro foi mantido
em uma ferramenta com suporte a colunas e cartões (GitHub Projects), com versionamento dos
artefatos no repositório Git.

### 2. Quadro Kanban

O quadro é composto por três colunas, conforme o fluxo do trabalho, e por uma raia (swimlane)
por integrante, de modo a tornar visível a responsabilidade de cada cartão.

| Coluna | Propósito |
| --- | --- |
| **A FAZER** | Cartões planejados e priorizados, ainda não iniciados. Representa o backlog comprometido para esta entrega. |
| **FAZENDO** | Cartões em execução. Limitado a no máximo 2 cartões por integrante (limite de WIP), para evitar dispersão e reduzir o *cycle time*. |
| **FEITO** | Cartões concluídos e revisados (ortografia, aderência ao template e aos critérios de avaliação). |

**Raias (swimlanes):** `Raul`, `Atila` e `Ambos` (cartões compartilhados).

### 3. Cartões

Cada cartão segue o padrão de informação exigido: identificador, nome, responsável, data
limite, prioridade e descrição.

| ID | Nome | Responsável | Data limite | Prioridade | Descrição |
| --- | --- | --- | --- | --- | --- |
| K01 | Setup do repositório e quadro Kanban | Ambos | Sáb 30/05 | Alta | Criar repositório Git, estrutura de pastas e quadro Kanban com colunas e raias. |
| K02 | Documento de Visão | Ambos | Sáb 30/05 | Alta | Elaborar o documento de visão e escopo do FluxBoard. |
| K03 | Histórias de usuário | Atila | Sáb 30/05 | Alta | Especificar os requisitos funcionais como histórias de usuário (Como/Eu quero/Para). |
| K04 | Requisitos não-funcionais | Raul | Sáb 30/05 | Alta | Especificar requisitos system-wide (qualidades, interfaces, normas, restrições). |
| K05 | Projeto físico do banco de dados | Atila | Dom 31/05 | Média | Diagrama e descrição textual das tabelas, chaves e relacionamentos. |
| K06 | Architecture Notebook | Raul | Dom 31/05 | Média | Documentar objetivos, decisões, mecanismos e visões da arquitetura. |
| K07 | Projeto de interface (storyboard + wireframes) | Atila | Dom 31/05 | Média | Storyboards com sequência de wireframes para os cenários principais. |
| K08 | Infraestrutura de implantação | Raul | Dom 31/05 | Média | Descrever hardware, software e serviços para produção. |
| K09 | Protótipo: núcleo, persistência e métricas | Raul | Dom 31/05 | Alta | Implementar domínio, persistência (SQLite) e cálculo das métricas. |
| K10 | Protótipo: interface e fluxos CRUD | Atila | Dom 31/05 | Alta | Implementar a interface e os fluxos de CRUD e movimentação de cartões. |
| K11 | Vídeo de teste de sistema | Atila | Dom/Seg | Alta | Gravar vídeo com um cenário de sucesso para cada serviço provido. |
| K12 | Descrição do processo de gerência | Ambos | Seg 01/06 | Média | Consolidar este documento com prints do quadro final. |
| K13 | Revisão, PDFs, ZIP e entrega | Ambos | Seg 01/06 | Alta | Revisar artefatos, exportar PDFs, montar e testar o ZIP, enviar no prazo. |

### 4. Métricas de fluxo acompanhadas

- **Work-in-progress (WIP):** número de cartões simultâneos em FAZENDO (limite = 2 por integrante).
- **Throughput:** cartões concluídos por dia.
- **Lead time:** tempo entre a entrada do cartão em A FAZER e a chegada em FEITO.
- **Cycle time:** tempo entre o início do trabalho (FAZENDO) e a conclusão (FEITO).

> **A inserir na entrega final:** capturas de tela do quadro Kanban no início e no fim do trabalho.
