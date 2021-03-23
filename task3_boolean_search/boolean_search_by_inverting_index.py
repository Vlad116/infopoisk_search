from os import listdir
from os.path import isfile, join
import re
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer

# nltk.download("stopwords")  # used only for first time

# 1. Создать инвертированный список терминов (индекс)
russian_stopwords = stopwords.words("russian")
wnl = WordNetLemmatizer()


def process_files(filenames):
    file_to_terms = {}
    for file in filenames:
        pattern = re.compile('[\W_]+')
        file_to_terms[file] = open(files_path + '/' + file, 'r', encoding='utf-8').read().lower()
        file_to_terms[file] = pattern.sub(' ', file_to_terms[file])
        re.sub(r'[\W_]+', '', file_to_terms[file])
        re.sub(r"[\n\s.,:–\\?—\-!()/«»'#№{}\[\]→%|+®©\"]+", " ", file_to_terms[file], flags=re.UNICODE)
        re.sub(r"[\d+]", "", file_to_terms[file], flags=re.UNICODE)
        file_to_terms[file] = file_to_terms[file].split()
        file_to_terms[file] = [w for w in file_to_terms[file] if w not in russian_stopwords]
        file_to_terms[file] = [wnl.lemmatize(w) for w in file_to_terms[file]]
    return file_to_terms


# input = [word1, word2, ...]
# output = {word1: [pos1, pos2], word2: [pos2, pos434], ...}
def index_one_file(termlist):
    fileIndex = {}

    for index, word in enumerate(termlist):
        if word in fileIndex.keys():
            fileIndex[word].append(index)
        else:
            fileIndex[word] = [index]

    return fileIndex


# input = {filename: [word1, word2, ...], ...}
# res = {filename: {word: [pos1, pos2, ...]}, ...}
def make_indices(termlists):
    total = {}
    for filename in termlists.keys():
        total[filename] = index_one_file(termlists[filename])
    return total


# input = {filename: {word: [pos1, pos2, ...], ... }}
# res = {word: {filename: [pos1, pos2]}, ...}, ...}
def fullIndex(regdex):
    total_index = {}
    for filename in regdex.keys():
        for word in regdex[filename].keys():
            if word in total_index.keys():
                if filename in total_index[word].keys():
                    total_index[word][filename].extend(regdex[filename][word][:])
                else:
                    total_index[word][filename] = regdex[filename][word]
            else:
                total_index[word] = {filename: regdex[filename][word]}
    return total_index


files_path = '../files'
files = [f for f in listdir(files_path) if isfile(join(files_path, f))]
files_len = len(files)
file_names = []

for i in range(files_len):
    file_names.append(files[i])

file_to_terms = process_files(file_names)
regular_index = make_indices(file_to_terms)
total_index = fullIndex(regular_index)

# 2. Реализовать булев поиск по построенному индексу
def one_word_query(word):
    pattern = re.compile('[\W_]+')
    word = pattern.sub(' ', word)
    if word in total_index.keys():
        return [filename for filename in total_index[word].keys()]
    else:
        return []

def free_text_query(string):
    pattern = re.compile('[\W_]+')
    string = pattern.sub(' ', string)
    result = []
    for word in string.split():
        result += one_word_query(word)
    return list(set(result))


def phrase_query(string):
    pattern = re.compile('[\W_]+')
    string = pattern.sub(' ', string)
    listOfLists, result = [], []

    for word in string.split():
        listOfLists.append(one_word_query(word))
    setted = set(listOfLists[0]).intersection(*listOfLists)

    for filename in setted:
        temp = []
        for word in string.split():
            temp.append(total_index[word][filename][:])
        for i in range(len(temp)):
            for ind in range(len(temp[i])):
                temp[i][ind] -= i
        if set(temp[0]).intersection(*temp):
            result.append(filename)
    return [result,string]

print(one_word_query('новости'))
print(free_text_query('новости спорт'))
print(phrase_query('главные новости'))