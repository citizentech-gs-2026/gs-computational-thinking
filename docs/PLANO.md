# Plano da aplicação em Python

Programa de terminal da Garoa: cadastra casas e cômodos, registra leituras do ar e da parede, calcula o ponto de orvalho, classifica o risco de mofo, diz se abrir a janela ajuda e gera o laudo do mês. Usa os mesmos limites do app (gs-web-app) e do ESP32.

## Menu
1. Cadastrar casa
2. Cadastrar cômodo
3. Registrar leitura (data, temperatura do ar, umidade do ar e temperatura da parede)
4. Ver o estado de um cômodo
5. Abrir a janela? (temperatura e umidade de fora)
6. Laudo do mês
7. Histórico de um cômodo
0. Sair

O menu usa while e match/case. Cada opção chama uma função.

## Persistência (JSON)
Arquivo dados/garoa.json, com duas listas: casas (cada casa tem seus cômodos) e leituras. Cada leitura guarda: casa, comodo, data (AAAA-MM-DD), temp_ar, ur_ar, temp_parede, orvalho, ur_parede e estado. Se o arquivo não existir ou estiver corrompido, o programa avisa e começa vazio (try/except).

## Contas (import math)
Fórmula de Magnus, com A = 17,62 e B = 243,12 °C:
- pressão de saturação (hPa) = 6,112 · exp(A·T / (B + T))
- ponto de orvalho = B·γ / (A − γ), com γ = ln(UR/100) + A·T / (B + T)
- umidade na parede (%) = UR do ar · psat(T do ar) / psat(T da parede), no máximo 100
- umidade absoluta (g/m³) = 216,7 · (UR/100 · psat(T)) / (273,15 + T)
Conferência: ar a 22 °C e 70% dá ponto de orvalho de 16,3 °C, e 95,5% numa parede a 17 °C.

## Estados do cômodo
- SENSOR: leitura impossível (temperatura fora de -10 a 60 °C, ou umidade fora de 0 a 100%)
- CONDENSAÇÃO: temperatura da parede menor ou igual ao ponto de orvalho
- RISCO: umidade na parede de 80% ou mais
- ATENÇÃO: de 70% a menos de 80%
- SECO: abaixo de 70%
- Alerta extra de ar seco: umidade do ar abaixo de 30%

Os limites ficam numa tupla constante.

## Abrir a janela?
Compara a umidade absoluta de dentro e de fora, com folga de 0,5 g/m³: ABRIR se fora < dentro − 0,5; FECHAR se fora > dentro + 0,5; senão, TANTO FAZ.

## Laudo do mês
O usuário digita AAAA-MM. O programa filtra as leituras com data[:7] igual ao mês, conta quantas ficaram em cada estado, e mostra o percentual de leituras em RISCO ou CONDENSAÇÃO por cômodo. Mensagens que não culpam o morador. Opcional: salvar como arquivo de texto.

## Validação
- Números: try/except ValueError, com limites de faixa e repetição da pergunta (while)
- Data: dividir por "-" e converter para int com try/except; checar mês de 1 a 12 e dia de 1 a 31 (sem datetime)
- Textos: não aceitar vazio
- Escolha do menu: repetir até ser válida

## Funções (exemplos)
pressao_saturacao, ponto_de_orvalho, umidade_na_parede, umidade_absoluta, classificar, decidir_janela, ler_float, ler_data, carregar_dados, salvar_dados, cadastrar_casa, cadastrar_comodo, registrar_leitura, gerar_laudo, mostrar_historico, main.

## Estrutura
- src/main.py e módulos (calculos.py, dados.py, menu.py, se fizer sentido)
- dados/garoa.json
- docs/ (ENTREGA.md e este plano)
- prompt.md e README.md
