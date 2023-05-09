# # sklearn-LDA
# 代码示例：https://mp.weixin.qq.com/s/hMcJtB3Lss1NBalXRTGZlQ （玉树芝兰） <br>
# 可视化：https://blog.csdn.net/qq_39496504/article/details/107125284  <br>
# sklearn lda参数解读:https://scikit-learn.org/stable/modules/generated/sklearn.decomposition.LatentDirichletAllocation.html
# <br>中文版参数解读：https://blog.csdn.net/TiffanyRabbit/article/details/76445909
# <br>LDA原理-视频版：https://www.bilibili.com/video/BV1t54y127U8
# <br>LDA原理-文字版：https://www.jianshu.com/p/5c510694c07e
# <br>score的计算方法：https://github.com/scikit-learn/scikit-learn/blob/844b4be24d20fc42cc13b957374c718956a0db39/sklearn/decomposition/_lda.py#L729
# <br>主题困惑度1：https://blog.csdn.net/weixin_43343486/article/details/109255165
# <br>主题困惑度2：https://blog.csdn.net/weixin_39676021/article/details/112187210

# 导包
import os
import pandas as pd
import re
import jieba
import jieba.posseg as psg
# import nltk
# nltk.download('punkt')
# nltk.download('averaged_perceptron_tagger')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
import string
import pandas as pd
# from nltk.corpus import stopwords
# from nltk.stem import WordNetLemmatizer
# from nltk import MWETokenizer
# from nltk.corpus import wordnet
import joblib
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import joblib

# wnl = WordNetLemmatizer()

# 引入路径
dic_file = r"dict.txt"
stop_file = r"stopwords.txt"


## 1. 预处理(设置分词函数)
def chinese_word_cut(mytext):
    dic_file=os.path.join(os.getcwd(),"LDA","LDAmodel","dict.txt")
    stop_file=os.path.join(os.getcwd(),"LDA","LDAmodel","stopwords.txt")
    jieba.load_userdict(dic_file)
    jieba.initialize()
    try:
        stopword_list = open(stop_file, encoding='utf-8')
    except:
        stopword_list = []
        print("error in stop_file")
    stop_list = []
    flag_list = ['n', 'nz', 'vn']
    for line in stopword_list:
        line = re.sub(u'\n|\\r', '', line)
        stop_list.append(line)

    word_list = []
    # jieba分词
    # print(mytext)
    seg_list = psg.cut(mytext)
    # print(seg_list)
    for seg_word in seg_list:
        # word = re.sub(u'[^\u4e00-\u9fa5]','',seg_word.word) #如果想要分析英语文本，注释这行代码，启动下行代码
        word = seg_word.word
        find = 0
        for stop_word in stop_list:
            if stop_word == word or len(word) < 2:  # this word is stopword
                find = 1
                break
        if find == 0 and seg_word.flag in flag_list:
            word_list.append(word)
    return (" ").join(word_list)


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


def english_word_cut(t):
    # 去除标点符号
    for c in string.punctuation:
        if c != '-':
            t = t.replace(c, ' ')

    # 分词，添加自定义词组，去除停用词
    # 添加自定义词组，在分词的过程中把这些词看成是一个词组，而不是单独拆开
    dic_list = []
    with open(dic_file, 'r') as f:
        # 逐行读取文件内容
        for line in f:
            # 使用split()方法将一行字符串按空格分割成单词列表
            words = line.strip().split()
            # 使用tuple()函数将单词列表转换成元组，并打印输出
            dic_list.append(tuple(words))
    tokenizer = MWETokenizer(dic_list, separator='-')
    # nltk.word_tokenize(t)将文本t分成一个个的单词，tokenizer.tokenize应用上述的自定义词组进一步处理分出来的词
    wordlist = tokenizer.tokenize(nltk.word_tokenize(t))
    # 去除停用词（以下代码设置了自定义的停用词表并添加到nltk提供的停用词中）
    # 加载默认的停用词列表
    stop_words = set(stopwords.words('english'))
    # 定义新的停用词列表
    # new_stop_words = ["custom_stop_word1", "custom_stop_word2", "custom_stop_word3"]
    new_stop_words = open(stop_file, encoding='utf-8').readlines()
    # print(new_stop_words)
    # 合并默认的停用词列表和自定义的停用词列表
    stop_words.update(new_stop_words)
    filtered = [w for w in wordlist if w not in stopwords.words('english')]

    # 标注词性
    refiltered = nltk.pos_tag(filtered)

    # 词形还原
    lemmas_sent = []
    for wordtag in refiltered:
        wordnet_pos = get_word_pos(wordtag[1]) or wordnet.NOUN
        word = wnl.lemmatize(wordtag[0], pos=wordnet_pos)
        lemmas_sent.append(word)  # 词形还原
    # print(lemmas_sent)
    return (" ").join(lemmas_sent)


