# Vídeo do teste de sistema (K11)

Coloque aqui o vídeo (ou um arquivo `LINK.txt` com o link) demonstrando um
**cenário de sucesso para cada serviço** do ParaFazer.

## Preparação (antes de gravar)

```bash
cd src
python3 seed.py     # cria dados de demonstração (zera o banco)
python3 main.py     # inicia a interface
```

> O `seed.py` **apaga e recria** o banco. Rode-o **uma vez** antes de gravar.
> Para mostrar persistência no fim, apenas feche e reabra com `python3 main.py`.

### Credenciais de demonstração (senha: `123456`)

| E-mail | Papel |
| --- | --- |
| `raul@exemplo.com` | líder |
| `atila@exemplo.com` | membro |

## Roteiro — cena a cena

Cada passo cobre um serviço exigido. As teclas (`c`, `m`, `s`...) são as do menu.

| # | Serviço | O que fazer na tela |
| --- | --- | --- |
| 1 | **Criar conta** (US01) | Tela inicial → `2`. Nome: `Maria`, e-mail: `maria@exemplo.com`, senha: `123456`. Aparece "Conta criada". |
| 2 | **Autenticar** (US02) | Tela inicial → `1`. E-mail `raul@exemplo.com`, senha `123456`. (Mostre antes uma senha errada → "Credenciais inválidas".) |
| 3 | **Participar de projeto** (US03) | Aparece a lista com o projeto `ParaFazer`; abra-o. Para reforçar: dentro do projeto use `a` (add membro), digite o e-mail de outra conta (ex.: `maria@exemplo.com`) → "X adicionado ao projeto". Depois logue com essa conta e mostre que o projeto aparece pra ela. |
| 4 | **CRUD de quadro** (US04) | Em "Quadros": `n` e crie `Quadro Demo` (note que A FAZER/FAZENDO/FEITO são criadas sozinhas). Depois abra o `Quadro Principal` (que já tem cartões). |
| 5 | **CRUD de raia** (US05) | No quadro: `r` e crie a raia `Frontend`. |
| 6 | **CRUD de cartão** (US06) | `c` para criar `Nova tela` (prioridade `alta`). Mostre também `e` (editar) o nome do cartão. |
| 7 | **Mover entre colunas** (US07) | `m`, informe o ID do cartão e escolha a coluna `FAZENDO`. |
| 8 | **Mover entre raias** (US08) | `s`, informe o ID do cartão e escolha a raia `Frontend`. |
| 9 | **Definir limite de WIP** (US09) | `w` na coluna `FAZENDO`, limite `1`. Depois tente `m` outro cartão para `FAZENDO` → aparece "Limite de WIP atingido" (bloqueio funcionando). |
| 10 | **Calcular métricas** (US10) | `x` para mostrar WIP, throughput, lead time e cycle time. |

## Fechamento (mostrar persistência)

1. `v` para voltar, `q` para sair da conta, `0` para encerrar.
2. Rode `python3 main.py` de novo, faça login e abra o projeto.
3. Os dados criados continuam lá → prova de que o sistema persiste no banco.

## Dicas de gravação

- Mostre o terminal grande e com fonte legível.
- Narre rapidamente cada serviço ("agora vou mover o cartão entre raias").
- O vídeo precisa de **um cenário de sucesso por serviço** — siga a tabela na ordem.