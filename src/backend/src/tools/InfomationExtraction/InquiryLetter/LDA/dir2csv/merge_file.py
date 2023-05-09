import os
import csv
import PyPDF2
import pandas as pd


def dir2csv(folder_path, save_path):
    # 拼装具体csv文件路径(根据文件总数确定文件名)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    file_num = len(os.listdir(folder_path))
    csv_file_path = os.path.join(save_path, "output.csv")

    # 打开CSV文件以写入数据
    with open(csv_file_path, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        # 写入表头
        writer.writerow(['content'])

        # 循环读取文件夹中的每个PDF文件
        for filename in os.listdir(folder_path):
            if filename.endswith('.pdf'):
                # 使用PyPDF2库打开PDF文件
                filepath = os.path.join(folder_path, filename)
                try:
                    with open(filepath, 'rb') as f:
                        # print(filepath)
                        pdf = PyPDF2.PdfFileReader(f)

                        # 将每页PDF的内容写入CSV文件
                        text = ""
                        for page in range(pdf.getNumPages()):
                            text += pdf.getPage(page).extractText()
                            # print(text)
                            # writer.writerow([pdf.getPage(page).extractText()])
                        writer.writerow([text])
                except:
                    os.remove(filepath)

    print('CSV文件已创建：', csv_file_path)
    return csv_file_path


if __name__ == '__main__':
    # 设置文件夹路径和CSV文件路径
    folder_path = r'C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\mappingLDA\inqueryLetter.pdf'  # 可以直接放绝对
    dir2csv(folder_path)
