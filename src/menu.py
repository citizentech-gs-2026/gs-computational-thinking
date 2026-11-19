"""Telas e ações do menu da Garoa: cada opção do menu é uma função daqui."""

import calculos
import dados
import entrada

# Faixa que o termômetro do sensor consegue medir (fora de -10 a 60 °C vira estado SENSOR)
FAIXA_DIGITADA_TEMPERATURA = (-40.0, 85.0)

# Opções do menu principal: (número, texto)
OPCOES_MENU = (
    ("1", "Cadastrar casa"),
    ("2", "Cadastrar cômodo"),
    ("3", "Registrar leitura"),
    ("4", "Ver o estado de um cômodo"),
    ("5", "Abrir a janela?"),
    ("6", "Laudo do mês"),
    ("7", "Histórico de um cômodo"),
    ("0", "Sair"),
)

# O que cada estado quer dizer, sem culpar quem mora na casa
MENSAGENS_ESTADO = {
    "SECO": "Parede seca. Por enquanto o mofo não tem condição de crescer.",
    "ATENÇÃO": "A parede está ficando úmida. Vale ventilar quando o ar de fora\n"
               "  estiver mais seco.",
    "RISCO": "A parede está úmida o bastante para o mofo crescer, mesmo sem mancha visível.",
    "CONDENSAÇÃO": "A parede está mais fria que o ponto de orvalho: a água do ar vira\n"
                   "  gota nela. Isso é sinal de parede fria ou mal isolada,\n"
                   "  um problema do imóvel.",
    "SENSOR": "Leitura impossível. Confira se o sensor está bem colocado e funcionando.",
}

# O que fazer com a janela em cada decisão
MENSAGENS_JANELA = {
    "ABRIR": "Abra a janela: o ar de fora tem menos água e vai secar o cômodo.",
    "FECHAR": "Mantenha a janela fechada: o ar de fora tem mais água e pioraria a umidade.",
    "TANTO FAZ": "Tanto faz: a quantidade de água no ar é parecida dentro e fora.",
}

LINHA = "-" * 52


def formatar(numero, casas=1):
    """Formata um número com vírgula decimal, como se escreve no Brasil."""
    if numero is None:
        return "-"
    return f"{numero:.{casas}f}".replace(".", ",")


def mostrar_titulo():
    """Mostra o nome do programa."""
    print("=" * 52)
    print("  GAROA - avisa antes de o mofo aparecer")
    print("  Ponto de orvalho, umidade na parede e laudo do mês")
    print("=" * 52)


def mostrar_menu():
    """Mostra o menu numerado."""
    print(f"\n{LINHA}\nMENU")
    for numero, texto in OPCOES_MENU:
        print(f"  {numero}. {texto}")
    print(LINHA)


def confirmar_gravacao(dados_garoa, mensagem):
    """Grava o JSON e mostra a confirmação; devolve True se gravou."""
    if dados.salvar_dados(dados.CAMINHO_DADOS, dados_garoa):
        print(f"\nOK: {mensagem} Dados gravados em {dados.NOME_EXIBIDO}.")
        return True
    return False


def escolher_casa(dados_garoa):
    """Pede para escolher uma casa e devolve o dicionário dela (ou None)."""
    nomes = dados.nomes_das_casas(dados_garoa)
    if len(nomes) == 0:
        print("\nNenhuma casa cadastrada. Use a opção 1 primeiro.")
        return None
    nome = entrada.escolher_da_lista("Escolha a casa:", nomes)
    return dados.buscar_casa(dados_garoa, nome)


def escolher_comodo(dados_garoa):
    """Pede casa e cômodo e devolve a tupla (casa, nome do cômodo) ou None."""
    casa = escolher_casa(dados_garoa)
    if casa is None:
        return None
    if len(casa["comodos"]) == 0:
        print(f"\nA casa {casa['nome']} ainda não tem cômodos. Use a opção 2 primeiro.")
        return None
    comodo = entrada.escolher_da_lista("Escolha o cômodo:", casa["comodos"])
    return (casa, comodo)


def cadastrar_casa(dados_garoa):
    """Cadastra uma casa nova com nome e bairro."""
    print("\nCADASTRAR CASA")
    nome = entrada.ler_texto("Nome da casa (ex.: Apartamento 12): ")
    if dados.buscar_casa(dados_garoa, nome) is not None:
        print(f"Já existe uma casa chamada {nome}.")
        return False
    bairro = entrada.ler_texto("Bairro: ")
    dados_garoa["casas"].append({"nome": nome, "bairro": bairro, "comodos": []})
    return confirmar_gravacao(dados_garoa, f"Casa cadastrada: {nome}.")


