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
    result=[]
    best_similarity = 0

    for x in temp:
        best_match = x
        if x not in word:
            for y in word:
                t = 0
                if len(x) >= len(y):
                    for j in range(len(y)):
                        if x[j] == y[j]:
                            t += 1
                        elif x[j] in y:
                            l = y.find(x[j])
                            if j - l == 1:
                                t += 1
                elif len(x) < len(y):
                    for j in range(len(x)):
                        if x[j] == y[j]:
                            t += 1
                        elif x[j] in y:
                            l = y.find(x[j])
                            if l - j == 1:
                                t += 1

                k = t / len(y) * 100
                h = t / len(x) * 100

                if k >= 50 and h >= 50:
                    if k + h > best_similarity:
                        best_similarity = k + h
                        best_match = y

        result.append(best_match)

    return " ".join(result)

def possible(word_input, word=data(), similarity_threshold=50):
    word_input = word_input.lower()
    possible_matches = []

    if word_input not in word:
        for y in word:
            t = 0
            if len(word_input) >= len(y):
                for j in range(len(y)):
                    if word_input[j] == y[j]:
                        t += 1
                    elif word_input[j] in y:
                        l = y.find(word_input[j])
                        if j - l == 1:
                            t += 1
            elif len(word_input) < len(y):
                for j in range(len(word_input)):
                    if word_input[j] == y[j]:
                        t += 1
                    elif word_input[j] in y:
                        l = y.find(word_input[j])
                        if l - j == 1:
                            t += 1

            k = t / len(y) * 100
            h = t / len(word_input) * 100

            if k >= similarity_threshold and h >= similarity_threshold:
                possible_matches.append((y, k + h))

    unique_matches = list({match[0]: match for match in possible_matches}.values())
    unique_matches.sort(key=lambda match: match[1], reverse=True)

    return [match[0] for match in unique_matches[:5]]

if __name__=="__main__":
    pass
