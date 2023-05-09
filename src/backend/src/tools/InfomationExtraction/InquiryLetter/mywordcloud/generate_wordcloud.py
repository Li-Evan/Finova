import os.path

import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import PyPDF2
import re
from PIL import Image

def _process_text(file_path):
    # 读取PDF文件中的文本
    pdf_path = file_path
    pdf_file = open(pdf_path, 'rb')
    pdf_reader = PyPDF2.PdfFileReader(pdf_file)
    text = ''
    for page in range(pdf_reader.numPages):
        text += pdf_reader.getPage(page).extractText()
    # print(text)

    # 手动删除停用词
    replace_list = ["万元","公司","你","的","请","与","年度","事项","存在","说明",
                    "意见","为","年","月","日","表示","预计"]
    for stop_word in replace_list:
        text = text.replace(stop_word,"")
    # print(text)

    # 对文本进行分词
    words = jieba.cut(text)

    # 将分词结果拼接为一个字符串
    words_str = ' '.join(words)
    # print(words_str)
    return words_str


def generate_wordcloud(pdf_file_path,dst):
    text = _process_text(pdf_file_path)
    print(text)
    # 生成词云图像
    wordcloud = WordCloud(font_path=os.path.dirname(__file__) + '/SimHei.ttf',
                          width=800,
                          height=600,
                          # background_color=None,
                          background_color='white',
                          max_font_size=120,
                          min_font_size=20,
                          colormap = 'PuBu',# Matplotlib 提供了多种预定义的 colormap，如 viridis、 jet、 winter、 summer、 spring、autumn、 cool、 hot、 gray 等
                          mode='RGBA',

                        ).generate(text)

    # 显示词云图像
    # plt.imshow(wordcloud, interpolation='bilinear')
    # plt.axis('off')
    # plt.show()

    # 保存词云图
    if not os.path.exists(dst):
        os.mkdir(dst)
    dst = os.path.join(dst,"wordcloud.png")
    wordcloud.to_file(dst)

if __name__ == '__main__':
    # 将要处理的文本文件的路径传递给函数
    file_path = r"C:\Users\Evan\Desktop\比赛\Finova（gitee）\fengshenfutubei\X系统\src\backend\src\tools\InfomationExtraction\InquiryLetter\inqueryLetter.pdf\LSD000004176309.pdf"
    output_path = os.path.join(os.getcwd(),"output")
    generate_wordcloud(file_path,output_path)
