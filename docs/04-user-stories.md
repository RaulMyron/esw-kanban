# FluxBoard

## Especificação de Requisitos Funcionais — Histórias de Usuário

Cada requisito funcional é descrito como uma história de usuário, segundo a perspectiva do
usuário final e em linguagem informal, adotando o modelo **Como … Eu quero … Para …**, com
critérios de aceitação.

---

### US01 — Criar conta

**Como** visitante,
**Eu quero** criar uma conta com e-mail e senha,
**Para** poder acessar os serviços do sistema.

Critérios de aceitação:
- O e-mail deve ser único.
- A senha é armazenada de forma protegida (hash).
- Após o cadastro, o usuário consegue autenticar-se.

---

### US02 — Autenticar

**Como** usuário cadastrado,
**Eu quero** autenticar-me com e-mail e senha,
**Para** acessar meus projetos e quadros.

Critérios de aceitação:
- Credenciais corretas concedem acesso.
- Credenciais incorretas exibem mensagem de erro sem revelar qual campo falhou.

---

### US03 — Participar de projetos

**Como** usuário autenticado,
**Eu quero** participar de um ou mais projetos,
**Para** organizar trabalhos distintos separadamente.

Critérios de aceitação:
- Um usuário pode estar associado a vários projetos.
- O usuário só vê quadros e cartões dos projetos dos quais participa.

---

### US04 — Gerenciar quadro (CRUD)

**Como** usuário de um projeto,
**Eu quero** criar, visualizar, atualizar e excluir quadros,
**Para** representar diferentes fluxos de trabalho do projeto.

Critérios de aceitação:
- Ao criar um quadro, são geradas automaticamente as colunas A FAZER, FAZENDO e FEITO.
- A exclusão de um quadro remove suas colunas, raias e cartões.

---

### US05 — Gerenciar raia/swimlane (CRUD)

**Como** usuário de um projeto,
**Eu quero** criar, visualizar, atualizar e excluir raias em um quadro,
**Para** separar o trabalho por categoria, equipe ou responsável.

Critérios de aceitação:
- Uma raia pertence a um único quadro.
- Cartões podem ser associados a uma raia.

---

### US06 — Gerenciar cartão de atividade (CRUD)

**Como** usuário de um projeto,
**Eu quero** criar, visualizar, atualizar e excluir cartões de atividade,
**Para** representar as atividades a serem realizadas.

Critérios de aceitação:
- Cada cartão contém identificador, nome, responsável, data limite, prioridade e descrição.
- Um novo cartão é criado por padrão na coluna A FAZER.

---

### US07 — Mover cartão entre colunas

**Como** usuário de um projeto,
**Eu quero** mover um cartão entre as colunas do quadro,
**Para** refletir o avanço da atividade no fluxo.

Critérios de aceitação:
- A movimentação respeita o limite de WIP da coluna de destino.
- A movimentação é registrada com data e hora.

---

### US08 — Mover cartão entre raias

**Como** usuário de um projeto,
**Eu quero** mover um cartão entre as raias do quadro,
**Para** reclassificar a atividade.

Critérios de aceitação:
- O cartão passa a pertencer à raia de destino.
- A movimentação é registrada com data e hora.

---

### US09 — Definir limite de WIP

**Como** líder de projeto,
**Eu quero** estabelecer o número máximo de cartões por coluna,
**Para** limitar o trabalho em progresso e evitar gargalos.

Critérios de aceitação:
- Tentar mover um cartão para uma coluna cheia é bloqueado com mensagem explicativa.
- Um limite igual a zero ou ausente significa "sem limite".

---

### US10 — Calcular métricas de fluxo

**Como** líder de projeto,
**Eu quero** calcular cycle time, lead time, throughput e WIP,
**Para** avaliar o desempenho do fluxo de trabalho.

Critérios de aceitação:
- *Lead time*: tempo entre a entrada do cartão em A FAZER e a chegada em FEITO.
- *Cycle time*: tempo entre a entrada em FAZENDO e a chegada em FEITO.
- *Throughput*: número de cartões que chegaram a FEITO em um período.
- *WIP*: número de cartões atualmente em colunas não finais.
