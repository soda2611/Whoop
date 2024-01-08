try:
    from necessary_function import spelling_checker_for_SOD, check_connection
except:
    from func.necessary_function import spelling_checker_for_SOD, check_connection
from googletrans import Translator
import re

translator=Translator()

class SODA_Open_Dictionary:
    def __init__(self, main_file_path='data/tu_dien_nguon.txt', sub_file_path='func/data/tu_dien_nguon.txt', internet_required=True):
        if internet_required==True: self.connection=check_connection()
        else: self.connection=False
        self.main_file_path=main_file_path
        self.sub_file_path=sub_file_path
        try:
            with open(self.main_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except:
            with open(self.sub_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        self.tu_dien = []
        for line in lines:
            word, wordtype, definition, translation, synonyms, level = line.strip().split(" % ")
            temp={"word": word, "type": wordtype, "definition": definition, "translation": translation, "level": level}
            if synonyms!="none":
                temp["synonyms"]=synonyms.split(", ")
            else:
                temp["synonyms"]=[]
            self.tu_dien.append(temp)

    def SOD_word_list(self, log_path="none"):
        try:
            with open(self.main_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except:
            with open(self.sub_file_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        if log_path!='none':
            log=open(log_path, "w", encoding="utf-8")

        tu_dien = []
        for line in lines:
            try:
                word, wordtype, definition, translation, synonyms, level = line.strip().split(" % ")
                tu_dien.append({"word": word, "type": wordtype, "definition": definition, "translation": translation, "level": level})
            except:
                if log_path!="none":
                    log.write(line+"\n")
        return tu_dien

    def SOD(self, inp, internet_required=True, boost_performance=False):
        if not boost_performance and internet_required and self.connection:
            try:
                if translator.detect(inp).lang=="en":
                    inp=spelling_checker_for_SOD(" ".join(inp.split()))
                else:
                    inp=translator.translate(text=inp).text.lower()
                for words in self.tu_dien:
                    if (words["word"]==inp) or (words["definition"]==inp):
                        return words
            except:
                return "Không tìm thấy từ"
        else:
            if internet_required:
                inp=spelling_checker_for_SOD(" ".join(inp.split()))
            for words in self.tu_dien:
                if (words["word"]==inp):
                    return words
        return "Không tìm thấy từ"
    
    def rewrite(self, filepath):
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

    def rewrite_word_source(self, filepath):
        with open(filepath, encoding="utf-8") as fi:
            list_=fi.read().split()
        words=[i["word"] for i in self.SOD_word_list()]
        for word in words:
            if word not in list_:
                list_.append(word)

        with open(filepath, "w", encoding="utf-8") as fo:
            fo.write(" ".join(list_))

    def grammar_structure_detector(self,inp,file_path):
        patterns=self.build_patterns(file_path)
        result=[]
        for i in patterns:
            if len(re.findall(patterns[i], inp))!=0:
                result.append(i.replace("\n",""))
        return result

    def build_patterns(self,file_path):
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

    def word_detector(self,inp):
        inp = inp.split()
        list_ = []
        i = 0
        while i < len(inp):
            max_len_phrase = inp[i]
            for j in range(i, len(inp)):
                phrase = " ".join(inp[i:j+1])
                if self.SOD(phrase, internet_required=False, boost_performance=True) != "Không tìm thấy từ":
                    if len(phrase) > len(max_len_phrase):
                        max_len_phrase = phrase
            if max_len_phrase not in list_:
                list_.append(max_len_phrase)
            i += len(max_len_phrase.split())
        return list_

if __name__=="__main__":
    print(SODA_Open_Dictionary().SOD(input(), boost_performance=True))