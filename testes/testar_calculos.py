"""Testes das contas da Garoa (fica fora do ZIP). Rode da raiz: python3 testes/testar_calculos.py"""

import sys

sys.path.insert(0, "src")

import calculos  # noqa: E402

# (ar °C, UR %, parede °C) -> (ponto de orvalho, UR na parede, estado)
CASOS_PAREDE = (
    ((22, 70, 17), (16.27, 95.5, "RISCO")),
    ((22, 70, 16), (16.27, 100.0, "CONDENSAÇÃO")),
    ((22, 50, 20), (11.09, 56.5, "SECO")),
    ((24, 65, 19), (17.01, 88.3, "RISCO")),
    ((22, 45, 21), (9.52, 47.8, "SECO")),
)

# (dentro T, UR, fora T, UR) -> (umidade absoluta dentro, fora, decisão)
CASOS_JANELA = (
    ((22, 70, 18, 60), (13.55, 9.20, "ABRIR")),
    ((22, 60, 20, 95), (11.62, 16.38, "FECHAR")),
    ((22, 60, 22, 58), (11.62, 11.23, "TANTO FAZ")),
)


def testar_parede():
    """Confere ponto de orvalho, umidade na parede e estado."""
    for entrada, esperado in CASOS_PAREDE:
        temp_ar, ur_ar, temp_parede = entrada
        orvalho, ur_parede, estado = esperado
        assert round(calculos.ponto_de_orvalho(temp_ar, ur_ar), 2) == orvalho, entrada
        assert round(calculos.umidade_na_parede(temp_ar, ur_ar, temp_parede), 1) == ur_parede, entrada
        resultado = calculos.classificar(temp_ar, ur_ar, temp_parede)
        assert resultado["estado"] == estado, (entrada, resultado)
        assert resultado["orvalho"] == orvalho, (entrada, resultado)
        assert resultado["ur_parede"] == ur_parede, (entrada, resultado)


def testar_janela():
    """Confere umidade absoluta e a decisão da janela."""
    for entrada, esperado in CASOS_JANELA:
        dentro, fora, decisao = calculos.decidir_janela(*entrada)
        assert round(dentro, 2) == esperado[0], (entrada, dentro)
        assert round(fora, 2) == esperado[1], (entrada, fora)
        assert decisao == esperado[2], (entrada, decisao)


def testar_limites():
    """Confere SENSOR, os limites 70/80 e o alerta de ar seco."""
    assert calculos.classificar(70, 50, 20)["estado"] == "SENSOR"
    assert calculos.classificar(22, 50, -15)["estado"] == "SENSOR"
    assert calculos.classificar(22, 0, 20)["estado"] == "SENSOR"
    assert calculos.classificar(22, 70, 22)["estado"] == "ATENÇÃO"
    assert calculos.classificar(22, 80, 22)["estado"] == "RISCO"
    assert calculos.ar_seco(29.9)
    assert not calculos.ar_seco(30)


if __name__ == "__main__":
    testar_parede()
    testar_janela()
    testar_limites()
    print("Todos os testes passaram.")
