# ParaFazer

## Documento de Visão

### 1. Introdução

Este documento define a visão e o escopo do **ParaFazer**, um sistema de software para gestão
de projetos baseada no método Kanban. Descreve o problema a ser resolvido, as partes
interessadas, o ambiente dos usuários, as funcionalidades de alto nível e os requisitos de
qualidade que orientam o desenvolvimento.

### 2. Posicionamento

#### 2.1 Definição do Problema

| Item | Descrição |
| --- | --- |
| O problema de | falta de visibilidade do fluxo de trabalho e de controle do trabalho em progresso em equipes |
| afeta | membros de equipes de projeto, líderes e demais partes interessadas |
| cujo impacto é | gargalos não detectados, sobrecarga, atrasos e dificuldade de medir o desempenho do processo |
| uma solução de sucesso seria | uma ferramenta que torne o fluxo visível, limite o trabalho em progresso e calcule métricas objetivas de fluxo |

#### 2.2 Posicionamento do Produto

| Item | Descrição |
| --- | --- |
| Para | equipes que gerenciam trabalho de forma contínua e incremental |
| Que | precisam visualizar e controlar o fluxo de atividades |
| O ParaFazer | é um sistema de gestão de projetos baseado em Kanban |
| Que | torna o fluxo visível, impõe limites de WIP e mede cycle time, lead time, throughput e WIP |
| Diferentemente de | planilhas e listas de tarefas simples |
| Nosso produto | oferece quadros com raias, regras de fluxo e métricas calculadas automaticamente |

### 3. Descrição das Partes Interessadas

#### 3.1 Resumo das Partes Interessadas

| Nome | Descrição | Responsabilidades |
| --- | --- | --- |
| Membro de equipe | Usuário que executa as atividades | Criar e mover cartões, manter as informações atualizadas |
| Líder de projeto | Usuário responsável por organizar o trabalho | Definir quadros, raias e limites de WIP; acompanhar métricas |
| Parte interessada (stakeholder) | Pessoa interessada no andamento | Consultar o quadro e as métricas de fluxo |
| Equipe de desenvolvimento | Autores do sistema | Construir, validar e implantar o software |

#### 3.2 Ambiente do Usuário

Os usuários trabalham em equipes pequenas a médias e atuam de forma colaborativa. As tarefas
têm ciclos curtos e mudam de estado com frequência. O sistema é utilizado em desktop, com
possibilidade de interface textual ou gráfica, e deve permitir que vários usuários participem
de vários projetos simultaneamente. Integra-se a um banco de dados relacional para
persistência das informações.

### 4. Visão Geral do Produto

#### 4.1 Necessidades e Funcionalidades

| Necessidade | Prioridade | Funcionalidade | Versão planejada |
| --- | --- | --- | --- |
| Controlar o acesso | Alta | Criação de conta e autenticação de usuário | 1.0 |
| Participar de projetos | Alta | Associação de usuários a um ou mais projetos | 1.0 |
| Visualizar o fluxo | Alta | CRUD de quadros com colunas A FAZER, FAZENDO e FEITO | 1.0 |
| Organizar o trabalho | Alta | CRUD de raias (swimlanes) | 1.0 |
| Gerir atividades | Alta | CRUD de cartões de atividade | 1.0 |
| Movimentar o trabalho | Alta | Mover cartões entre colunas e entre raias | 1.0 |
| Limitar trabalho em progresso | Média | Definição de limite de WIP por coluna | 1.0 |
| Medir o processo | Média | Cálculo de cycle time, lead time, throughput e WIP | 1.0 |

### 5. Outros Requisitos do Produto

| Requisito | Prioridade | Versão planejada |
| --- | --- | --- |
| Persistência em banco de dados relacional | Alta | 1.0 |
| Senhas armazenadas de forma protegida (hash) | Alta | 1.0 |
| Tempo de resposta das operações inferior a 1 s em uso típico | Média | 1.0 |
| Portabilidade entre Windows e Linux | Média | 1.0 |
| Documentação de instalação e uso | Média | 1.0 |

### 6. Solução Proposta (resumo)

O ParaFazer é estruturado em camadas (apresentação, aplicação/serviços, domínio e
persistência). O núcleo de domínio é independente da interface, permitindo tanto uma interface
textual quanto gráfica. A persistência usa banco de dados relacional. As métricas são
calculadas a partir do histórico de movimentação dos cartões, registrado com data e hora.
