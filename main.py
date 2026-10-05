import os
import sys
import argparse
import config
import files
import translator
import utils

version = "1.5.0"

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
    parser.add_argument("-c", "--copy", action="store_true")
    parser.add_argument("-f", "--file")
    parser.add_argument("-o", "--output", nargs="?", const="")
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
    print(f"  {base_color}-t, --text{config.RESET} <texto>       Converte texto em código Morse.")
    print(f"  {base_color}-m, --morse{config.RESET} <morse>      Converte código Morse em texto.")
    print(f"  {base_color}-f, --file{config.RESET} <arquivo>     Converte um arquivo .txt (detecta Morse ou texto).")
    print(f"  {base_color}-o, --output{config.RESET} [arquivo]   Salva o resultado em arquivo (sem nome: dados_<data>.txt).")
    print(f"  {base_color}-c, --copy{config.RESET}               Copia o resultado para a área de transferência.")
    print(f"  {base_color}-v, --version{config.RESET}            Exibe metadados, sistema e versão do aplicativo.")
    print(f"  {base_color}-h, --help{config.RESET}               Exibe este menu de ajuda.")
    print(f"\n{base_color}Dica:{config.RESET} coloque -c e -o antes de -t ou -m.")

def Copy_result(result):
    if utils.Copy(result):
        print("Copiado para a área de transferência!", file=sys.stderr)
    else:
        utils.Error("Erro: Nenhuma área de transferência detectada ou suportada no sistema.")
        sys.exit(1)

def Save_file(path, result):
    if path == "":
        path = files.Default_name()
    if os.path.exists(path):
        try:
            answer = input(f"O arquivo '{path}' já existe. Sobrescrever? (s/n): ").strip().lower()
        except EOFError:
            answer = "n"
        if answer != "s":
            utils.Error("Operação cancelada: o arquivo não foi alterado.")
            sys.exit(1)
    if files.Write(path, result):
        print(f"Salvo em: {path}", file=sys.stderr)
    else:
        utils.Error(f"Erro: Não foi possível gravar o arquivo '{path}'.")
        sys.exit(1)

def Deliver(result, args):
    if args.output is None:
        print(result)
    else:
        Save_file(args.output, result)
    if args.copy:
        Copy_result(result)

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
    if args.file and (args.text or args.morse):
        utils.Error("Erro: -f não combina com -t ou -m, o sentido da conversão é detectado sozinho.")
        sys.exit(1)
    if (args.copy or args.output is not None) and not (args.text or args.morse or args.file):
        utils.Error("Erro: -c e -o precisam de -t, -m ou -f. Exemplo: DitPlex -c -t \"SOS\"")
        sys.exit(1)
    if args.file:
        text = files.Read(args.file)
        if text is None:
            utils.Error(f"Erro: Não foi possível ler o arquivo '{args.file}'.")
            sys.exit(1)
        if not text.strip():
            utils.Error(f"Erro: O arquivo '{args.file}' está vazio.")
            sys.exit(1)
        Deliver(translator.Convert(text), args)
        sys.exit(0)
    if args.text:
        if content:
            Deliver(translator.Morse(content), args)
            sys.exit(0)
        utils.Error("Erro: Faltou informar o texto. Exemplo: DitPlex -t \"SOS\"")
        sys.exit(1)
    if args.morse:
        if content:
            Deliver(translator.MinT(content), args)
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