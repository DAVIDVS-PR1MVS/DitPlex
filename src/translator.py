import unicodedata

morse = [
    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
    ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
    "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..",
    "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.",
    ".-.-.-", "--..--", "..--..", ".----.", "-.-.--", "-.--.", "-.--.-", ".-...", "---...", "-.-.-.", "-...-", ".-.-.", "-....-", "..--.-", ".-..-.", "...-..-", ".--.-."
]
letters = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', "0", "1", "2", "3", "4", "5", "6", "7", "8", "9",
    ".", ",", "?", "'", "!", "(", ")", "&", ":", ";", "=", "+", "-", "_", '"', "$", "@"
]
key = dict(zip(letters, morse))
key2 = dict(zip(morse, letters))

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