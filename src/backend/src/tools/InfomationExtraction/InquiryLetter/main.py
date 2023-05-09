import argparse
import os
import sys

dir_mytest = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(dir_mytest)
sys.path.insert(0, dir_mytest)
import joblib
from LDA.LDAmodel import LDAsklearn
from LDA.LDAmodel import arr2json
from mywordcloud import generate_wordcloud
from LDA.dir2csv import merge_file

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-src',
                        default=r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\InquiryLetter\inqueryLetter.pdf\LSD000038177842.pdf",
                        help='Source address(uploaded file or dir)')
    parser.add_argument('-imgdst',
                        default=r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\InquiryLetter\mywordcloud\output",
                        help='wordcloud Destination address')
    parser.add_argument('-jsondst',
                        default=r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\InquiryLetter\LDA\jsonoutput",
                        help='json file(possibility) Destination address')
    parser.add_argument('-xlsxdst',
                        default=r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\InquiryLetter\LDA\xlsxoutput",
                        help='excel(when input dir) Destination address')
    parser.add_argument('-merge_csv_dst',
                        default=r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\InquiryLetter\LDA\dir2csv",
                        help='middle csv file Destination address')
    parser.add_argument('-choice', default='1', help="choice upload file or dir")

    args = parser.parse_args()

    src = args.src
    imgdst = args.imgdst
    jsondst = args.jsondst
    xlsxdst = args.xlsxdst
    merge_csv_dst = args.merge_csv_dst

    if eval(args.choice) == 1:
        filename = os.path.split(src)[-1].split(".")[0]  # 文件名
        possibility_array = LDAsklearn.lda_test(src)  # 属于每种主题的可能性的列表
        arr2json.arr2json(possibility_array, jsondst, filename)  # 把 possibility_array 转为json并存储
        generate_wordcloud.generate_wordcloud(src, imgdst, filename)  # 生成词云并存储
    else:
        file_num = len(os.listdir(src))
        csv_file_path = merge_file.dir2csv(src, merge_csv_dst)
        LDAsklearn.lda_train(csv_file_path, xlsxdst, file_num)
