import os.path

import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
# import tushare as ts

def cal():
    #1.读取数据并排序
    share_code = "600519.SH"
    data_file = share_code+".csv"
    # print(data_file)
    # print(os.path.join(os.getcwd(),"share_data",data_file))
    df = pd.read_csv(os.path.join(os.getcwd(),"share_data",data_file),index_col='trade_date',parse_dates=['trade_date'])[['open','close','high','low']]
    df = df.sort_index(ascending=True)
    # df = pd.read_csv(os.path.join(os.getcwd(),"share_data",data_file))
    # print(df)
    #2.五日均线与六十日均线
    df['ma5'] = np.nan
    df['ma60'] = np.nan
    for i in range(4,len(df)):
        df.loc[df.index[i],'ma5'] = df.loc[df.index[i-4:i+1],'open'].mean()
    for i in range(59,len(df)):
        df.loc[df.index[i],'ma60'] = df.loc[df.index[i-59:i+1],'open'].mean()
    # for i in range(4, len(df)):
    #     df.loc[df.index[i],'ma5'] = df['close'][i-4:i+1].mean()
    #
    # for i in range(29, len(df)):
    #     df.loc[df.index[i],'ma30'] = df['close'][i-29:i+1].mean()

    #3.切前三百画图
    # df[['close','ma5','ma60']].plot()
    # plt.show()

    #4.金叉和死叉
    # df3 = df.dropna()
    # df3 = df3['19800101':]
    # golden_cross = []
    # death_cross = []
    # for i in range(1,len(df3)):
    #     if df3['ma5'][i-1] < df['ma60'][i-1] and df['ma5'][i] >= df['ma60'][i]:
    #         golden_cross.append(df3.index[i])
    #     elif df3['ma5'][i-1] > df['ma60'][i-1] and df['ma5'][i] <= df['ma60'][i]:
    #         death_cross.append(df3.index[i])

    df = df.dropna()
    df = df['1980-01-01':]
    golden_cross = [] # 存储买入时间
    death_cross = [] # 存储卖出时间
    for i in range(1,len(df)):
        if df['ma5'][i] >= df['ma60'][i] and df['ma5'][i-1] < df['ma60'][i-1]:
            golden_cross.append(df.index[i])
        if df['ma5'][i] <= df['ma60'][i] and df['ma5'][i-1] > df['ma60'][i-1]:
            death_cross.append(df.index[i])
    print(golden_cross)
    print(death_cross)

    # #5.策略收益
    # sr1 = pd.Series(1,index=golden_cross)
    # sr2 = pd.Series(0,index=death_cross)
    # sr = sr1.append(sr2).sort_index()
    # # sr = pd.concat([sr1, sr2], axis=0).sort_index()
    # print('茅台双均线策略（从发行股票第一天开始）')
    # first_money = 100000
    # print('本金:',first_money)
    # money = first_money
    # hold = 0
    # for i in range(len(sr)):
    #     p = df['open'][sr.index[i]]
    #     if sr.iloc[i]== 1:
    #         buy = (money // (100*p))
    #         money -= buy*100*p
    #         hold += buy*100
    #     else:
    #         money += hold*p
    #         hold = 0
    #         print(f'第{i//2+1}次交易后的收益：',money-first_money)
    # p = df['close'][-1]
    # last_money = p*hold +money
    #
    #
    # print('总收益:',last_money-first_money)
