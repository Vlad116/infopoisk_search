from os import listdir
from os.path import isfile, join
import re
import nltk
from nltk.corpus import stopwords
from string import punctuation
import pymorphy2
import pandas
from collections import Counter
from collections import defaultdict, OrderedDict
import math
import numpy

# nltk.download("stopwords") # used only for first time
russian_stopwords = stopwords.words("russian")
morgh = pymorphy2.MorphAnalyzer()

# def to_normal_form(word):
#     p = morgh.parse(word)[0]
#     print(p.normal_form)
#     return p.normal_form

# Подсчитать tf каждого термина
def computeTF(wordDict, bow):
    tfDict = {}
    bowCount = len(bow)
    for word, count in wordDict.items():
        tfDict[word] = count/float(bowCount)
    return tfDict

# Подсчитать idf
def computeIDF(docList):
    import math
    idfDict = {}
    N = len(docList)

    idfDict = dict.fromkeys(docList[0].keys(), 0)
    for doc in docList:
        for word, val in doc.items():
            if val > 0:
                idfDict[word] += 1

    for word, val in idfDict.items():
        idfDict[word] = math.log10(N / float(val))

    return idfDict

# Подсчитать tf-idf
def computeTFIDF(tfBow, idfs):
    tfidf = {}
    for word, val in tfBow.items():
        tfidf[word] = val*idfs[word]
    return tfidf

files_path = '../files'
files = [f for f in listdir(files_path) if isfile(join(files_path, f))]
print(files)

files_words = []

for file_name in files:
    file = open(files_path + '/' + file_name, "r", encoding="utf-8")
    file_content = file.read().replace('<b>', ' ')

    sentence = re.sub(r"[\n\s.,:–\\?—\-!()/«»'#№{}\[\]→%|+®©\"]+", " ", file_content, flags=re.UNICODE).lower()
    sentence = re.sub(r"[\d+]", "", sentence, flags=re.UNICODE)

    tokens = [token for token in sentence.split(" ") if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]

    files_words.append(tokens)

wordSet = set([item for sublist in files_words for item in sublist])

fileWordDictionaries = []

for i in range(len(files_words)):
    fileWordDictionaries.append(dict.fromkeys(wordSet,0))
    for word in files_words[i]:
        fileWordDictionaries[i][word] += 1

df = pandas.DataFrame(fileWordDictionaries)

tfDictionaries = []

for i in range(len(fileWordDictionaries)):
    tfDictionaries.append(computeTF(fileWordDictionaries[i],files_words[i]))

df_TF = pandas.DataFrame(tfDictionaries)

idfs = computeIDF(fileWordDictionaries)

tfIdfDictionaries = []

for i in range(len(tfDictionaries)):
    tfIdfDictionaries.append(computeTFIDF(tfDictionaries[i],idfs))

df_TF_IDF = pandas.DataFrame(tfIdfDictionaries)

tfIdfSumDict = {}

for col_name in df_TF_IDF.columns:
    # print(df_TF_IDF[col_name].sum())
    tfIdfSumDict[col_name]=df_TF_IDF[col_name].sum()

to_path = 'tf_idf.txt'
print("Dumping to file......................")
output_file = open(to_path, "a", encoding="utf-8")
# output_file.write("слово idf tf-idf\n")
for key in sorted(tfIdfSumDict):
    print(key)
    print(tfIdfSumDict[key])
    output_file.write(key + " " + str(idfs[key]) + " " + str(tfIdfSumDict[key]))
    output_file.write("\n")

# for col_name in sorted(tfIdfSumDict):
# df_TF_IDF_Sum = pandas.DataFrame([df.sum()], index=['sum'])
# print(df_TF_IDF_Sum)