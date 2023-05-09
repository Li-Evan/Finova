import pandas as pd
import numpy as np
import os

def rsi(data, window_length):
    """
    计算RSI指标

    参数：
        data：原始数据集
        window_length：计算RSI指标的时间窗口长度

    返回值：
        RSI指标的值，以及用于计算RSI指标的数据
    """
    close = data['close']
    delta = close.diff()
    delta = delta[1:]  # 删除第一个NaN值
    up = delta.where(delta > 0, 0)
    down = -delta.where(delta < 0, 0)
    ema_up = up.ewm(alpha=1 / window_length).mean()
    ema_down = down.ewm(alpha=1 / window_length).mean()
    rs = ema_up / ema_down
    rsi = 100 - (100 / (1 + rs))
    return rsi, close[1:]

def momentum_strategy(data, rsi_window_length, buy_threshold, sell_threshold):
    """
    实现动量策略并计算买入和卖出日期

    参数：
        data：原始数据集
        rsi_window_length：计算RSI指标的时间窗口长度
        buy_threshold：买入阈值
        sell_threshold：卖出阈值

    返回值：
        买入和卖出日期列表
    """
    # 计算RSI指标
    rsi_values, close_prices = rsi(data, rsi_window_length)

    # 初始化买入和卖出日期列表
    buy_dates = []
    sell_dates = []

    # 根据RSI指标的值进行交易
    for i in range(1, len(rsi_values)):
        # 如果RSI指标的值低于买入阈值并且前一天RSI指标的值高于买入阈值，则买入
        if rsi_values[i] < buy_threshold and rsi_values[i-1] > buy_threshold:
            buy_dates.append(data['trade_date'][i])

        # 如果RSI指标的值高于卖出阈值并且前一天RSI指标的值低于卖出阈值，则卖出
        elif rsi_values[i] > sell_threshold and rsi_values[i-1] < sell_threshold:
            sell_dates.append(data['trade_date'][i])

    return buy_dates, sell_dates



# 读取CSV文件，生成DataFrame
share_code = "600519.SH"
data_file = share_code+".csv"
df = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()),"share_data",data_file))
# print(df)
data = df

# 计算买入和卖出日期列表
buy, sell = momentum_strategy(data, rsi_window_length=14, buy_threshold=30, sell_threshold=70)

# 打印买入和卖出日期列表
print('买入日期列表：', buy)
print('卖出日期列表：', sell)