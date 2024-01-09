try:
    from necessary_function import spelling_checker_for_SOD, check_connection, data as word_data
except:
    from func.necessary_function import spelling_checker_for_SOD, check_connection, data as word_data
from googletrans import Translator
import re

translator=Translator()

def SOD_word_list():
    try:
        with open("data/tu_dien_nguon.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        with open("func/data/tu_dien_nguon.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

    tu_dien = []
    for line in lines:
        try:
            word, wordtype, definition, translation, synonyms, level = line.strip().split(" % ")
            tu_dien.append({"word": word, "type": wordtype, "definition": definition, "translation": translation, "level": level})
        except:
            pass
    return tu_dien

def data():
    try:
        with open("data/tu_dien_nguon.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        with open("func/data/tu_dien_nguon.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

    tu_dien = []
    for line in lines:
        word, wordtype, definition, translation, synonyms, level = line.strip().split(" % ")
        temp={"word": word, "type": wordtype, "definition": definition, "translation": translation, "level": level}
        if synonyms!="none":
            temp["synonyms"]=synonyms.split(", ")
        else:
            temp["synonyms"]=synonyms
        tu_dien.append(temp)
    
    return tu_dien

def SOD(inp, internet_required=True, boost_performance=False, tu_dien=data(), word=word_data()):
    if not boost_performance and internet_required and check_connection():
        try:
            if translator.detect(inp).lang=="en":
                inp=spelling_checker_for_SOD(" ".join(inp.split()), word=word)
            else:
                inp=translator.translate(text=inp).text.lower()
            for words in tu_dien:
                if (words["word"]==inp) or (words["definition"]==inp):
                    return words
        except:
            return "Không tìm thấy từ"
    else:
        if internet_required:
            inp=spelling_checker_for_SOD(" ".join(inp.split()), word=word)
        for words in tu_dien:
            if (words["word"]==inp):
                return words
    return "Không tìm thấy từ"
    
def rewrite(filepath):
    try:
        with open("data/tu_dien_nguon.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        with open("func/data/tu_dien_nguon.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

    tu_dien = []
    for line in lines:
        word, wordtype, definition, translation = line.strip().split(" % ")
        tu_dien.append({"word": word, "type": wordtype, "definition": definition, "translation": translation})

    with open(filepath, "w", encoding="utf-8") as fo:
        for i in tu_dien:
            fo.write(i["word"]+" ")

def rewrite_word_source(filepath):
    with open(filepath, encoding="utf-8") as fi:
        list_=fi.read().split()
    words=[i["word"] for i in SOD_word_list()]
    for word in words:
        if word not in list_:
            list_.append(word)

    with open(filepath, "w", encoding="utf-8") as fo:
        fo.write(" ".join(list_))

def grammar_structure_detector(inp,file_path):
    patterns=build_patterns(file_path)
    result=[]
    for i in patterns:
        if len(re.findall(patterns[i], inp))!=0:
            result.append(i.replace("\n",""))
    return result

def build_patterns(file_path):
    patterns = {}
    with open(file_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts,structure = line.split(": ")
            parts=parts.split('...')
            pattern = '.*?'.join(f'({part.strip()})' for part in parts)
            patterns[structure] = pattern
    return patterns

def word_detector(inp):
    inp = inp.split()
    list_ = []
    i = 0
    while i < len(inp):
        max_len_phrase = inp[i]
        for j in range(i, len(inp)):
            phrase = " ".join(inp[i:j+1])
            if SOD(phrase, internet_required=False, boost_performance=True) != "Không tìm thấy từ":
                if len(phrase) > len(max_len_phrase):
                    max_len_phrase = phrase
        if max_len_phrase not in list_:
            list_.append(max_len_phrase)
        i += len(max_len_phrase.split())
    return list_

if __name__=="__main__":
    pass