import os

dict_file = r"C:\Users\LZP\Desktop\LDA\lda\stop_dic\dict.txt"
dict_list = []
with open(dict_file,'r') as f:
    # 逐行读取文件内容
    for line in f:
        # 使用split()方法将一行字符串按空格分割成单词列表
        words = line.strip().split()
        print(words)
        # 使用tuple()函数将单词列表转换成元组，并打印输出
        dict_list.append(tuple(words))
        # print(tuple(words))
print(dict_list)