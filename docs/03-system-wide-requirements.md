# ParaFazer

## Especificação de Requisitos System-Wide (Requisitos Não-Funcionais)

### 1. Introdução

Este documento especifica os requisitos não-funcionais do ParaFazer, organizados segundo a
classificação **FURPS+** (usabilidade, confiabilidade, desempenho, suportabilidade e demais
requisitos de interface, restrições e conformidade). Complementa as histórias de usuário, que
tratam dos requisitos funcionais.

### 2. Requisitos Funcionais System-Wide

Requisitos funcionais que se aplicam a todo o sistema e não são expressos como histórias de
usuário:

- **Autenticação:** todo acesso aos serviços exige usuário autenticado por e-mail e senha.
- **Auditoria de fluxo:** toda movimentação de cartão entre colunas ou raias é registrada com
  data e hora, para fins de cálculo de métricas e rastreabilidade.
- **Autorização por projeto:** um usuário só acessa quadros e cartões de projetos dos quais
  participa.

### 3. Qualidades do Sistema

#### 3.1 Usabilidade

- A interface deve usar a terminologia do método Kanban (quadro, raia, cartão, WIP).
- Uma operação principal (criar/mover cartão) não deve exigir mais que três passos do usuário.
- Mensagens de erro devem ser claras e orientar a correção.

#### 3.2 Confiabilidade

- Nenhuma operação confirmada pode resultar em perda de dados; as escritas são transacionais.
- O sistema deve manter consistência entre cartões, colunas e raias mesmo após falha de
  energia (uso de transações no banco de dados).

#### 3.3 Desempenho

- Operações de CRUD e de movimentação devem responder em menos de 1 segundo para um quadro
  com até 500 cartões.
- O cálculo das métricas deve concluir em menos de 2 segundos no mesmo cenário.

#### 3.4 Suportabilidade

- O núcleo de domínio deve ser independente da interface, permitindo trocar a UI sem alterar a
  lógica de negócio.
- O código deve seguir um padrão de organização em camadas para facilitar manutenção e testes.
- A configuração de conexão com o banco deve ser externalizada (arquivo ou variável de ambiente).

### 4. Interfaces do Sistema

#### 4.1 Interface com o Usuário

- **Look & feel:** interface limpa, orientada ao quadro, com colunas dispostas lado a lado e
  cartões legíveis.
- **Layout e navegação:** área principal exibe o quadro; ações de cartão acessíveis a partir do
  próprio cartão; navegação entre projetos por menu.
- **Consistência:** mesmos rótulos e posições de ações em todas as telas.

#### 4.2 Interfaces com Sistemas e Dispositivos Externos

- **Interface de software:** acesso a um Sistema Gerenciador de Banco de Dados relacional
  (SQLite no protótipo; PostgreSQL em produção).
- **Interface de hardware:** não há requisitos especiais de hardware além de estação de
  trabalho padrão.
- **Interface de comunicação:** em produção, comunicação cliente-servidor sobre HTTPS.

### 5. Regras de Negócio

- **RN01 — Colunas fixas:** todo quadro deve conter exatamente as colunas A FAZER, FAZENDO e FEITO.
- **RN02 — Limite de WIP:** se uma coluna possui limite de WIP definido, não é permitido mover
  um cartão para ela quando o número de cartões já atingiu o limite.
- **RN03 — Campos obrigatórios do cartão:** identificador, nome, responsável, data limite,
  prioridade e descrição.
- **RN04 — Registro de movimentação:** toda movimentação de cartão registra origem, destino e
  instante, para cálculo de métricas.

### 6. Conformidade, Restrições e Documentação

- **Normas e padrões:** ISO/IEC 25010 (modelo de qualidade de produto de software) como
  referência para os atributos de qualidade; UML para os modelos de projeto.
- **Métricas:** definições de cycle time, lead time, throughput e WIP conforme o método Kanban.
- **Restrições de projeto:** arquitetura em camadas; persistência relacional; núcleo
  independente da interface.
- **Licenciamento:** software acadêmico; bibliotecas de terceiros, se usadas, devem ter licença
  permissiva (MIT, BSD ou Apache 2.0).
- **Documentação:** manual de instalação e de uso e documentação dos artefatos do processo.
