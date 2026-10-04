import os
import sys
import re
import platform
import shutil
import subprocess
from config import RED, RESET

def System():
    try:
        return platform.freedesktop_os_release()["ID"]
    except (AttributeError, OSError):
        return platform.system()

arch = platform.machine()

def Error(message):
    print(f"{RED}{message}{RESET}", file=sys.stderr)

def Clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def Number(option):
    onlynumbers = re.sub(r"\D", "", option)
    return int(onlynumbers) if onlynumbers else 0

def Copy(text):
    if os.name == "nt":
        cmd, data = ["clip"], text.encode("utf-16")
    elif platform.system() == "Darwin":
        cmd, data = ["pbcopy"], text.encode("utf-8")
    else:
        options = [["wl-copy"], ["xclip", "-selection", "clipboard"], ["xsel", "--clipboard", "--input"]]
        cmd = next((c for c in options if shutil.which(c[0])), None)
        if cmd is None:
            return False
        data = text.encode("utf-8")
    try:
        subprocess.run(cmd, input=data, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except (OSError, subprocess.CalledProcessError):
        return False