# prompt.md: uso de Inteligência Artificial

## 1. Ferramentas utilizadas
| Ferramenta | Para que usamos |
|---|---|
| Claude (chat no claude.ai) | Planejar a aplicação: menu, formato do JSON, contas, estados, janela e laudo. Gerou o pacote com README.md, docs/ENTREGA.md e docs/PLANO.md, que revisamos e usamos como especificação. |
| Claude Code (extensão do VS Code, modelo Claude Opus 5.5) | Escrever o código em Python a partir do PLANO.md, os testes das contas, o script que monta o ZIP, e completar o readme e este prompt.md. Também rodou os testes e o programa com entradas erradas, e depois fez a revisão final (caminhos dos arquivos, seção de integração e limpeza do prompt.md). |
| Python 3.11 (terminal) | Rodar o programa, os testes de referência (testes/testar_calculos.py) e o script do ZIP. |
| Git | Guardar cada etapa num commit pequeno. |

## 2. Interações realizadas (prompts e respostas)

### Interação 1: planejamento da aplicação
- **Prompt:** pedimos ao Claude um plano para a parte de Python da Garoa: o que o programa de terminal deve fazer, o formato do JSON, as contas do ponto de orvalho, os estados do cômodo e o que a disciplina exige.
- **Resumo da resposta:** um pacote com README.md, docs/ENTREGA.md (checklist e critérios de nota) e docs/PLANO.md (menu de 7 opções, JSON com casas e leituras, fórmula de Magnus com A = 17,62 e B = 243,12, estados SENSOR, CONDENSAÇÃO, RISCO, ATENÇÃO e SECO, decisão da janela com folga de 0,5 g/m³, laudo do mês e regras de validação).
- **O que aproveitamos:** o PLANO.md virou a especificação do código. Mantivemos os mesmos limites (70% e 80%) do app e do ESP32, para as três partes da Garoa darem a mesma resposta.

### Interação 2: implementação do programa
- **Prompt (resumo):** "Implemente a entrega de Python da Garoa seguindo README.md, docs/ENTREGA.md e docs/PLANO.md. Terminal, só biblioteca padrão, `python3 src/main.py`, código dividido em módulos, dados/garoa.json de exemplo com 1 casa, 2 cômodos e cerca de 12 leituras em 2 meses. Use menu com while + match/case, validação que repete a pergunta, try/except (números, data e JSON ausente ou corrompido), if/elif/else, for, funções com retorno, listas, tuplas e dicionários e JSON. Só conteúdo visto em aula: nada de datetime, os, sys, lambda nem bibliotecas externas; data validada com split('-') e int(). Confira os valores de referência num arquivo de testes, monte o ZIP com um script e preencha o readme e o prompt.md." O pedido trazia também os valores de referência (por exemplo, ar a 22 °C e 70% com parede a 17 °C dá ponto de orvalho de 16,27 °C, 95,5% na parede e RISCO).
- **Resumo da resposta:** o Claude criou cinco módulos (main.py, menu.py, calculos.py, entrada.py e dados.py), o arquivo de testes, o JSON de exemplo e o script montar_zip.py. Primeiro escreveu as contas e os testes e rodou os testes antes de fazer o menu.
- **O que aproveitamos:** o código inteiro, depois de testado. Duas decisões do Claude que revisamos:
  - O plano pedia duas coisas ao mesmo tempo: recusar valor fora da faixa e ter o estado SENSOR para leitura impossível. A solução foi aceitar na digitação a faixa que o sensor consegue medir (-40 a 85 °C) e marcar como SENSOR o que fica fora de -10 a 60 °C.
  - Umidade de 0% vira SENSOR, porque o logaritmo da fórmula não existe para zero.

### Interação 3: revisão e testes com entradas erradas
- **Prompt (resumo, parte final do mesmo pedido):** "Antes de terminar, releia o código contra os requisitos, confirme com busca no código que não há datetime, lambda nem bibliotecas fora da padrão, e rode na mão as entradas ruins: letra no lugar de número, temperatura fora da faixa, data 2026-13-40, opção 99, vazio, e o JSON apagado e corrompido."
- **Resumo da resposta:** o Claude buscou no código os termos proibidos (nada encontrado) e conferiu em qual arquivo aparece cada requisito. Rodou o programa com cada entrada ruim e encontrou detalhes de tela para corrigir (lista na seção 4).
- **O que aproveitamos:** as correções e a lista de onde cada requisito aparece, que usamos para estudar o código.

