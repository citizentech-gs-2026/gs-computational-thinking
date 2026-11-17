"""Leitura e validação do que o usuário digita: a pergunta se repete até a resposta ser válida."""

# Dias de cada mês, de janeiro a dezembro (fevereiro é ajustado no ano bissexto)
DIAS_POR_MES = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)

# Anos aceitos nas datas
FAIXA_ANO = (2000, 2100)


def ler_texto(pergunta):
    """Pede um texto e repete enquanto vier vazio."""
    while True:
        texto = input(pergunta).strip()
        if texto != "":
            return texto
        print("  Não pode ficar vazio. Tente de novo.")


def ler_float(pergunta, minimo, maximo):
    """Pede um número decimal entre minimo e maximo e repete até ser válido."""
    while True:
        texto = input(pergunta).strip().replace(",", ".")
        try:
            numero = float(texto)
        except ValueError:
            print("  Digite um número (por exemplo 22,5).")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"  O valor precisa estar entre {minimo:g} e {maximo:g}.")


def ler_inteiro(pergunta, minimo, maximo):
    """Pede um número inteiro entre minimo e maximo e repete até ser válido."""
    while True:
        texto = input(pergunta).strip()
        try:
            numero = int(texto)
        except ValueError:
            print("  Digite só o número da opção.")
            continue
        if minimo <= numero <= maximo:
            return numero
        print(f"  Escolha um número de {minimo} a {maximo}.")


def ler_sim_nao(pergunta):
    """Pede s ou n e devolve True para sim."""
    while True:
        resposta = input(pergunta).strip().lower()
        match resposta:
            case "s" | "sim":
                return True
            case "n" | "nao" | "não":
                return False
            case _:
                print("  Responda s ou n.")


def ano_bissexto(ano):
    """Diz se o ano tem 29 de fevereiro."""
    return ano % 4 == 0 and (ano % 100 != 0 or ano % 400 == 0)


def dias_no_mes(ano, mes):
    """Devolve quantos dias tem o mês daquele ano."""
    if mes == 2 and ano_bissexto(ano):
        return 29
    return DIAS_POR_MES[mes - 1]


def converter_mes(texto):
    """Converte AAAA-MM em (ano, mes), ou devolve None se for inválido."""
    partes = texto.split("-")
    if len(partes) != 2 or len(partes[0]) != 4 or len(partes[1]) != 2:
        return None
    try:
        ano = int(partes[0])
        mes = int(partes[1])
    except ValueError:
        return None
    if ano < FAIXA_ANO[0] or ano > FAIXA_ANO[1] or mes < 1 or mes > 12:
        return None
    return (ano, mes)


def data_valida(texto):
    """Diz se o texto é uma data AAAA-MM-DD que existe no calendário."""
    partes = texto.split("-")
    if len(partes) != 3 or len(partes[2]) != 2:
        return False
    ano_mes = converter_mes(partes[0] + "-" + partes[1])
    if ano_mes is None:
        return False
    try:
        dia = int(partes[2])
    except ValueError:
        return False
    ano, mes = ano_mes
    return 1 <= dia <= dias_no_mes(ano, mes)


def ler_data(pergunta):
    """Pede uma data AAAA-MM-DD e repete até ser uma data que existe."""
    while True:
        texto = input(pergunta).strip()
        if data_valida(texto):
            return texto
        print("  Data inválida. Use AAAA-MM-DD, por exemplo 2026-11-19.")


def ler_mes(pergunta):
    """Pede um mês AAAA-MM e repete até ser válido."""
    while True:
        texto = input(pergunta).strip()
        if converter_mes(texto) is not None:
            return texto
        print("  Mês inválido. Use AAAA-MM, por exemplo 2026-11.")


def escolher_da_lista(titulo, opcoes):
    """Mostra uma lista numerada e devolve o item escolhido (ou None se a lista estiver vazia)."""
    if len(opcoes) == 0:
        return None
    print(f"\n{titulo}")
    for indice in range(len(opcoes)):
        print(f"  {indice + 1}. {opcoes[indice]}")
    escolha = ler_inteiro("Número: ", 1, len(opcoes))
    return opcoes[escolha - 1]