## 2.LDA分析
# 打印每个主题的前n_top_words个词
def print_top_words(model, feature_names, n_top_words):
    tword = []
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        topic_w = " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
        tword.append(topic_w)
        print(topic_w)
    return tword

def lda_train(csv_file_path, save_path,file_num,n_topics=10):
    # data = pd.read_excel(csv_file_path)
    data = pd.read_csv(csv_file_path,encoding="utf-8")
    # 如果需要中文分词就将english_word_cut改为chinese_word_cut就好了
    data["content_cutted"] = data.content.apply(chinese_word_cut)

    # n_features = 1000  # 提取1000个特征词语
    tf_vectorizer = CountVectorizer(
        # strip_accents = 'unicode',
        # max_features=n_features,
        # stop_words='english',
        # max_df = 0.5,
        # min_df = 10
    )

    tf = tf_vectorizer.fit_transform(data.content_cutted)

    ### 选定LDA划分的主题数并进行相关分析
    # n_topics指需要划分出来的主题数
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,
                                    learning_method='batch',
                                    learning_offset=50,
                                    #                                 doc_topic_prior=0.1, # alpha值
                                    #                                 topic_word_prior=0.01, # beta值
                                    random_state=0)
    # 训练lda模型
    lda.fit(tf)

    # 保存lda模型和文本特征提取器

    lda_save_path = os.path.join('LDA/checkpoint/',str(file_num)+'lda_model.joblib')
    vectorizer_save_path = os.path.join('LDA/checkpoint/',str(file_num)+'vectorizer_model.joblib')
    joblib.dump(lda, lda_save_path)
    joblib.dump(tf_vectorizer, vectorizer_save_path)

    ### 输出每篇文章对应主题
    topics = lda.transform(tf)

    topic = []
    for t in topics:
        topic.append("Topic #" + str(list(t).index(np.max(t))))
    data['概率最大的主题序号'] = topic
    data['每个主题对应概率'] = list(topics)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    save_path = os.path.join(save_path,str(file_num)+"data_topic.xlsx")
    data.to_excel(save_path, index=False)

    n_top_words = 25
    tf_feature_names = tf_vectorizer.get_feature_names_out()
    topic_word = print_top_words(lda, tf_feature_names, n_top_words)
    print(topic_word)


def lda_test(filepath):

    lda = joblib.load('LDA/checkpoint/lda_model.joblib')
    tf_vectorizer = joblib.load('LDA/checkpoint/vectorizer.joblib')
    import PyPDF2
    # 加载数据
    with open(filepath, 'rb') as f:
        pdf = PyPDF2.PdfFileReader(f)

        # 将每页PDF的内容写入CSV文件
        text = ""
        for page in range(pdf.getNumPages()):
            text += pdf.getPage(page).extractText()

    # print(text)

    # 抽取文本特征
    tf = tf_vectorizer.transform([text])

    # 使用模型预测主题分布
    topic_distribution = lda.transform(tf)

    # 返回主题分布
    # print(topic_distribution)
    return topic_distribution


if __name__ == '__main__':
    parent_dir = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
    data_path = os.path.join(parent_dir, "LDA/dir2csv/output.csv")
    # print(data_path)
    save_path = r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\信息提取模块\InquiryLetter\LDA\xlsxoutput"
    lda_train(data_path,save_path,10)
    # lda_test(r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\mappingLDA\LDA\inequry-leter-pdf\LSD000421177813.pdf")
