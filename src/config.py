import os
import configparser
from platformdirs import user_config_dir

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

def Path():
    try:
        folder = user_config_dir("ditplex")
        os.makedirs(folder, exist_ok=True)
        return os.path.join(folder, "config.ini")
    except OSError:
        return None

configs = Path()

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

Basecolor = Data()