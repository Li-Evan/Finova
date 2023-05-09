import pandas as pd
import numpy as np
import os
import arr2json


def cal(share):
    # 读取CSV文件，生成DataFrame
    # share_code = "600519.SH"
    # data_file = share_code + ".csv"
    # df = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), "share_data", data_file))

    df = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), "share_data", share))
    # print(df)


    # 计算动量指标
    n = 10  # 动量指标计算的天数
    df['momentum'] = df['close'].pct_change(n)
    # print(df['momentum'])

    # 生成买卖信号
    df['signal'] = np.where(df['momentum'] > 0, 1, 0)
    df['signal'] = np.where(df['momentum'] < 0, -1, df['signal'])

    # 执行买卖操作
    position = 0  # 股票持仓状态，0表示空仓，1表示持仓
    buy = []  # 买入日期列表
    sell = []  # 卖出日期列表

    for i in range(len(df)):
        # 如果信号为1，且当前为空仓，则买入股票
        if df.iloc[i]['signal'] == 1 and position == 0:
            buy.append(df.iloc[i]['trade_date'])

            position = 1
        # 如果信号为-1，且当前持仓，则卖出股票
        elif df.iloc[i]['signal'] == -1 and position == 1:
            sell.append(df.iloc[i]['trade_date'])
            position = 0

    # 如果最后一天仍然持仓，则在最后一天卖出股票
    if position == 1:
        sell.append(df.iloc[-1]['trade_date'])

    # 输出结果
    # print("Buy dates:", buy)
    # print("Sell dates:", sell)
    return [buy,sell]

    # #5.策略收益
    # sr1 = pd.Series(1,index=buy)
    # sr2 = pd.Series(0,index=sell)
    # # 合并两个Series对象并排序
    # sr = pd.concat([sr1, sr2], axis=0).sort_index()
    # # print(sr)
    # # sr = sr1.append(sr2).sort_index()
    # print(share_code+'动量模型策略（从发行股票第一天开始）')
    # first_money = 100000
    # print('本金:',first_money)
    # money = first_money
    # hold = 0
    # for i in range(len(sr)):
    #     print(sr.index[i])
    #     print(money)
    #     print(hold)
    #     # p = df['open'][sr.index[i]]
    #     p = df.loc[df['trade_date'] == sr.index[i], 'open'].values[0]
    #     if sr.iloc[i]== 1:
    #         buy = (money // (100*p))
    #         money -= buy*100*p
    #         hold += buy*100
    #     else:
    #         money += hold*p
    #         hold = 0
    #         print(f'第{i//2+1}次交易后的收益：',money-first_money)
    # p = df.iloc[-1]["close"]
    # # p = df['close'][-1]
    # last_money = p*hold +money
    #
    #
    # print('总收益:',last_money-first_money)