### Interação 4: revisão final com base no feedback do professor
- **Prompt (resumo):** lemos o feedback que o professor deu à Sprint 4 (chave de API dentro do ZIP, gravação sem try/except, caminhos que dependem da pasta de onde o programa roda, uso de biblioteca sem requirements.txt, programa grande em um arquivo só, falta de seção de integração) e pedimos ao Claude para conferir se a entrega da GS repetia esses problemas e para corrigir o que repetisse.
- **Resumo da resposta:** o Claude verificou que não havia chave de API nem biblioteca externa, que as duas gravações (JSON e laudo) tinham try/except e que o código já estava dividido em módulos. Apontou que o caminho `dados/garoa.json` dependia da pasta de onde o programa era aberto, que o prompt.md ainda tinha um aviso interno e que faltava explicar a integração com as outras partes da Garoa.
- **O que aproveitamos:** os caminhos passaram a ser calculados a partir da pasta do próprio programa (`os.path`, em `dados.py`), `salvar_dados` cria a pasta `dados/` se ela não existir, o README ganhou a seção "Integração com o restante da solução" e o aviso foi retirado deste arquivo.

### Interação 5: conferência antes de enviar
- **Prompt (resumo):** "Fiz alguns ajustes. Reverifique tudo: se está certo e coerente, se há algum ponto de que o professor pode reclamar (ele corrige com IA) e faça testes para garantir que tudo funciona como previsto."
- **Resumo da resposta:** o Claude leu as mudanças, rodou de novo os testes de referência e o programa inteiro (as 7 opções, entradas erradas, JSON ausente, corrompido e com formato errado, pasta `dados/` apagada, programa aberto de outra pasta e o ZIP extraído fora do repositório). Tudo funcionou. Apontou ajustes de acabamento: as confirmações mostravam o caminho completo do Windows em toda gravação, algumas linhas de código passavam de 100 caracteres e o readme citava docs/PLANO.md e docs/ENTREGA.md, que não vão no ZIP.
- **O que aproveitamos:** a tela passou a mostrar só `dados/garoa.json`, as linhas longas foram quebradas e o readme passou a dizer que a pasta docs/ fica no repositório.

## 3. Aplicação no projeto
Feito com ajuda da IA e revisado pelo grupo:
- **src/calculos.py:** `pressao_saturacao`, `ponto_de_orvalho`, `umidade_na_parede`, `umidade_absoluta`, `dentro_da_faixa`, `leitura_possivel`, `classificar` (estado da leitura), `ar_seco` e `decidir_janela`. Constantes em tuplas: `FAIXA_TEMPERATURA`, `FAIXA_UMIDADE`, `LIMITES_PAREDE` (70 e 80) e `ESTADOS`.
- **src/entrada.py:** `ler_texto`, `ler_float`, `ler_inteiro`, `ler_sim_nao`, `ler_data`, `ler_mes` e `escolher_da_lista`, todas com while repetindo a pergunta. A data é conferida com `split("-")` e `int()` dentro de try/except, incluindo o número de dias de cada mês e o ano bissexto.
- **src/dados.py:** `carregar_dados` e `salvar_dados` (json.load e json.dump com try/except), `caminho_laudo` (monta o caminho do laudo), `estrutura_valida` e as buscas `buscar_casa`, `comodo_existe`, `leituras_do_comodo` e `leituras_do_mes` (filtro por `data[:7]`).
- **src/menu.py:** uma função por opção (`cadastrar_casa`, `cadastrar_comodo`, `registrar_leitura`, `ver_estado`, `abrir_janela`, `gerar_laudo` e `mostrar_historico`), mais `montar_laudo`, `contar_estados` e `percentual_mofo`.
- **src/main.py:** `main` (laço while do menu) e `executar_opcao` (match/case).
- **dados/garoa.json:** exemplo com o Apartamento 12 (Jardim Ângela), Quarto e Sala, e 12 leituras de outubro e novembro de 2026. Os valores calculados foram gerados pelas próprias funções de calculos.py.
- **testes/testar_calculos.py** e **entrega/montar_zip.py** (ficam fora do ZIP, exceto o resultado).

