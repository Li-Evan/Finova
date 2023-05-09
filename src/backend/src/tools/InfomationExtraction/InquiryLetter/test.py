import jieba
from mywordcloud import WordCloud
import matplotlib.pyplot as plt
import PyPDF2
import re
from PIL import Image

def process_text(filename):
    # 读取PDF文件中的文本
    pdf_path = r"C:\Users\LZP\Desktop\富途比赛算法部分\信息提取模块\问询函\inequry-leter-pdf\LSD000150177391.pdf"
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page).extractText()
    print(text)

    pattern = re.compile(r'[^\u4e00-\u9fa5]')
    # 使用正则表达式替换所有匹配到的非中文字符
    # text = pattern.sub('', text)

    # text = text.replace(" ", "")
    # text = text.replace("\n", "")
    # text = text.replace("万元", "")
    # text = re.compile(r'[0-9]').sub('', text)
    print(text)  # 输出 "Hello,World!"

    # 对文本进行分词
    words = jieba.cut(text)

    # 将分词结果拼接为一个字符串
    words_str = ' '.join(words)
    print(words_str)
    # 生成词云图像
    wordcloud = WordCloud(font_path='simhei.ttf', width=800, height=600,background_color='white').generate(words_str)

    # 显示词云图像
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()
    
    # 保存词云图
    wordcloud.to_file("mywordcloud.png")
# 将要处理的文本文件的路径传递给函数
process_text('text.txt')