def cadastrar_comodo(dados_garoa):
    """Cadastra um cômodo dentro de uma casa já cadastrada."""
    print("\nCADASTRAR CÔMODO")
    casa = escolher_casa(dados_garoa)
    if casa is None:
        return False
    nome = entrada.ler_texto("Nome do cômodo (ex.: Quarto das crianças): ")
    if dados.comodo_existe(casa, nome):
        print(f"A casa {casa['nome']} já tem o cômodo {nome}.")
        return False
    casa["comodos"].append(nome)
    return confirmar_gravacao(dados_garoa, f"Cômodo cadastrado: {nome}, em {casa['nome']}.")


def mostrar_resultado(leitura):
    """Mostra orvalho, umidade na parede, estado e alertas de uma leitura."""
    estado = leitura["estado"]
    print(f"\n  Ar: {formatar(leitura['temp_ar'])} °C e {formatar(leitura['ur_ar'], 0)}%"
          f" | Parede: {formatar(leitura['temp_parede'])} °C")
    if estado != "SENSOR":
        print(f"  Ponto de orvalho: {formatar(leitura['orvalho'])} °C")
        print(f"  Umidade na parede: {formatar(leitura['ur_parede'])}%")
    print(f"  ESTADO: {estado}")
    print(f"  {MENSAGENS_ESTADO.get(estado, '')}")
    if estado != "SENSOR" and calculos.ar_seco(leitura["ur_ar"]):
        print("  Alerta: ar seco (abaixo de 30%). Pode irritar nariz e garganta.")


def registrar_leitura(dados_garoa):
    """Pede data e medições, calcula o estado e grava a leitura."""
    print("\nREGISTRAR LEITURA")
    escolha = escolher_comodo(dados_garoa)
    if escolha is None:
        return False
    casa, comodo = escolha
    minimo, maximo = FAIXA_DIGITADA_TEMPERATURA

    data = entrada.ler_data("Data (AAAA-MM-DD): ")
    temp_ar = entrada.ler_float("Temperatura do ar (°C): ", minimo, maximo)
    ur_ar = entrada.ler_float("Umidade do ar (%): ", 0, 100)
    temp_parede = entrada.ler_float("Temperatura da parede (°C): ", minimo, maximo)

    leitura = {"casa": casa["nome"], "comodo": comodo, "data": data,
               "temp_ar": temp_ar, "ur_ar": ur_ar, "temp_parede": temp_parede}
    leitura.update(calculos.classificar(temp_ar, ur_ar, temp_parede))
    dados_garoa["leituras"].append(leitura)

    mostrar_resultado(leitura)
    return confirmar_gravacao(dados_garoa, f"Leitura de {data} registrada em {comodo}.")


def ver_estado(dados_garoa):
    """Mostra o estado do cômodo segundo a leitura mais recente."""
    print("\nESTADO DO CÔMODO")
    escolha = escolher_comodo(dados_garoa)
    if escolha is None:
        return None
    casa, comodo = escolha
    leituras = dados.leituras_do_comodo(dados_garoa, casa["nome"], comodo)
    if len(leituras) == 0:
        print(f"\n{comodo} ainda não tem leituras. Use a opção 3.")
        return None
    ultima = leituras[-1]
    print(f"\n{comodo} ({casa['nome']}), leitura de {ultima['data']}:")
    mostrar_resultado(ultima)
    return ultima["estado"]


def abrir_janela():
    """Compara a água no ar de dentro e de fora e diz se abrir a janela ajuda."""
    print("\nABRIR A JANELA?")
    minimo, maximo = FAIXA_DIGITADA_TEMPERATURA
    temp_dentro = entrada.ler_float("Temperatura dentro (°C): ", minimo, maximo)
    ur_dentro = entrada.ler_float("Umidade dentro (%): ", 1, 100)
    temp_fora = entrada.ler_float("Temperatura fora (°C): ", minimo, maximo)
    ur_fora = entrada.ler_float("Umidade fora (%): ", 1, 100)

    dentro, fora, decisao = calculos.decidir_janela(temp_dentro, ur_dentro, temp_fora, ur_fora)
    print(f"\n  Água no ar dentro: {formatar(dentro, 2)} g/m³")
    print(f"  Água no ar fora:   {formatar(fora, 2)} g/m³")
    print(f"  DECISÃO: {decisao}")
    print(f"  {MENSAGENS_JANELA[decisao]}")
    return decisao


def contar_estados(leituras):
    """Devolve um dicionário com quantas leituras ficaram em cada estado."""
    contagem = {}
    for estado in calculos.ESTADOS:
        contagem[estado] = 0
    for leitura in leituras:
        contagem[leitura["estado"]] = contagem.get(leitura["estado"], 0) + 1
    return contagem


