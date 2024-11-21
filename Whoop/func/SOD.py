try:
    from necessary_function import spelling_checker_for_SOD, check_connection, data as word_data
except:
    from func.necessary_function import spelling_checker_for_SOD, check_connection, data as word_data
from googletrans import Translator
import re, requests

translator=Translator()

def SOD_word_list(path="data/tu_dien_nguon.txt", sub_path="func/data/tu_dien_nguon.txt"):
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = f.readlines()
    except:
        with open(sub_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

    tu_dien = {}
    for line in lines:
        word, wordtype, definition, translation, synonyms, level = line.strip().split(" % ")
        temp={"word": word, "type": wordtype, "definition": definition, "translation": translation, "level": level}
        if synonyms!="none":
            temp["synonyms"]=synonyms.split(", ")
        else:
            temp["synonyms"]=synonyms
        tu_dien[word] = temp
    
    return tu_dien

source={}
for i in SOD_word_list():
    source[i.lower()]=i

def SOD(inp):
    for word in inp:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        response = requests.get(url)
        
        data_={}
        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                word_data = data[0]
                meanings = word_data.get("meanings", "none")
                for meaning in meanings:
                    part_of_speech = meaning.get("partOfSpeech", "none")
                    synonyms = meaning.get("synonyms", "none")
                    antonyms = meaning.get("antonyms", "none")
                    data_[part_of_speech]={"definition": "", "synonyms": synonyms, "antonyms": antonyms}
                    for definition in meaning.get("definitions", "none"):
                        definition_text = definition.get("definition", "none")
                        example = definition.get("example", [])

                        if example==[]: example=2*"\n"
                        else: example=f"\nVí dụ: {example}\n\n"
                        data_[part_of_speech]["definition"]=data_[part_of_speech]["definition"]+f"- {definition_text}{example}"
    return data_ if data_ else "Không tìm thấy từ"

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
            pattern = '\s*.*?'.join(f'({part.strip()})' for part in parts)
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
            if phrase in source:
                if len(phrase) > len(max_len_phrase):
                    max_len_phrase = phrase
        if max_len_phrase not in list_:
            list_.append(max_len_phrase)
        i += len(max_len_phrase.split())
    return list_

if __name__=="__main__":
    print(SOD([input()]))

    