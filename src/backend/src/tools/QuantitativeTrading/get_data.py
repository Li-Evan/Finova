import numpy as np
import random
import matplotlib.pyplot as plt
import pandas as pd
import tushare as ts
import os

#1.爬取某只股票信息并保存
share_code = "600519.SH"
ts.set_token('f5e0931bb8d5140214d95286b80ff8b9b769302d6577f0e944c3aa21')
pro = ts.pro_api()
fd = pro.daily(ts_code=share_code, start_date='19800101', end_date='20230301')
# print(type(fd))
fd = fd.iloc[::-1]
fd.to_csv(os.path.join(os.getcwd(),"share_data",share_code+'.csv'))