## 4. Validação
- **Valores de referência:** testes/testar_calculos.py confere com `assert` os 5 casos de parede (por exemplo, 22 °C, 70% e parede a 16 °C dá 16,27 °C, 100% e CONDENSAÇÃO) e os 3 casos da janela (22/70 dentro e 18/60 fora dá 13,55 e 9,20 g/m³ e ABRIR). Também confere SENSOR, os limites de 70% e 80% e o alerta de ar seco. Todos passaram.
- **Entradas inválidas testadas no programa:** letra no lugar de número, temperatura 200 °C, umidade 150% e -5%, datas 2026-13-40, 2026-02-30 e "ontem", mês 2026-1, opção 99, opção vazia, nome vazio ou só com espaços, casa com nome repetido (mesmo com letras minúsculas), "sim" e "n" na pergunta s/n. Em todos os casos a pergunta se repetiu, sem erro na tela.
- **Caminhos:** depois da correção, rodamos o programa de uma pasta diferente da raiz (por exemplo, `python3 /caminho/do/projeto/src/main.py`), registramos uma leitura, geramos e salvamos o laudo, e apagamos a pasta `dados/` para ver o programa recriá-la ao gravar. Tudo funcionou sem erro na tela.
- **JSON:** apagamos o arquivo, gravamos um JSON quebrado pela metade e um JSON válido mas com outro formato (uma lista). Nos três casos o programa avisou e começou vazio, e a gravação seguinte criou um arquivo correto. Encerrar a entrada no meio (Ctrl+D ou Ctrl+C) mostra uma mensagem curta em vez de erro.
- **Conferência das contas:** o ponto de orvalho de 16,3 °C para 22 °C e 70%, previsto no PLANO.md, saiu igual no programa. O laudo de 2026-11 dos dados de exemplo dá 75% das leituras do Quarto em RISCO ou CONDENSAÇÃO.
- **O que foi corrigido durante os testes:**
  - O primeiro código usava `raise`, `enumerate` e `sort(key=...)`, que não vimos em aula. Foram trocados por funções que devolvem None ou False, por `range(len(...))` e por uma inserção em ordem feita com while.
  - Uma leitura de exemplo dava 69,97% na parede: aparecia como "70,0%" mas o estado era SECO, o que confundia. Foi trocada por outra que cai em ATENÇÃO.
  - O laudo dizia "na maior parte do mês" com exatamente 50%. Passou a dizer "em metade ou mais das leituras".
  - A leitura SENSOR mostrava "Umidade na parede: -%". Agora mostra só o estado e o aviso.
  - A confirmação de cadastro dizia "Casa Casa da Vila cadastrada". Mudou para "Casa cadastrada: Casa da Vila".
  - Depois da mudança para `os.path`, cada confirmação mostrava o caminho completo do arquivo (C:\Users\...). Passou a mostrar só `dados/garoa.json`.
- **ZIP:** o script lista e confere o conteúdo. O ZIP foi extraído numa pasta temporária fora do repositório e o programa rodou lá dentro, abrindo com os dados de exemplo.

## 5. Análise crítica
- **Benefícios:** a IA transformou o plano em código rapidamente e já dividido em módulos pequenos. Ter os valores de referência antes de começar ajudou muito: as contas foram conferidas com testes automáticos, e não só "no olho". A revisão com entradas erradas achou detalhes de tela que provavelmente passariam.
- **Limitações:** a IA tende a usar recursos de Python que não vimos em aula, e foi preciso pedir e conferir que o código ficasse só no conteúdo da disciplina. A exceção consciente é o módulo `os` da biblioteca padrão, usado só para montar os caminhos dos arquivos a partir da pasta do programa; preferimos isso a depender da pasta de onde o terminal é aberto.
- **Dificuldades:** conciliar duas regras do plano que pareciam brigar (recusar valor fora da faixa e ter o estado SENSOR) e garantir que todo o grupo entende cada função, já que o código não foi digitado por nós linha a linha. Para isso, estudamos a lista de onde está cada requisito e as perguntas que o professor pode fazer.
