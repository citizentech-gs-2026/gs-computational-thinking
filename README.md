# Garoa · Lógica (Python)

Computational Thinking with Python · Global Solution FIAP 2026.2 · CitizenTech da Minha Cidade
Entrega: 19/11/2026, 23h55 · Teams: um único ZIP

Esta é uma das partes da CitizenTech Garoa. A ficha completa, a pesquisa e as decisões ficam no gs-docs.

## A CitizenTech em uma frase

Garoa: um sensor barato no ar e na parede fria de cada cômodo calcula o ponto de orvalho. Ele avisa antes de o mofo aparecer, diz se abrir a janela ajuda ou piora e guarda um histórico que vira prova do morador.

| | |
|---|---|
| Cidadão | Família que mora de aluguel ou em casa precária com mofo, principalmente com criança ou pessoa com asma, rinite ou alergia |
| Problema | O mofo cresce escondido, adoece quem mora na casa, e quando a família reclama não tem como provar que o problema é do imóvel |
| Cidade | São Paulo (SP) |
| ODS | 3 (saúde), 11 (cidades e moradia), 10 (menos desigualdade) |

## O que esta parte faz

Aplicação Python de terminal que processa as medições e decide. Ela cadastra casas e cômodos em JSON, registra leituras do ar e da parede, calcula o ponto de orvalho e a umidade na parede, classifica o estado (SECO, ATENÇÃO, RISCO, CONDENSAÇÃO), diz se abrir a janela ajuda ou piora e gera o laudo do mês. Usa menu, validação de entrada, try/except e match/case. O plano completo está em docs/PLANO.md, no repositório do grupo (essa pasta não vai no ZIP).

## Estrutura

- src/ código Python (main.py e módulos)
- dados/ arquivo JSON de persistência
- docs/ ENTREGA.md (o que enviar) e PLANO.md (o que o programa faz)
- prompt.md uso de IA (obrigatório)
- testes/ conferência das contas com os valores de referência (`python3 testes/testar_calculos.py`)
- entrega/montar_zip.py gera o ZIP da entrega

O ZIP enviado no Teams tem só src/, dados/garoa.json, prompt.md e readme.md. As pastas docs/, testes/ e entrega/ ficam apenas no repositório.

## Como rodar

Precisa de Python 3.10 ou mais novo (por causa do match/case). Não precisa instalar nada: só a biblioteca padrão do Python.

Abra o terminal na pasta do projeto (a que tem src/ e dados/) e rode:

```
python3 src/main.py
```

No Windows, se `python3` não funcionar, use `python src/main.py`. O programa descobre a pasta do projeto a partir do próprio arquivo e lê e grava `dados/garoa.json` ali, então também funciona se for aberto de outra pasta, com o caminho completo do main.py (se a pasta `dados/` não existir, ele a cria ao gravar). Não há `requirements.txt` porque o programa não usa nenhuma biblioteca externa: só `json`, `math` e `os` (para montar os caminhos). Ele já abre com uma casa de exemplo (Apartamento 12, com Quarto e Sala) e 12 leituras de outubro e novembro de 2026. Para testar o laudo, escolha a opção 6 e digite `2026-10` ou `2026-11`.

## Funcionalidades

1. **Cadastrar casa**: nome e bairro. Não aceita nome vazio nem repetido.
2. **Cadastrar cômodo**: escolhe a casa numa lista e dá nome ao cômodo.
3. **Registrar leitura**: data (AAAA-MM-DD), temperatura e umidade do ar e temperatura da parede. O programa calcula o ponto de orvalho e a umidade na parede (fórmula de Magnus), classifica o estado e grava no JSON.
4. **Ver o estado de um cômodo**: mostra a leitura mais recente, o estado e o que ele quer dizer, além do alerta de ar seco (umidade do ar abaixo de 30%).
5. **Abrir a janela?**: compara a umidade absoluta (g/m³) de dentro e de fora, com folga de 0,5 g/m³, e diz ABRIR, FECHAR ou TANTO FAZ.
6. **Laudo do mês**: para um mês AAAA-MM, conta as leituras de cada estado por cômodo e mostra o percentual em RISCO ou CONDENSAÇÃO, com mensagens que não culpam o morador. Pode salvar o laudo em `dados/laudo_AAAA-MM_casaN.txt`.
7. **Histórico de um cômodo**: tabela com todas as leituras em ordem de data.
0. **Sair**.

Estados de uma leitura:

| Estado | Quando |
|---|---|
| SENSOR | Leitura impossível: temperatura fora de -10 a 60 °C ou umidade fora de 0 a 100% |
| CONDENSAÇÃO | Temperatura da parede menor ou igual ao ponto de orvalho |
| RISCO | Umidade na parede de 80% ou mais |
| ATENÇÃO | Umidade na parede de 70% a menos de 80% |
| SECO | Umidade na parede abaixo de 70% |

Proteções: número inválido, valor fora da faixa, data que não existe (como 2026-13-40 ou 2026-02-30), texto vazio e opção inexistente fazem a pergunta se repetir. Se `dados/garoa.json` estiver ausente ou corrompido, o programa avisa e começa sem dados, sem mostrar erro técnico.

## Organização do código

| Arquivo | O que faz |
|---|---|
| src/main.py | Abre o programa, carrega os dados e mantém o menu (while + match/case) |
| src/menu.py | Uma função para cada opção do menu e as telas |
| src/calculos.py | Contas: pressão de saturação, ponto de orvalho, umidade na parede, umidade absoluta, estado e janela |
| src/entrada.py | Leitura com validação: números, textos, datas, meses, s/n e escolha em lista |
| src/dados.py | Lê e grava o JSON (json.load e json.dump), monta os caminhos dos arquivos e faz as buscas nas listas |
| dados/garoa.json | Casas, cômodos e leituras de exemplo |

## Integração com o restante da solução

Esta aplicação é a parte "lógica" da Garoa e conversa com as outras partes pelas mesmas regras:

- **Sensor (ESP32):** o kit mede a temperatura e a umidade do ar e a temperatura da parede. O programa recebe esses mesmos três números (digitados, na simulação) e usa os mesmos limites do sensor: umidade na parede de 70% (ATENÇÃO) e 80% (RISCO), e CONDENSAÇÃO quando a parede está no ponto de orvalho ou abaixo.
- **App web (gs-web-app):** as contas (fórmula de Magnus com A = 17,62 e B = 243,12) e os estados são os mesmos do app, então o mesmo cômodo recebe a mesma resposta no app e aqui. O JSON de leituras tem os mesmos campos (data, ar, parede, ponto de orvalho, umidade na parede e estado) que o histórico do app, e o laudo do mês é o mesmo conceito do laudo do app.
- **Matemática (Differentiated Problem Solving):** a decisão "abrir a janela?" usa a umidade absoluta de dentro e de fora. O modelo cúbico da umidade de fora (dados do INMET) mostra que a umidade externa passa de 80% entre 21h e 7h, e por isso a recomendação típica é fechar a janela de madrugada e abrir à tarde.
- **Experiência e pitch:** o laudo do mês usa mensagens que não culpam o morador, como na interface do app.

## Equipe

| Nome completo | RM |
|---|---|
| Ana Beatriz Da Cruz Silva | RM572278 |
| Arthur Carvalho Gomes Da Costa | RM570387 |
| Carolina Kiyomi Hada | RM571664 |
| Sávio Pessôa Afonso | RM570789 |
| Victor Paes Pontes | RM572781 |

## Entrega

O que enviar, o checklist e os critérios de nota estão em docs/ENTREGA.md, no repositório do grupo.
