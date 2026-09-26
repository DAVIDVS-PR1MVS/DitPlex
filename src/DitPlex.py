import os
import unicodedata
import re
import sys
import platform
import configparser
from platformdirs import user_config_dir
#///////////////////////
version = "1.4.0"
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
def Path():
    folder = user_config_dir("ditplex")
    os.makedirs(folder, exist_ok=True)
    return os.path.join(folder, "config.ini")
def Data():
    config = configparser.ConfigParser()
    if not os.path.exists(configs):
        config["SETTINGS"] = {"cor": "1"}
        with open(configs, "w", encoding="utf-8") as a:
            config.write(a)
        return colors["1"]

    config.read(configs, encoding="utf-8")
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
    "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----."
]
letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"
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
            config = configparser.ConfigParser()
            config["SETTINGS"] = {"cor": str(escolha)}
            with open(configs, "w", encoding="utf-8") as a:
                config.write(a)
            Basecolor = colors[escolha]
            print("Cor atualizada!")
        else:
            print("Cor inválida.3")
        input("\nPressione Enter para continuar...")
    elif option == 4:
        sys.exit()
    else:
        print("Esse modo Não existe, tente novamente")
        input("\nPressione Enter para tentar novamente...")
#///////////////////////
if len(sys.argv) > 1:
    arg = sys.argv[1].lower()

    if arg in ["--version", "-v"]:
        print(f"{Basecolor}[Version]:{RESET} {version} {Basecolor}[OS/Arch]:{RESET} {System()}/{arch} {Basecolor}[License]:{RESET} MIT")
        sys.exit(0)
    elif arg in ["--help", "-h"]:
        print(f"{Basecolor}Uso:{RESET} DitPlex [opção] [conteúdo]\n")
        print(f"{Basecolor}Opções disponíveis:{RESET}")
        print(f"  {Basecolor}-t, --text{RESET} <texto>   Converte texto em código Morse.")
        print(f"  {Basecolor}-m, --morse{RESET} <morse>   Converte código Morse em texto.")
        print(f"  {Basecolor}-v, --version{RESET}          Exibe metadados, sistema e versão do aplicativo.")
        print(f"  {Basecolor}-h, --help{RESET}          Exibe este menu de ajuda.")
        sys.exit(0)
    elif arg in ["--text", "-t"]:
        if len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
            translate = Morse(text)
            print(translate)
        else:
            print(f"Erro: Faltou informar o texto. Exemplo: DitPlex -t \"SOS\"")
            sys.exit(1)
        sys.exit(0)
    elif arg in ["--morse", "-m"]:
        if len(sys.argv) > 2:
            text = " ".join(sys.argv[2:])
            translate = MinT(text)
            print(translate)
        else:
            print(f"Erro: Faltou informar o código Morse. Exemplo: DitPlex -m \"... --- ...\"")
            sys.exit(1)
        sys.exit(0)
    else:
        print(f"Opção desconhecida: '{sys.argv[1]}'. Use --help ou -h para ver as opções disponíveis.")
        sys.exit(1)
#///////////////////////
if __name__=="__main__":
    try:
        while True:
            Menu()
            option = input("Selecione o Modo: ")
            option = Number(option)
            Mode(option)
    except KeyboardInterrupt:
        sys.exit(0)
#///////////////////////