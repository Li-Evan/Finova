import pandas as pd

# 读取CSV文件
df = pd.read_csv('main.csv', encoding="gbk")

# 检查列'公司简称'是否存在空值
df = df.dropna(subset=['公司简称'])

# 保存到新的CSV文件中
df.to_csv('main.csv', index=False,encoding="gbk")
