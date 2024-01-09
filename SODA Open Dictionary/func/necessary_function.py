import socket

def get_config():
    with open("func/setting/setting.txt", "r", encoding="utf-8") as fi:
        setting=fi.readlines()
    settings={}
    for index in setting:
        option, properties=index.strip().split(": ")
        settings[option]=properties
    
    return settings

def check_connection(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except:
        return False

def levenshtein_distance(s1, s2):
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

def data():
    try:
        with open("data/word.txt", encoding="utf-8") as fi:
            word = [str(i) for i in fi.read().split()]
    except:
        with open("func/data/word.txt", encoding="utf-8") as fi:
            word = [str(i) for i in fi.read().split()]

    return word

def spelling_checker_for_SOD(you, word=data()):

    you = you.lower()
    temp = [str(i) for i in you.split()]
    for x in temp:
        if x not in word:
            distances = {w: levenshtein_distance(x, w) for w in word}
            closest_word = min(distances, key=distances.get)
            you = you.replace(x, closest_word)

    return you

if __name__=="__main__":
    pass