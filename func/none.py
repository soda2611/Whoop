from nltk.corpus import wordnet
from nltk import download
from func.SOD import SODA_Open_Dictionary

SOD=SODA_Open_Dictionary().SOD

download("wordnet")

def save_english_dictionary_to_file(file_path):
    with open(file_path, 'w', encoding="utf-8") as file:
        for synset in list(wordnet.all_synsets()):
            for lemma in synset.lemmas():
                definition=synset.definition()
                word=lemma.name()
                trans, syns, level="none", "none", "none"
                word_prop=SOD(word, internet_required=False, boost_performance=True, main_file_path="tu_dien_nguon (backup).txt", sub_file_path="func/tu_dien_nguon (backup).txt")
                if word_prop!="Không tìm thấy từ":
                    if word_prop["translation"]!="none":
                        trans=word_prop["translation"]
                    else:
                        trans=word_prop["definition"]
                    if word_prop["synonyms"]!="none":
                        syns=", ".join(word_prop["synonyms"])
                    if word_prop["level"]!="none":
                        level=word_prop["level"]
                try:    
                    file.write(f'{word} % {synset.pos()} % {definition} % {trans} % {syns} % {level}\n')
                except: print(f'{word} % {synset.pos()} % {definition} % {trans} % {syns} % {level}\n')

# Sử dụng hàm để lưu từ điển
save_english_dictionary_to_file('english_dictionary.txt')
