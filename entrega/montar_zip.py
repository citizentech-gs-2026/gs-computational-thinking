"""Gera entrega/garoa-python.zip com src/*.py, dados/garoa.json, prompt.md e readme.md.

Rode da raiz do projeto: python3 entrega/montar_zip.py
"""

import zipfile

CAMINHO_ZIP = "entrega/garoa-python.zip"

# (arquivo no repositório, nome dentro do ZIP)
ARQUIVOS = (
    ("src/main.py", "src/main.py"),
    ("src/menu.py", "src/menu.py"),
    ("src/calculos.py", "src/calculos.py"),
    ("src/entrada.py", "src/entrada.py"),
    ("src/dados.py", "src/dados.py"),
    ("dados/garoa.json", "dados/garoa.json"),
    ("prompt.md", "prompt.md"),
    ("README.md", "readme.md"),
)


def montar_zip(caminho_zip, arquivos):
    """Grava o ZIP com a lista de arquivos e devolve os nomes que entraram."""
    nomes = []
    with zipfile.ZipFile(caminho_zip, "w", zipfile.ZIP_DEFLATED) as pacote:
        for origem, destino in arquivos:
            pacote.write(origem, destino)
            nomes.append(destino)
    return nomes


def conferir_zip(caminho_zip):
    """Confere se o ZIP só tem .py, o JSON, prompt.md e readme.md; devolve True se está certo."""
    certo = True
    with zipfile.ZipFile(caminho_zip) as pacote:
        for nome in pacote.namelist():
            permitido = nome.endswith(".py") or nome in ("dados/garoa.json", "prompt.md", "readme.md")
            if not permitido or "__pycache__" in nome:
                print(f"  NÃO DEVIA ESTAR NO ZIP: {nome}")
                certo = False
            else:
                print(f"  {nome}")
    return certo


if __name__ == "__main__":
    montar_zip(CAMINHO_ZIP, ARQUIVOS)
    print(f"Conteúdo de {CAMINHO_ZIP}:")
    if conferir_zip(CAMINHO_ZIP):
        print("ZIP pronto para enviar no Teams.")
    else:
        print("Atenção: o ZIP tem arquivos que não deviam estar lá.")
