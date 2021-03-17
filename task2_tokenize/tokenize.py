from os import listdir
from os.path import isfile, join
import re
import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation
from collections import Counter

nltk.download("stopwords") # used only for first time

words_path = 'words.txt'
tokens_path = 'tokens.txt'
files_path = '../files'

files = [f for f in listdir(files_path) if isfile(join(files_path, f))]
mystem = Mystem()
russian_stopwords = stopwords.words("russian")
words = []

def preprocess_text(text):
    tokens = mystem.lemmatize(text.lower())
    tokens = [token for token in tokens if token not in russian_stopwords \
              and token != " " \
              and token.strip() not in punctuation]
    return tokens

files_len = len(files)

for i in range(files_len):
    file_name = files[i]
    print('Processing site ' + str(i) + '/' + str(files_len) + '. ' + file_name)
    file = open(files_path + '/' + file_name, "r", encoding="utf-8")
    file_content = file.read().replace('<b>', ' ')
    file.close()

    # makes normalization faster
    sentence = re.sub(r"[\n\s.,:–\\?—\-!()/«»'#№{}\[\]→%|+®©\"]+", " ", file_content, flags=re.UNICODE).lower()
    sentence = re.sub(r"[\d+]", "", sentence, flags=re.UNICODE)

    tokens = [token for token in sentence.split(" ") if token not in russian_stopwords \
              and token != " " \

              and token.strip() not in punctuation]
    words.extend(tokens)

words_file = open(words_path, "a", encoding="utf-8")
words_dict = Counter(words)
words_dict_len = len(words_dict)
print(words_dict_len)
print(words_dict)

print('Dumping words to file......................')
for key, value in words_dict.items():
    words_file.write(key + " " + str(value) + "\n")
words_file.close()

# with open(words_path,"r",encoding="utf-8") as word_file:
#     word_list = [line.split(None, 1)[0] for line in word_file]
#
# words_dict = Counter(word_list)
# words_dict_len = len(words_dict)

# with open("file.txt", "r") as ins:
#     array = []
#     for line in ins:
#         array.append(line)

tokens = {}
print('Lemmatizing words to file......................')
i = 1

for word, count in words_dict.items():
    print(str(word) + ' ' + str(count))
    print('Processing word ' + str(i) + '/' + str(words_dict_len) + '. ' + word)
    token = mystem.lemmatize(word)[0]
    if token in tokens:
        tokens.get(token).append(word)
    else:
        tokens[token] = [word]
    i += 1

print("Dumping tokens to file......................")
tokens_file = open(tokens_path, "a", encoding="utf-8")

for key, words_tokens in tokens.items():
    print(key)
    print(words_tokens)
    tokens_file.write(key + " ")
    for word in words_tokens:
        tokens_file.write(word + " ")
    tokens_file.write("\n")