def percentual_mofo(contagem, total):
    """Devolve o percentual de leituras em RISCO ou CONDENSAÇÃO."""
    if total == 0:
        return 0.0
    return (contagem["RISCO"] + contagem["CONDENSAÇÃO"]) * 100 / total


def montar_laudo(casa, mes, leituras_mes):
    """Devolve a lista de linhas do laudo do mês, um bloco por cômodo."""
    linhas = [f"LAUDO DO MÊS {mes} - {casa['nome']} ({casa.get('bairro', '-')})",
              f"Leituras no mês: {len(leituras_mes)}", LINHA]
    for comodo in casa["comodos"]:
        do_comodo = []
        for leitura in leituras_mes:
            if leitura["comodo"] == comodo:
                do_comodo.append(leitura)
        total = len(do_comodo)
        linhas.append(f"{comodo}: {total} leitura(s)")
        if total == 0:
            linhas.append("  Sem leituras neste mês.")
            continue
        contagem = contar_estados(do_comodo)
        for estado in calculos.ESTADOS:
            if contagem[estado] > 0:
                linhas.append(f"  {estado:<12} {contagem[estado]:>3}")
        percentual = percentual_mofo(contagem, total)
        linhas.append(f"  Em RISCO ou CONDENSAÇÃO: {formatar(percentual)}% das leituras")
        if percentual >= 50:
            linhas.append("  Em metade ou mais das leituras a parede teve condição de mofo.")
            linhas.append("  Isso aponta para o imóvel (parede fria, infiltração ou pouca")
            linhas.append("  ventilação), não para o jeito de morar.")
        elif percentual > 0:
            linhas.append("  Houve dias com condição de mofo. Vale continuar medindo.")
        else:
            linhas.append("  Nenhuma leitura com condição de mofo neste mês.")
    linhas.append(LINHA)
    linhas.append("Medições feitas pela família com a Garoa")
    linhas.append("(ponto de orvalho calculado pela fórmula de Magnus).")
    return linhas


def gravar_laudo(caminho, linhas):
    """Grava as linhas do laudo num arquivo de texto e devolve True se deu certo."""
    try:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            for linha in linhas:
                arquivo.write(linha + "\n")
        return True
    except OSError:
        print(f"Erro: não foi possível gravar {caminho}.")
        return False


def gerar_laudo(dados_garoa):
    """Mostra o laudo do mês de uma casa e oferece salvar em arquivo de texto."""
    print("\nLAUDO DO MÊS")
    casa = escolher_casa(dados_garoa)
    if casa is None:
        return None
    mes = entrada.ler_mes("Mês (AAAA-MM): ")
    leituras_mes = dados.leituras_do_mes(dados_garoa, casa["nome"], mes)
    if len(leituras_mes) == 0:
        print(f"\nNenhuma leitura de {casa['nome']} em {mes}.")
        return None

    linhas = montar_laudo(casa, mes, leituras_mes)
    print()
    for linha in linhas:
        print(linha)

    if entrada.ler_sim_nao("\nSalvar o laudo em arquivo de texto? (s/n): "):
        numero = dados_garoa["casas"].index(casa) + 1
        caminho = dados.caminho_laudo(mes, numero)
        if gravar_laudo(caminho, linhas):
            print(f"OK: laudo salvo em {caminho}.")
    return linhas


def mostrar_historico(dados_garoa):
    """Mostra todas as leituras de um cômodo numa tabela."""
    print("\nHISTÓRICO DO CÔMODO")
    escolha = escolher_comodo(dados_garoa)
    if escolha is None:
        return 0
    casa, comodo = escolha
    leituras = dados.leituras_do_comodo(dados_garoa, casa["nome"], comodo)
    if len(leituras) == 0:
        print(f"\n{comodo} ainda não tem leituras.")
        return 0

    print(f"\n{comodo} ({casa['nome']})")
    print(f"{'Data':<11} {'Ar °C':>6} {'UR %':>5} {'Parede':>6}"
          f" {'Orvalho':>7} {'UR par.':>7}  Estado")
    for leitura in leituras:
        print(f"{leitura['data']:<11} {formatar(leitura['temp_ar']):>6}"
              f" {formatar(leitura['ur_ar'], 0):>5}"
              f" {formatar(leitura['temp_parede']):>6} {formatar(leitura['orvalho']):>7}"
              f" {formatar(leitura['ur_parede']):>7}  {leitura['estado']}")
    print(f"Total: {len(leituras)} leitura(s)")
    return len(leituras)
