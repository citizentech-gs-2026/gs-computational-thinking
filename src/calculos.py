"""Contas da Garoa: ponto de orvalho, umidade na parede, estado e janela."""

import math

# Constantes da fórmula de Magnus (B em °C)
MAGNUS_A = 17.62
MAGNUS_B = 243.12

# Faixas em que uma leitura é possível (mínimo, máximo)
FAIXA_TEMPERATURA = (-10.0, 60.0)
FAIXA_UMIDADE = (0.0, 100.0)

# Limites da umidade na parede: (ATENÇÃO a partir de, RISCO a partir de)
LIMITES_PAREDE = (70.0, 80.0)

# Abaixo desta umidade do ar, o ar está seco demais para a saúde
LIMITE_AR_SECO = 30.0

# Folga, em g/m³, para dizer se abrir a janela faz diferença
FOLGA_JANELA = 0.5

# Estados possíveis de um cômodo
ESTADOS = ("SECO", "ATENÇÃO", "RISCO", "CONDENSAÇÃO", "SENSOR")


def pressao_saturacao(temperatura):
    """Devolve a pressão de saturação do vapor (hPa) na temperatura dada."""
    return 6.112 * math.exp(MAGNUS_A * temperatura / (MAGNUS_B + temperatura))


def ponto_de_orvalho(temperatura, umidade):
    """Devolve a temperatura (°C) em que o ar começa a virar água."""
    gama = math.log(umidade / 100) + MAGNUS_A * temperatura / (MAGNUS_B + temperatura)
    return MAGNUS_B * gama / (MAGNUS_A - gama)


def umidade_na_parede(temp_ar, umidade_ar, temp_parede):
    """Devolve a umidade relativa (%) do ar encostado na parede, no máximo 100."""
    umidade = umidade_ar * pressao_saturacao(temp_ar) / pressao_saturacao(temp_parede)
    return min(umidade, 100.0)


def umidade_absoluta(temperatura, umidade):
    """Devolve quantos gramas de água há em cada m³ de ar."""
    vapor = umidade / 100 * pressao_saturacao(temperatura)
    return 216.7 * vapor / (273.15 + temperatura)


def dentro_da_faixa(valor, faixa):
    """Diz se o valor está entre o mínimo e o máximo da faixa (tupla)."""
    minimo, maximo = faixa
    return minimo <= valor <= maximo


def leitura_possivel(temp_ar, umidade_ar, temp_parede):
    """Diz se os três números podem ter vindo de um sensor funcionando."""
    if not dentro_da_faixa(temp_ar, FAIXA_TEMPERATURA):
        return False
    if not dentro_da_faixa(temp_parede, FAIXA_TEMPERATURA):
        return False
    # Umidade 0% não existe no ar de uma casa e quebraria o logaritmo
    return 0 < umidade_ar <= FAIXA_UMIDADE[1]


def classificar(temp_ar, umidade_ar, temp_parede):
    """Devolve um dicionário com orvalho, umidade na parede e estado da leitura."""
    if not leitura_possivel(temp_ar, umidade_ar, temp_parede):
        return {"orvalho": None, "ur_parede": None, "estado": "SENSOR"}

    orvalho = ponto_de_orvalho(temp_ar, umidade_ar)
    ur_parede = umidade_na_parede(temp_ar, umidade_ar, temp_parede)
    limite_atencao, limite_risco = LIMITES_PAREDE

    if temp_parede <= orvalho:
        estado = "CONDENSAÇÃO"
    elif ur_parede >= limite_risco:
        estado = "RISCO"
    elif ur_parede >= limite_atencao:
        estado = "ATENÇÃO"
    else:
        estado = "SECO"

    return {"orvalho": round(orvalho, 2), "ur_parede": round(ur_parede, 1), "estado": estado}


def ar_seco(umidade_ar):
    """Diz se o ar está seco demais (abaixo de 30%)."""
    return umidade_ar < LIMITE_AR_SECO


def decidir_janela(temp_dentro, ur_dentro, temp_fora, ur_fora):
    """Devolve (umidade absoluta dentro, fora, decisão ABRIR/FECHAR/TANTO FAZ)."""
    dentro = umidade_absoluta(temp_dentro, ur_dentro)
    fora = umidade_absoluta(temp_fora, ur_fora)

    if fora < dentro - FOLGA_JANELA:
        decisao = "ABRIR"
    elif fora > dentro + FOLGA_JANELA:
        decisao = "FECHAR"
    else:
        decisao = "TANTO FAZ"

    return (dentro, fora, decisao)
