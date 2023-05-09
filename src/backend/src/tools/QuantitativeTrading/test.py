import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# 读取CSV文件
share_code = "600519.SH"
data_file = share_code+".csv"
df = pd.read_csv(os.path.join(os.getcwd(),"share_data",data_file))
df = df.iloc[::-1]


df.to_csv('output_file.csv', index=False)