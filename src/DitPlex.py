import os
import unicodedata
import re
import sys
import argparse
import platform
import configparser
from platformdirs import user_config_dir
#///////////////////////
version = "1.4.1"
def System():
    try:
        return platform.freedesktop_os_release()["ID"]
    except (AttributeError, OSError):
        return platform.system()
arch = platform.machine()
#///////////////////////
colors = {
    "1": "\033[32m",    # Verde
    "2": "\033[31m",    # Vermelho
    "3": "\033[34m",    # Azul
    "4": "\033[33m",    # Amarelo
    "5": "\033[36m",    # Ciano
    "6": "\033[35m"     # Roxo
}
RESET = "\033[0m"
RED = colors["2"]
def Error(message):
    print(f"{RED}{message}{RESET}", file=sys.stderr)
def Path():
    try:
        folder = user_config_dir("ditplex")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, "config.ini")
    except OSError:
        return None
def Save(color):
    if configs is None:
        return False
    config = configparser.ConfigParser()
    config["SETTINGS"] = {"cor": str(color)}
    try:
        with open(configs, "w", encoding="utf-8") as a:
            config.write(a)
        return True
    except OSError:
        return False
def Data():
    if configs is None:
        return colors["1"]
    if not os.path.exists(configs):
        Save("1")
        return colors["1"]

    config = configparser.ConfigParser()
    try:
        config.read(configs, encoding="utf-8")
    except (OSError, configparser.Error):
        return colors["1"]
    color = config.get("SETTINGS", "cor", fallback="1").strip().upper()
    return colors.get(color, colors["1"])
configs = Path()
Basecolor = Data()
def Menu_colors():
    nomes = {
        "1": "Verde", "2": "Vermelho", "3": "Azul",
        "4": "Amarelo", "5": "Ciano", "6": "Roxo"
    }
    print(f"{Basecolor} =================================={RESET}")
    print(f"{Basecolor}        ESCOLHA UMA COR{RESET}")
    print(f"{Basecolor} =================================={RESET}\n")
    for numero, nome in nomes.items():
        cor = colors[numero]
        print(f"   {numero}. {cor}{nome}{RESET}")
    print(f"\n{Basecolor} =================================={RESET}")
#///////////////////////
morse = [
    #a-i (a, b, c, d, e, f, g, h, i)
    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
    #j-r (j, k, l, m, n, o, p, q, r)
    ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
    #s-z (s, t, u, v, w, x, y, z)
    "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..",
    #0-9
    "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.",
    #símbolos (. , ? ' ! ( ) & : ; = + - _ " $ @)
    ".-.-.-", "--..--", "..--..", ".----.", "-.-.--", "-.--.", "-.--.-", ".-...", "---...", "-.-.-.", "-...-", ".-.-.", "-....-", "..--.-", ".-..-.", "...-..-", ".--.-."
]
letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ".", ",", "?", "'", "!", "(", ")", "&", ":", ";", "=", "+", "-", "_", '"', "$", "@"
]
key = dict(zip(letters, morse))
key2 = dict(zip(morse, letters))
#///////////////////////
def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')
def Menu():
    Clear()

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
    print(f"{Basecolor}{menu}{RESET}")
#///////////////////////
def Upper(text):
    nfkd = unicodedata.normalize("NFKD", text.upper())
    return ''.join([c for c in nfkd if not unicodedata.combining(c)])
def Morse(text):
    less = Upper(text)
    translate = []
    for caractere in less:
        if caractere in key:
            translate.append(key[caractere])
        elif caractere == " ":
            translate.append("/")
        else:
            translate.append(caractere)
    return " ".join(translate)
def MinT(text):
    translate = []
    for simbol in text.split(" "):
        if simbol in key2:
            translate.append(key2[simbol])
        elif simbol == "/":
            translate.append(" ")
        else:
            translate.append(simbol)
    return "".join(translate)
def Number(option):
    onlynumbers = re.sub(r"\D", "", option)
    return int(onlynumbers) if onlynumbers else 0
def Mode(option):
    if option == 1:
        Clear()
        text = input("Digite o texto: ")
        print("\nResultado:", Morse(text))
        input("\nPressione Enter para continuar...")
    elif option == 2:
        Clear()
        text = input("Digite o código Morse (separe letras por espaço e palavras por /): ")
        translate = MinT(text)
        print("\nResultado:", translate)
        input("\nPressione Enter para continuar...")
    elif option == 3:
        global Basecolor
        Clear()
        Menu_colors()
        escolha = input("Selecione a cor: ").strip()
        if escolha in colors:
            Basecolor = colors[escolha]
            if Save(escolha):
                print("Cor atualizada!")
            else:
                Error("Cor aplicada, mas não foi possível salvar a configuração.")
        else:
            Error("Cor inválida.")
        input("\nPressione Enter para continuar...")
    elif option == 4:
        sys.exit()
    else:
        Error("Esse modo não existe, tente novamente")
        input("\nPressione Enter para tentar novamente...")
#///////////////////////
class ArgParser(argparse.ArgumentParser):
    def error(self, message):
        Error(f"Erro: {message}")
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
    print(f"{Basecolor}Uso:{RESET} DitPlex [opção] [conteúdo]\n")
    print(f"{Basecolor}Opções disponíveis:{RESET}")
    print(f"  {Basecolor}-t, --text{RESET} <texto>    Converte texto em código Morse.")
    print(f"  {Basecolor}-m, --morse{RESET} <morse>   Converte código Morse em texto.")
    print(f"  {Basecolor}-v, --version{RESET}          Exibe metadados, sistema e versão do aplicativo.")
    print(f"  {Basecolor}-h, --help{RESET}             Exibe este menu de ajuda.")
def CLI(argv=None):
    flags, content = Split(sys.argv[1:] if argv is None else argv)
    args, extras = Parser().parse_known_args(flags)

    if args.version:
        print(f"{Basecolor}[Version]:{RESET} {version} {Basecolor}[OS/Arch]:{RESET} {System()}/{arch} {Basecolor}[License]:{RESET} MIT")
        sys.exit(0)
    if args.help:
        Help()
        sys.exit(0)
    if extras:
        Error(f"Opção desconhecida: '{extras[0]}'. Use --help ou -h para ver as opções disponíveis.")
        sys.exit(1)
    if args.text:
        if content:
            print(Morse(content))
            sys.exit(0)
        Error("Erro: Faltou informar o texto. Exemplo: DitPlex -t \"SOS\"")
        sys.exit(1)
    if args.morse:
        if content:
            print(MinT(content))
            sys.exit(0)
        Error("Erro: Faltou informar o código Morse. Exemplo: DitPlex -m \"... --- ...\"")
        sys.exit(1)
#///////////////////////
if __name__=="__main__":
    CLI()
    try:
        while True:
            Menu()
            option = input("Selecione o Modo: ")
            option = Number(option)
            Mode(option)
    except KeyboardInterrupt:
        sys.exit(0)
#///////////////////////