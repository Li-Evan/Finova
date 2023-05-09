#!/usr/bin/env python
# coding: utf-8

import re
import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
import string
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import MWETokenizer
from nltk.corpus import wordnet
wnl = WordNetLemmatizer()

def get_word_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return None

text = open("./data.txt",encoding='utf-8').readlines()
print(text)
word_dict = {}
for t in text:
    print(t)
    #去除标点符号
    for c in string.punctuation:
        if c !='-':
            t = t.replace(c,' ')

    #分词，添加自定义词组，去除停用词
    # 添加自定义词组，在分词的过程中把这些词看成是一个词组，而不是单独拆开
    tokenizer = MWETokenizer([('Python', 'programs'), ('a', 'little', 'bit'), ('a', 'lot')], separator = '-')
    # nltk.word_tokenize(t)将文本t分成一个个的单词，tokenizer.tokenize应用上述的自定义词组进一步处理分出来的词
    wordlist = tokenizer.tokenize(nltk.word_tokenize(t))
    # 去除停用词（以下代码设置了自定义的停用词表并添加到nltk提供的停用词中）
    # 加载默认的停用词列表
    stop_words = set(stopwords.words('english'))
    # 定义新的停用词列表
    stop_file = r"C:\Users\LZP\Desktop\LDA\lda\stop_dic\stopwords.txt"
    new_stop_words = open(stop_file, encoding='utf-8').readlines()
    # new_stop_words = ["custom_stop_word1", "custom_stop_word2", "custom_stop_word3"]
    # 合并默认的停用词列表和自定义的停用词列表
    stop_words.update(new_stop_words)
    filtered = [w for w in wordlist if w not in stopwords.words('english')]

    #标注词性
    refiltered =nltk.pos_tag(filtered)

    #词形还原
    lemmas_sent = []
    for wordtag in refiltered:
        wordnet_pos = get_word_pos(wordtag[1]) or wordnet.NOUN
        word = wnl.lemmatize(wordtag[0], pos=wordnet_pos)
        lemmas_sent.append(word) # 词形还原
        word_dict[word] = word_dict.get(word,0)+1
    # print(lemmas_sent)
# print(word_dict)

# 把词频保存起来
# wordfreq = pd.DataFrame({'word':word_dict.keys(),'freq':word_dict.values()})
# wordfreq.to_excel("wordfreq.xlsx",index=False)




