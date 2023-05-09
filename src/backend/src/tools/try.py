import os
import pandas as pd
def turn_csv(file_dir):
    li = os.listdir(file_dir)
    print(li)
    for file in li:
        # 读取Excel文件
        file_path = os.path.join(file_dir, file)
        df = pd.read_csv(file_path,encoding="gbk")

        # 将数据写入CSV文件
        save_path = os.path.join(os.path.split(file_dir)[0], file.split(".")[0] + ".csv")
        df.to_csv(save_path, index=False, encoding='utf-8')
        print("Deal:" + save_path)

if __name__ == '__main__':
    turn_csv(r"C:\Users\Evan\Desktop\比赛\futu\fengshenfutubei\X系统\src\backend\src\tools\InfomationExtraction\annualReport\data")