# ParaFazer

## Projeto de Interface com o Usuário — Storyboards e Wireframes

O projeto de interface é representado por storyboards, cada um descrevendo um cenário de uso
composto por uma sequência de wireframes. Os wireframes são esboços simples de tela.

---

### Storyboard 1 — Acesso ao sistema

**Cenário:** um usuário cadastrado autentica-se e chega ao seu quadro.

**Wireframe 1.1 — Login**

```
+-------------------------------------------+
|                ParaFazer                  |
|-------------------------------------------|
|   E-mail:    [_____________________]      |
|   Senha:     [_____________________]      |
|                                           |
|        [ Entrar ]   [ Criar conta ]       |
+-------------------------------------------+
```

**Wireframe 1.2 — Lista de projetos**

```
+-------------------------------------------+
|  ParaFazer            usuario@exemplo.com |
|-------------------------------------------|
|  Meus projetos                            |
|   > Projeto Alpha                         |
|   > Projeto Beta                          |
|                                           |
|  [ + Novo projeto ]                       |
+-------------------------------------------+
```

---

### Storyboard 2 — Visualização e movimentação no quadro

**Cenário:** o usuário abre um quadro e move um cartão de A FAZER para FAZENDO.

**Wireframe 2.1 — Quadro Kanban**

```
+----------------------------------------------------------+
|  Projeto Alpha  >  Quadro Principal                       |
|----------------------------------------------------------|
| Raia: Backend                                             |
|  A FAZER (3)   |  FAZENDO (1/2)  |  FEITO (5)             |
|  [#12 Login ]  |  [#08 API ]     |  [#01 Setup ]          |
|  [#15 BD    ]  |                 |  [#02 Visão ]          |
|  [#18 Deploy]  |                 |  ...                   |
|----------------------------------------------------------|
| Raia: Frontend                                            |
|  A FAZER (2)   |  FAZENDO (0/2)  |  FEITO (3)             |
|  [#20 Telas ]  |                 |  [#05 Wireframe]       |
+----------------------------------------------------------+
|  [ + Cartão ]  [ Métricas ]  [ Config. WIP ]              |
+----------------------------------------------------------+
```

**Wireframe 2.2 — Detalhe / edição de cartão**

```
+-------------------------------------------+
|  Cartão #12                               |
|-------------------------------------------|
|  Nome:        [ Implementar login      ]  |
|  Responsável: [ Atila              v   ]  |
|  Data limite: [ 31/05/2026             ]  |
|  Prioridade:  ( ) Baixa (o) Media ( )Alta |
|  Descrição:   [ Tela e validação...    ]  |
|                                           |
|  Mover para:  [ FAZENDO v ]  [ Salvar ]   |
+-------------------------------------------+
```

---

### Storyboard 3 — Métricas de fluxo

**Cenário:** o líder consulta as métricas do quadro.

**Wireframe 3.1 — Painel de métricas**

```
+-------------------------------------------+
|  Métricas — Quadro Principal              |
|-------------------------------------------|
|  WIP atual ............... 1              |
|  Throughput (hoje) ....... 4 cartões      |
|  Lead time médio ......... 2,5 dias       |
|  Cycle time médio ........ 1,2 dias       |
|                                           |
|              [ Voltar ]                   |
+-------------------------------------------+
```

---

> **A inserir na entrega final:** versões desenhadas dos wireframes (ferramenta de wireframe ou
> esboço à mão digitalizado), caso o professor prefira além do esboço textual acima.
