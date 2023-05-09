import csv


def get_info(income_path, cashflow_path, assets_path):
    data_dict = {}
    with open(income_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # 跳过第一行
        next(csvreader)
        next(csvreader)
        for row in csvreader:
            if row[1:] != []:
                # 第一列为key，剩下的为value组成的列表
                data_dict[row[0]] = row[1:]
    with open(cashflow_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # 跳过第一行
        next(csvreader)
        next(csvreader)
        for row in csvreader:
            if row[1:] != []:
                # 第一列为key，剩下的为value组成的列表
                data_dict[row[0]] = row[1:]

    with open(assets_path, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        # 跳过第一行
        next(csvreader)
        next(csvreader)
        for row in csvreader:
            # print(row)
            if row[1:] != []:
                # 第一列为key，剩下的为value组成的列表
                data_dict[row[0]] = row[1:]
    # print(data_dict)
    # for key, _ in data_dict.items():
    #     if "流动" in key:
    #         print(key+_[0])
    #     # print(_)
    return data_dict


if __name__ == '__main__':
    income_path = r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\信息提取模块\annualReport\data\宁德时代(300750)_利润表.CSV"
    cashflow_path = r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\信息提取模块\annualReport\data\宁德时代(300750)_现金流量表.CSV"
    assets_path = r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\信息提取模块\annualReport\data\宁德时代(300750)_资产负债表.CSV"
    get_info(income_path=income_path, cashflow_path=cashflow_path, assets_path=assets_path)
