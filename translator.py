import unicodedata

morse = [
    #a-i
    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..",
    #j-r
    ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.",
    #s-z
    "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--..",
    #0-9
    "-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...", "---..", "----.",
    #simbols
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
    
def IsMorse(text, threshold=0.90):
    text = "".join(text.split())
    if not text:
        return False
    morse = sum(1 for c in text if c in ".-/")
    return morse / len(text) >= threshold

def Convert(text):
    func = MinT if IsMorse(text) else Morse
    return "\n".join(func(line) for line in text.splitlines())