"""Garoa: programa de terminal que avisa antes de o mofo aparecer. Rode da raiz: python3 src/main.py"""

import dados
import menu


def executar_opcao(opcao, dados_garoa):
    """Chama a função da opção escolhida e devolve False quando é para sair."""
    match opcao:
        case "1":
            menu.cadastrar_casa(dados_garoa)
        case "2":
            menu.cadastrar_comodo(dados_garoa)
        case "3":
            menu.registrar_leitura(dados_garoa)
        case "4":
            menu.ver_estado(dados_garoa)
        case "5":
            menu.abrir_janela()
        case "6":
            menu.gerar_laudo(dados_garoa)
        case "7":
            menu.mostrar_historico(dados_garoa)
        case "0":
            return False
        case _:
            print("Opção inexistente. Digite um número de 0 a 7.")
    return True


def main():
    """Carrega os dados e mantém o menu aberto até o usuário sair."""
    menu.mostrar_titulo()
    dados_garoa = dados.carregar_dados(dados.CAMINHO_DADOS)
    print(f"{len(dados_garoa['casas'])} casa(s) e {len(dados_garoa['leituras'])} leitura(s) carregadas.")

    continuar = True
    while continuar:
        menu.mostrar_menu()
        opcao = input("Escolha uma opção: ").strip()
        continuar = executar_opcao(opcao, dados_garoa)
    print("\nAté logo! Seus dados estão guardados em", dados.CAMINHO_DADOS)


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n\nPrograma encerrado. O que já foi gravado continua salvo.")
