"""Leitura e gravação do arquivo dados/garoa.json e buscas nos dados."""

import json

# Caminho relativo: o programa é rodado da raiz do projeto (python3 src/main.py)
CAMINHO_DADOS = "dados/garoa.json"

# Campos que toda leitura guarda no JSON
CAMPOS_LEITURA = ("casa", "comodo", "data", "temp_ar", "ur_ar", "temp_parede",
                  "orvalho", "ur_parede", "estado")


def dados_vazios():
    """Devolve a estrutura de dados sem nenhuma casa nem leitura."""
    return {"casas": [], "leituras": []}


def estrutura_valida(dados):
    """Diz se o conteúdo lido do JSON tem as listas casas e leituras."""
    if type(dados) != dict:
        return False
    if type(dados.get("casas")) != list or type(dados.get("leituras")) != list:
        return False
    for casa in dados["casas"]:
        if type(casa) != dict or "nome" not in casa or type(casa.get("comodos")) != list:
            return False
    for leitura in dados["leituras"]:
        if type(leitura) != dict or not tem_campos(leitura, CAMPOS_LEITURA):
            return False
        if type(leitura["data"]) != str:
            return False
    return True


def tem_campos(dicionario, campos):
    """Diz se o dicionário tem todas as chaves da tupla campos."""
    for campo in campos:
        if campo not in dicionario:
            return False
    return True


def carregar_dados(caminho):
    """Lê o JSON; se faltar ou estiver corrompido, avisa e devolve dados vazios."""
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except FileNotFoundError:
        print(f"Aviso: {caminho} não foi encontrado. Começando sem dados.")
        return dados_vazios()
    except (ValueError, UnicodeDecodeError):
        print(f"Aviso: {caminho} está corrompido. Começando sem dados.")
        print("       Ao gravar algo novo, o arquivo será substituído.")
        return dados_vazios()
    except OSError:
        print(f"Aviso: não foi possível abrir {caminho}. Começando sem dados.")
        return dados_vazios()

    if not estrutura_valida(dados):
        print(f"Aviso: {caminho} não tem o formato da Garoa. Começando sem dados.")
        return dados_vazios()
    return dados


def salvar_dados(caminho, dados):
    """Grava os dados no JSON e devolve True se deu certo."""
    try:
        with open(caminho, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=2)
        return True
    except OSError:
        print(f"Erro: não foi possível gravar em {caminho}.")
        print("      Rode o programa a partir da pasta do projeto: python3 src/main.py")
        return False


def nomes_das_casas(dados):
    """Devolve a lista com o nome de cada casa cadastrada."""
    nomes = []
    for casa in dados["casas"]:
        nomes.append(casa["nome"])
    return nomes


def buscar_casa(dados, nome):
    """Devolve o dicionário da casa com esse nome (sem diferenciar maiúsculas) ou None."""
    for casa in dados["casas"]:
        if casa["nome"].lower() == nome.lower():
            return casa
    return None


def comodo_existe(casa, nome_comodo):
    """Diz se a casa já tem um cômodo com esse nome."""
    for comodo in casa["comodos"]:
        if comodo.lower() == nome_comodo.lower():
            return True
    return False


def leituras_do_comodo(dados, nome_casa, nome_comodo):
    """Devolve as leituras de um cômodo, da mais antiga para a mais nova."""
    encontradas = []
    for leitura in dados["leituras"]:
        if leitura["casa"] == nome_casa and leitura["comodo"] == nome_comodo:
            inserir_por_data(encontradas, leitura)
    return encontradas


def inserir_por_data(lista, leitura):
    """Coloca a leitura na lista mantendo a ordem por data (AAAA-MM-DD ordena como texto)."""
    posicao = len(lista)
    while posicao > 0 and lista[posicao - 1]["data"] > leitura["data"]:
        posicao = posicao - 1
    lista.insert(posicao, leitura)


def leituras_do_mes(dados, nome_casa, mes):
    """Devolve as leituras da casa cujo mês (data[:7]) é igual a AAAA-MM."""
    encontradas = []
    for leitura in dados["leituras"]:
        if leitura["casa"] == nome_casa and leitura["data"][:7] == mes:
            encontradas.append(leitura)
    return encontradas
