import sys
import argparse
import config
import translator
import utils

version = "1.4.1"

def Menu():
    utils.Clear()
    base_color = config.Basecolor
    menu = r"""
 ██████╗ ██╗████████╗
 ██╔══██╗██║╚══██╔══╝
 ██║  ██║██║   ██║   
 ██║  ██║██║   ██║   
 ██████╔╝██║   ██║   
 ╚═════╝ ╚═╝   ╚═╝   
 ██████╗ ██╗     ███████╗██╗  ██╗
 ██╔══██╗██║     ██╔════╝╚██╗██╔╝
 ██████╔╝██║     █████╗   ╚███╔╝ 
 ██╔═══╝ ██║     ██╔══╝   ██╔██╗ 
 ██║     ███████╗███████╗██╔╝ ██╗
 ╚═╝     ╚══════╝╚══════╝╚═╝  ╚═╝

 ==================================

   1. Transmitir  (Texto -> Morse)
   2. Decodificar (Morse -> Texto)
   3. Configurar
   4. Sair

 ==================================
"""
    print(f"{base_color}{menu}{config.RESET}")

def Menu_colors():
    base_color = config.Basecolor
    nomes = {
        "1": "Verde", "2": "Vermelho", "3": "Azul",
        "4": "Amarelo", "5": "Ciano", "6": "Roxo"
    }
    print(f"{base_color} =================================={config.RESET}")
    print(f"{base_color}        ESCOLHA UMA COR{config.RESET}")
    print(f"{base_color} =================================={config.RESET}\n")
    for numero, nome in nomes.items():
        cor = config.colors[numero]
        print(f"   {numero}. {cor}{nome}{config.RESET}")
    print(f"\n{base_color} =================================={config.RESET}")

def Mode(option):
    if option == 1:
        utils.Clear()
        text = input("Digite o texto: ")
        translate = translator.Morse(text)
        print("\nResultado:", translate)
        
        escolha = input("\nDeseja Copiar o resultado?(s/n): ").strip().lower()
        if escolha == "s":
            if utils.Copy(translate):
                print("Código Morse copiado para a área de transferência!")
            else:
                utils.Error("Erro: Nenhuma área de transferência detectada ou suportada no sistema.")
        input("\nPressione Enter para continuar...")

    elif option == 2:
        utils.Clear()
        text = input("Digite o código Morse (separe letras por espaço e palavras por /): ")
        translate = translator.MinT(text)
        print("\nResultado:", translate)
        
        escolha = input("\nDeseja Copiar o resultado?(s/n): ").strip().lower()
        if escolha == "s":
            if utils.Copy(translate):
                print("Texto copiado para a área de transferência!")
            else:
                utils.Error("Erro: Nenhuma área de transferência detectada ou suportada no sistema.")
        input("\nPressione Enter para continuar...")

    elif option == 3:
        utils.Clear()
        Menu_colors()
        escolha = input("Selecione a cor: ").strip()
        if escolha in config.colors:
            config.Basecolor = config.colors[escolha]
            if config.Save(escolha):
                print("Cor atualizada!")
            else:
                utils.Error("Cor aplicada, mas não foi possível salvar a configuração.")
        else:
            utils.Error("Cor inválida.")
        input("\nPressione Enter para continuar...")
    elif option == 4:
        sys.exit()
    else:
        utils.Error("Esse modo não existe, tente novamente")
        input("\nPressione Enter para tentar novamente...")

class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        utils.Error(f"Erro: {message}")
        sys.exit(1)

def Parser():
    parser = ArgParser(prog="DitPlex", add_help=False, allow_abbrev=False)
    parser.add_argument("-t", "--text", action="store_true")
    parser.add_argument("-m", "--morse", action="store_true")
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-h", "--help", action="store_true")
    return parser

def Split(argv):
    for i, arg in enumerate(argv):
        if arg in ("-t", "--text", "-m", "--morse"):
            return argv[:i + 1], " ".join(argv[i + 1:]).strip()
    return argv, ""

def Help():
    base_color = config.Basecolor
    print(f"{base_color}Uso:{config.RESET} DitPlex [opção] [conteúdo]\n")
    print(f"{base_color}Opções disponíveis:{config.RESET}")
    print(f"  {base_color}-t, --text{config.RESET} <texto>    Converte texto em código Morse.")
    print(f"  {base_color}-m, --morse{config.RESET} <morse>   Converte código Morse em texto.")
    print(f"  {base_color}-v, --version{config.RESET}          Exibe metadados, sistema e versão do aplicativo.")
    print(f"  {base_color}-h, --help{config.RESET}             Exibe este menu de ajuda.")

def CLI(argv=None):
    flags, content = Split(sys.argv[1:] if argv is None else argv)
    args, extras = Parser().parse_known_args(flags)

    if args.version:
        base_color = config.Basecolor
        print(f"{base_color}[Version]:{config.RESET} {version} {base_color}[OS/Arch]:{config.RESET} {utils.System()}/{utils.arch} {base_color}[License]:{config.RESET} MIT")
        sys.exit(0)
    if args.help:
        Help()
        sys.exit(0)
    if extras:
        utils.Error(f"Opção desconhecida: '{extras[0]}'. Use --help ou -h para ver as opções disponíveis.")
        sys.exit(1)
    if args.text:
        if content:
            print(translator.Morse(content))
            sys.exit(0)
        utils.Error("Erro: Faltou informar o texto. Exemplo: DitPlex -t \"SOS\"")
        sys.exit(1)
    if args.morse:
        if content:
            print(translator.MinT(content))
            sys.exit(0)
        utils.Error("Erro: Faltou informar o código Morse. Exemplo: DitPlex -m \"... --- ...\"")
        sys.exit(1)

if __name__ == "__main__":
    CLI()
    try:
        while True:
            Menu()
            option = input("Selecione o Modo: ")
            option = utils.Number(option)
            Mode(option)
    except KeyboardInterrupt:
        sys.exit(0)