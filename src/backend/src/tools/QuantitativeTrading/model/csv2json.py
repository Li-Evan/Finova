import pandas as pd
import json
import os


def csv2json(data_path, save_path):
    # print(data_path)
    # print(save_path)
    # 读取CSV文件
    # share_code = "000002.SZ"
    # data_file = share_code+".csv"
    # df = pd.read_csv(os.path.join(os.getcwd(),"share_data",data_file))
    df = pd.read_csv(data_path)

    # 选择需要转换的列
    df = df[['trade_date', 'open', 'close', 'high', 'low']]
    # print(df)
    cols = ['trade_date', 'open', 'close', 'high', 'low']

    # 重命名列名，将英文名转化为中文名
    df.columns = ['交易日期', '开盘价', '收盘价', '最高价', '最低价']
    # 转换为JSON格式
    data = []
    data.append(['Trade_date', 'Price', 'Type'])
    for row in df.itertuples(index=False):
        data.append([row.交易日期, row.开盘价, 'open'])
        data.append([row.交易日期, row.最高价, 'high'])
        data.append([row.交易日期, row.最低价, 'low'])
        data.append([row.交易日期, row.收盘价, 'close'])

    with open(os.path.join(save_path, "data.json"), "w") as f:
        json.dump(data, f)
