import argparse
import os
import sys
dir_mytest = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(dir_mytest)
sys.path.insert(0, dir_mytest)
import joblib
import calculate
import arr2json


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('-income_path', default=r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\annualReport\data\宁德时代(300750)_利润表.CSV", help='利润表路径')
    parser.add_argument('-cashflow_path',default=r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\annualReport\data\宁德时代(300750)_现金流量表.CSV", help='现金流量表路径')
    parser.add_argument('-assets_path',default=r'C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\annualReport\data\宁德时代(300750)_资产负债表.CSV',help="资产负债表路径")

    args = parser.parse_args()
    income_path=args.income_path
    cashflow_path=args.cashflow_path
    assets_path = args.assets_path

    ratio_arr = calculate.calculate(income_path,cashflow_path,assets_path)
    arr2json.arr2json(ratio_arr)