import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import arr2json


def cal(share):
    # 读取CSV文件，生成DataFrame
    # share_code = "600519.SH"
    # data_file = share_code + ".csv"
    # df = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), "share_data", data_file))
    # print(df)
    df = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), "share_data", share))
    data = df

    # 计算移动平均线
    def moving_average(data, window_size):
        return data['close'].rolling(window_size).mean()

    # 计算指数移动平均线
    def exponential_moving_average(data, window_size):
        return data['close'].ewm(span=window_size, adjust=False).mean()

    # 计算MADC指标
    def madc(data, short_window, long_window):
        # 计算短期移动平均线和长期移动平均线
        short_ma = moving_average(data, short_window)
        long_ma = moving_average(data, long_window)

        # 计算MADC指标
        madc = short_ma - long_ma

        # 返回MADC指标和移动平均线
        return madc, short_ma, long_ma

    # 计算MADC指标
    short_window = 10
    long_window = 30
    madc, short_ma, long_ma = madc(data, short_window, long_window)

    # 绘制收盘价、移动平均线和MADC指标
    # plt.plot(data['trade_date'], data['close'], label='Close')
    # plt.plot(data['trade_date'], short_ma, label='Short MA')
    # plt.plot(data['trade_date'], long_ma, label='Long MA')
    # plt.plot(data['trade_date'], madc, label='MADC')
    # plt.title('MADC Indicator')
    # plt.legend()
    # plt.show()

    # 初始化变量
    position = None
    buy = []
    sell = []

    # 根据MACD策略进行交易
    for i in range(long_window, len(data)):
        if madc[i-1] < 0 and madc[i] > 0: # MADC指标上穿0线
            if position != True: # 如果没有持有股票，则买入
                position = True
                buy.append(data['trade_date'][i])
                # print('Buying at ' + str(data['trade_date'][i]))
        elif madc[i-1] > 0 and madc[i] < 0: # MADC指标下穿0线
            if position != False: # 如果持有股票，则卖出
                position = False
                sell.append(data['trade_date'][i])
                # print('Selling at ' + str(data['trade_date'][i]))
        else:
            pass # 不做任何操作

    # 打印买入和卖出日期
    # print('Buy Dates:', buy)
    # print('Sell Dates:', sell)
    return [buy,sell]

    # sr1 = pd.Series(1,index=buy)
    # sr2 = pd.Series(0,index=sell)
    # # sr = sr1.append(sr2).sort_index()
    # sr = pd.concat([sr1, sr2], axis=0).sort_index()
    # print(share_code+'MACD模型策略（从发行股票第一天开始）')
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