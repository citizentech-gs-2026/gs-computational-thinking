# Testemunha · Lógica (Python)

> **Computational Thinking with Python** · Global Solution FIAP 2026.2 · CitizenTech da Minha Cidade
> Entrega: **19/11/2026, 23h55** · Teams: um único ZIP

Esta é uma das partes da CitizenTech **Testemunha**. A ficha completa, a pesquisa e as decisões ficam no [gs-docs](https://github.com/citizentech-gs-2026/gs-docs).

## A CitizenTech em uma frase
**Testemunha** (nome provisório): um sensor barato no ar e na parede fria de cada cômodo calcula o ponto de orvalho. Ele avisa antes de o mofo aparecer, diz se abrir a janela ajuda ou piora e guarda um histórico que vira prova do morador.

| | |
|---|---|
| Cidadão | Família que mora de aluguel ou em casa precária com mofo, principalmente com criança ou pessoa com asma, rinite ou alergia |
| Problema | O mofo cresce escondido, adoece quem mora na casa, e quando a família reclama não tem como provar que o problema é do imóvel |
| Cidade | São Paulo (SP) |
| ODS | 3 (saúde), 11 (cidades e moradia), 10 (menos desigualdade) |

## O que esta parte faz
Aplicação Python de terminal que **processa as medições e decide**. Ela cadastra casas e cômodos em JSON, registra leituras do ar e da parede, calcula o ponto de orvalho e a umidade na parede, classifica o estado (SECO, ATENÇÃO, RISCO, CONDENSAÇÃO) e gera o laudo do mês. Usa menu, validação de entrada, try/except e match/case.

## Estrutura
```
src/        código Python (main.py e módulos)
dados/      arquivos JSON de persistência
docs/       ENTREGA.md
prompt.md   uso de IA (obrigatório)
```

## Como rodar
```bash
python3 src/main.py
```

## Equipe
| Nome completo | RM |
|---|---|
| Ana Beatriz Da Cruz Silva | RM572278 |
| Arthur Carvalho Gomes Da Costa | RM570387 |
| Carolina Kiyomi Hada | RM571664 |
| Sávio Pessôa Afonso | RM570789 |
| Victor Paes Pontes | RM572781 |

## Entrega
O que enviar, checklist e critérios de nota estão em **[docs/ENTREGA.md](docs/ENTREGA.md)**.
