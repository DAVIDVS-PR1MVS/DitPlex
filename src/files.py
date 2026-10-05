from datetime import datetime

def Default_name():
    return datetime.now().strftime("dados_%Y-%m-%d_%H-%M-%S.txt")

def Read(path):
    try:
        with open(path, "r", encoding="utf-8-sig") as a:
            return a.read()
    except (OSError, UnicodeDecodeError):
        return None

def Write(path, text):
    try:
        with open(path, "w", encoding="utf-8") as a:
            a.write(text + "\n")
        return True
    except OSError:
        return False