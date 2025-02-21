try:
    from necessary_function import spelling_checker_for_SOD, check_connection, data as word_data
except:
    from func.necessary_function import spelling_checker_for_SOD, check_connection, data as word_data
from googletrans import Translator
import re, requests, json, threading

translator=Translator()

def SOD_word_list(path="data/tu_dien_nguon.txt", sub_path="func/data/tu_dien_nguon.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = f.read()
    except:
        with open(sub_path, "r", encoding="utf-8") as f:
            data = f.read()

    tu_dien = eval(data)
    
    return tu_dien

with open("func/data/source.txt", encoding="utf-8") as f: 
    source=eval(f.read())

def SOD(inp, database='default', database_path='default', get_database_from_path=True, internet=check_connection()):
    result = {}
    lock = threading.Lock()

    def fetch_word_data(word):
        nonlocal completed
        data_ = {}

        if database_path != 'default' and word in _database_:
            data_ = _database_[word]
        elif internet:
            url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
            try:
                response = requests.get(url)
            except:
                print(f"\rLỗi truy vấn: {word}", end="", flush=True)
            else:
                if response.status_code == 200:
                    data = response.json()
                    if isinstance(data, list):
                        for i in data:
                            word_data = i
                            meanings = word_data.get("meanings", "none")
                            for meaning in meanings:
                                part_of_speech = meaning.get("partOfSpeech", "none")
                                synonyms = meaning.get("synonyms", "none")
                                antonyms = meaning.get("antonyms", "none")
                                data_[part_of_speech] = {
                                    "definition": "",
                                    "synonyms": synonyms,
                                    "antonyms": antonyms
                                }
                                for definition in meaning.get("definitions", "none"):
                                    definition_text = definition.get("definition", "none")
                                    example = definition.get("example", [])
                                    example = f"\nE.g: {example}\n\n" if example else "\n\n"
                                    data_[part_of_speech]["definition"] += f"- {definition_text}{example}"
                                    data_[part_of_speech]["word"] = word
                                    data_[part_of_speech]["type"] = part_of_speech

                with lock:
                    if data_:
                        _database_.update({word: data_})
                        with open(database_path, "w", encoding="utf-8") as fo:
                            fo.write(json.dumps(_database_, ensure_ascii=False, indent=4))

        result[word] = data_ if data_ else "Không tìm thấy từ"

    _database_={}
    
    if database!='default': _database_.update(database)
    
    if database_path!='default' and get_database_from_path:
        with open(database_path, encoding="utf-8") as f:
            _database_.update(eval(f.read()))

    threads = []
    for word in inp:
        thread = threading.Thread(target=fetch_word_data, args=(word,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return result

def word_detector(inp):
    inp = inp.split()
    list_ = []
    i = 0
    while i < len(inp):
        max_len_phrase = inp[i]
        for j in range(i, len(inp)):
            phrase = " ".join(inp[i:j+1])
            if phrase in source:
                if len(phrase) > len(max_len_phrase):
                    max_len_phrase = phrase
        if max_len_phrase not in list_:
            list_.append(max_len_phrase)
        i += len(max_len_phrase.split())
    return list_
