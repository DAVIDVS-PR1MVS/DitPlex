#!/usr/bin/env python3
"""
Script de automação de compilação otimizada para o DitPlex.
Suporta isolamento via venv, exclusão de módulos desnecessários e localização dinâmica da raiz do projeto.
"""

import argparse
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

# Habilita suporte a cores ANSI no terminal Windows
if sys.platform == "win32":
    os.system("")


class Style:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    CYAN = "\033[96m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"


def print_banner():
    banner = f"""
{Style.CYAN}{Style.BOLD}=============================================================
                  DitPlex • Build Utility                     
============================================================={Style.RESET}"""
    print(banner)


def print_step(title: str, detail: str = ""):
    detail_fmt = f" {Style.DIM}({detail}){Style.RESET}" if detail else ""
    print(f"{Style.CYAN}[+] {Style.BOLD}{title}{Style.RESET}{detail_fmt}")


def print_success(message: str):
    print(f"{Style.GREEN}[V] {message}{Style.RESET}")


def print_warning(message: str):
    print(f"{Style.YELLOW}[!] {message}{Style.RESET}")


def print_error(message: str):
    print(f"{Style.RED}[X] {message}{Style.RESET}")


def run_command(cmd, env=None):
    print_step("Iniciando processo do PyInstaller", " ".join(cmd))
    result = subprocess.run(cmd, env=env)
    if result.returncode != 0:
        print_error(f"Falha na compilação. Código de saída: {result.returncode}")
        sys.exit(result.returncode)


def setup_isolated_venv(venv_dir: Path) -> Path:
    if venv_dir.exists():
        shutil.rmtree(venv_dir, ignore_errors=True)

    print_step("Criando ambiente virtual isolado", venv_dir.name)
    subprocess.run([sys.executable, "-m", "venv", str(venv_dir)], check=True)

    if sys.platform == "win32":
        python_exe = venv_dir / "Scripts" / "python.exe"
        pyinstaller_exe = venv_dir / "Scripts" / "pyinstaller.exe"
    else:
        python_exe = venv_dir / "bin" / "python"
        pyinstaller_exe = venv_dir / "bin" / "pyinstaller"

    print_step("Instalando dependências em ambiente isolado", "pyinstaller, platformdirs")
    subprocess.run(
        [str(python_exe), "-m", "pip", "install", "--quiet", "pyinstaller", "platformdirs"],
        check=True
    )

    return pyinstaller_exe


def clean_artifacts(root_dir: Path, name: str):
    print_step("Removendo artefatos e arquivos temporários de compilação")
    for folder in ["build", ".build_venv"]:
        path = root_dir / folder
        if path.exists():
            shutil.rmtree(path, ignore_errors=True)

    spec_file = root_dir / f"{name}.spec"
    if spec_file.exists():
        spec_file.unlink()


def main():
    print_banner()
    start_time = time.time()

    parser = argparse.ArgumentParser(
        description="Utilitário avançado de compilação otimizada para o DitPlex."
    )
    parser.add_argument(
        "--source",
        type=str,
        default="src/main.py",
        help="Caminho do código-fonte relativo à raiz (Padrão: src/main.py)"
    )
    parser.add_argument(
        "--name",
        type=str,
        default="DitPlex",
        help="Nome final do arquivo executável (Padrão: DitPlex)"
    )
    parser.add_argument(
        "--icon",
        type=str,
        default="assets/icon.ico",
        help="Caminho para o ícone .ico relativo à raiz (Padrão: assets/icon.ico)"
    )
    parser.add_argument(
        "--isolated",
        action="store_true",
        help="Gera o executável utilizando um venv limpo para reduzir o tamanho"
    )
    parser.add_argument(
        "--clean",
        action="store_true",
        help="Limpa compilações anteriores antes de iniciar"
    )

    args = parser.parse_args()

    current = Path(__file__).resolve().parent
    if (current / "src").exists():
        root_dir = current
    elif (current.parent / "src").exists():
        root_dir = current.parent
    else:
        root_dir = current.parent.parent

    source_path = root_dir / args.source
    icon_path = root_dir / args.icon

    if not source_path.exists():
        print_error(f"Arquivo fonte '{args.source}' não foi encontrado em '{source_path}'.")
        sys.exit(1)

    if args.clean and (root_dir / "dist").exists():
        print_step("Limpando compilações anteriores", "dist/")
        shutil.rmtree(root_dir / "dist", ignore_errors=True)

    if args.isolated:
        venv_dir = root_dir / ".build_venv"
        pyinstaller_bin = setup_isolated_venv(venv_dir)
    else:
        pyinstaller_bin = Path("pyinstaller")

    cmd = [
        str(pyinstaller_bin),
        "--onefile",
        "--clean",
        f"--name={args.name}"
    ]

    if icon_path.exists():
        cmd.append(f"--icon={str(icon_path)}")
    else:
        print_warning(f"Ícone não encontrado em '{icon_path}'. O build continuará sem ícone.")

    # Exclusões seguras para manter a estabilidade da biblioteca padrão do Python
    excluded_modules = [
        "tkinter", "unittest", "pydoc", "sqlite3",
        "setuptools", "pkg_resources", "distutils", "_distutils_hack",
        "email", "http", "xml", "ssl", "asyncio", "multiprocessing",
        "doctest", "pdb", "test"
    ]
    for module in excluded_modules:
        cmd.append(f"--exclude-module={module}")

    if sys.platform.startswith("linux"):
        cmd.append("--strip")

    cmd.append(str(source_path))

    run_command(cmd)
    clean_artifacts(root_dir, args.name)

    elapsed_time = time.time() - start_time
    output_exe = root_dir / "dist" / (f"{args.name}.exe" if sys.platform == "win32" else args.name)

    file_size_mb = 0.0
    if output_exe.exists():
        file_size_mb = output_exe.stat().st_size / (1024 * 1024)

    print(f"\n{Style.GREEN}{Style.BOLD}=============================================================")
    print("                COMPILAÇÃO CONCLUÍDA COM SUCESSO             ")
    print(f"============================================================={Style.RESET}")
    print(f" Arquivo gerado : {Style.BOLD}{output_exe}{Style.RESET}")
    print(f" Tamanho final  : {Style.BOLD}{file_size_mb:.2f} MB{Style.RESET}")
    print(f" Tempo decorrido: {Style.BOLD}{elapsed_time:.2f} segundos{Style.RESET}\n")


if __name__ == "__main__":
    main()