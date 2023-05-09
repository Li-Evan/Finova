import os.path

import requests
import pandas as pd

df = pd.read_csv("main.csv", encoding="gbk").loc[:, "函件内容"]
print(type(df.values))

def get_file(file_name):
    url = "http://reportdocs.static.szse.cn/UpFiles/fxklwxhj/"+file_name
    print(url)
    import requests
    response = requests.get(url)
    if not os.path.exists("../inqueryLetter.pdf"):
        os.mkdir("../inqueryLetter.pdf")

    with open(os.path.join(os.getcwd(), "../inqueryLetter.pdf", file_name), "wb") as f:
        f.write(response.content)

num = 0
for filename in df.values:
    # print(filename)
    # filename = filename.replace('HF', '')
    # print(filename)
    get_file(filename)
# # print(response.content)
