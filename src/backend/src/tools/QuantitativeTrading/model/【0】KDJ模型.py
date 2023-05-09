import pandas as pd
import numpy as np
import os

# 读取CSV文件，生成DataFrame
share_code = "600519.SH"
data_file = share_code+".csv"
df = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()),"share_data",data_file))
# print(df)
data = df

# 设置KDJ指标的参数
n = 9
m1 = 3
m2 = 3

# 计算RSV值
df['lowest'] = df['low'].rolling(window=n, min_periods=n).min()  # 计算最近n天的最低价
df['highest'] = df['high'].rolling(window=n, min_periods=n).max()  # 计算最近n天的最高价
df['rsv'] = (df['close'] - df['lowest']) / (df['highest'] - df['lowest']) * 100  # 计算RSV值

# 计算KDJ指标
df['k'] = np.nan
df['d'] = np.nan
df['j'] = np.nan

for i in range(n, len(df)):
    # 计算K值和D值
    if i == n:
        df.loc[i, 'k'] = 50
        df.loc[i, 'd'] = 50
    else:
        k = m1 * df.loc[i, 'rsv'] + (1 - m1) * df.loc[i - 1, 'k']
        d = m2 * k + (1 - m2) * df.loc[i - 1, 'd']
        df.loc[i, 'k'] = k
        df.loc[i, 'd'] = d

    # 计算J值
    j = 3 * df.loc[i, 'k'] - 2 * df.loc[i, 'd']
    df.loc[i, 'j'] = j

# 生成交易信号
df['signal'] = np.nan
df['buy'] = np.nan
df['sell'] = np.nan

for i in range(n, len(df)):
    # 根据KDJ指标的值生成交易信号
    if df.loc[i, 'j'] < 0 and df.loc[i - 1, 'j'] >= 0:
        df.loc[i, 'signal'] = 'buy'
    elif df.loc[i, 'j'] > 100 and df.loc[i - 1, 'j'] <= 100:
        df.loc[i, 'signal'] = 'sell'

    # 根据交易信号确定买入和卖出的日期
    if df.loc[i, 'signal'] == 'buy':
        df.loc[i, 'buy'] = df.loc[i, 'trade_date']
    elif df.loc[i, 'signal'] == 'sell':
        df.loc[i, 'sell'] = df.loc[i, 'trade_date']

# 将买入和卖出的日期存储在buy和sell列表中
buy = df.loc[df['signal'] == 'buy', 'buy'].tolist()
sell = df.loc[df['signal'] == 'sell', 'sell'].tolist()
