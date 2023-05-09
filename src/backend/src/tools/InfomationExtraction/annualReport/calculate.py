import get_info


def calculate(income_path,cashflow_path,assets_path):

    data_info = get_info.get_info(income_path,cashflow_path,assets_path)
    # # print(data_info)

    for key, value in data_info.items():
        # 已经确定能且仅能获取一项的项目
        if "净利润" == key:
            # print(key + str(eval(value[0])))
            netProfit = eval(value[0])
        if "营业利润" in key:
            # print(key + str(eval(value[0])))
            operatingProfit = eval(value[0])
        if "营业收入" == key:
            # print(key + str(eval(value[0])))
            operatingIncome = eval(value[0])
        if "所有者权益(或股东权益)合计" in key:
            # print(key + str(eval(value[0])))
            netAssets = eval(value[0])
        if "销售商品、提供劳务收到的现金" in key:
            # print(key + str(eval(value[0])))
            salesIncome = eval(value[0])
        if "销售费用" in key:
            # print(key + str(eval(value[0])))
            salesCost = eval(value[0])
        if "存货" == key:
            # print(key + str(eval(value[0])))
            inventory = eval(value[0])
        if "应收票据及应收账款" in key:
            # print(key + str(eval(value[0])))
            accountsReceivable = eval(value[0])
        if "资产总计" in key:
            # print(key + str(eval(value[0])))
            totalAssets = eval(value[0])
        if "经营活动产生的现金流量净额" in key:
            # print(key + str(eval(value[0])))
            cashFlowOpetating = eval(value[0])
        if "实收资本(或股本)" in key:
            # print(key + str(eval(value[0])))
            shareCapital = eval(value[0])
        if "流动资产合计" == key:
            # print(key + value[0])
            currentAssets = eval(value[0])
        if "流动负债合计" == key:
            # print(key + value[0])
            currentLiabilities = eval(value[0])
        if "负债合计" == key:
            # print(key + value[0])
            totalLiabilities = eval(value[0])
        if "研发费用" in key:
            # print(key + value[0])
            RDExpenses = eval(value[0])
        if "固定资产净额" in key:
            # print(key + value[0])
            netFixedAssets = eval(value[0])
        if "投资活动产生的现金流量净额" in key:
            # print(key + value[0])
            cashFlowInvesting = abs(eval(value[0]))
        # 代尝试项目


    '''
    营运能力：
    1. 库存周转率：销售收入 1 ÷ 平均存货 1 公式：库存周转率 = 销售收入 ÷ [(期初存货 + 期末存货) ÷ 2]
    2. 应收账款周转率：营业收入 1 ÷ 平均应收账款 1 公式：应收账款周转率 = 营业收入 ÷ [(期初应收账款 + 期末应收账款) ÷ 2]
    3. 总资产周转率：营业收入 1 ÷ 平均总资产（资产总计） 1  公式：总资产周转率 = 营业收入 ÷ [(期初总资产 + 期末总资产) ÷ 2]
    4. 现金流量比率：经营活动现金流量净额 1  ÷ 净营业收入（营业收入）1 公式：现金流量比率 = 经营活动现金流量净额 ÷ 净营业收入
    5. 存货周转天数：平均存货 1 ÷ 日销售成本 1 公式：存货周转天数 = [(期初存货 + 期末存货) ÷ 2] ÷ (年度销售成本 ÷ 365)
    6. 应收账款周转天数：平均应收账款 1 ÷ 日销售收入 1  公式：应收账款周转天数 = [(期初应收账款 + 期末应收账款) ÷ 2] ÷ (年度销售收入 ÷ 365)
    '''

    # 库存周转率
    inventoryTurnoverRatio = salesIncome / inventory

    # 应收账款周转率
    accountsReceivableTurnoverRatio = operatingIncome / accountsReceivable

    # 总资产周转率
    totalAssetTurnover = operatingIncome / totalAssets

    # 现金流量比率
    cashFlowRatio = cashFlowOpetating / operatingIncome

    # 存货周转天数
    daysInventoryOutstanding = inventory / (salesCost / 365)

    # 应收账款周转天数
    daysSalesOutstanding = accountsReceivable / (salesCost / 365)

    operational_capacity_li = [inventoryTurnoverRatio, accountsReceivableTurnoverRatio, totalAssetTurnover,
                               cashFlowRatio, daysInventoryOutstanding, daysSalesOutstanding]
    # print(li)
    # return operational_capacity_li

    '''
    盈利能力：
    1. 毛利率：毛利润 ÷ 销售收入 公式：毛利率 = (销售收入 - 销售成本) ÷ 销售收入
    2. 净利率：净利润 ÷ 销售收入 公式：净利率 = 净利润 ÷ 销售收入
    3. 营业利润率：营业利润 ÷ 销售收入 公式：营业利润率 = 营业利润 ÷ 销售收入
    4. 总资产收益率：净利润 ÷ 平均总资产 公式：总资产收益率 = 净利润 ÷ [(期初总资产 + 期末总资产) ÷ 2]
    5. 每股收益：净利润 ÷ 加权平均股本 公式：每股收益 = 净利润 ÷ 加权平均股本
    '''

    # 毛利率
    grossMargin = (salesIncome - salesCost) / salesIncome
    # 净利率
    netProfitMargin = netProfit / salesIncome
    # 营业利润率
    operatingProfitMargin = operatingProfit / salesIncome
    # 总资产收益率
    returnOnTotalAssets = netProfit / totalAssets
    # 每股收益
    earningsPerShare = netProfit / shareCapital

    profit_ability_li = [grossMargin, netProfitMargin, operatingProfitMargin, returnOnTotalAssets, earningsPerShare]
    # print(li)

    '''
    偿债能力：
    1. 流动比率：流动资产 ÷ 流动负债 公式：流动比率 = 流动资产 ÷ 流动负债
    2. 速动比率：(流动资产 - 存货) ÷ 流动负债 公式：速动比率 = (流动资产 - 存货) ÷ 流动负债
    3. 负债总额与净资产比率：负债总额 ÷ 净资产 公式：负债总额与净资产比率 = 负债总额 ÷ 净资产
    '''

    # 流动比率
    currentRatio = currentAssets / currentLiabilities

    # 速动比率
    quickRatio = (currentAssets - inventory) / currentLiabilities

    # 负债总额与净资产比率
    debtToEquityRatio = totalLiabilities / netAssets

    debt_repayment_ability_li = [currentRatio, quickRatio, debtToEquityRatio]

    '''
    发展能力：
    1. 固定资产周转率：营业收入 ÷ 平均固定资产 公式：固定资产周转率 = 营业收入 ÷ [(期初固定资产 + 期末固定资产) ÷ 2]
    2. 研发费用率：研发费用 ÷ 营业收入 公式：研发费用率 = 研发费用 ÷ 营业收入
    3. 资产负债率：负债总额 ÷ 总资产 公式：资产负债率 = 负债总额 ÷ 总资产
    4. 现金再投资比率：经营活动现金流量净额 ÷ 投资活动现金流量净额 公式：现金再投资比率 = 经营活动现金流量净额 ÷ 投资活动现金流量净额
    '''

    # 固定资产周转率
    fixedAssetTurnoverRatio = operatingIncome / netFixedAssets

    # 研发费用率
    RDExpenseRatio = RDExpenses / operatingIncome

    # 资产负债率
    debtToAssetRatio = totalLiabilities / netAssets

    # 现金再投资比率
    cashReinvestmentRatio = cashFlowOpetating / cashFlowInvesting

    development_ability_li = [fixedAssetTurnoverRatio, RDExpenseRatio, debtToAssetRatio, cashReinvestmentRatio]

    return [operational_capacity_li,profit_ability_li,debt_repayment_ability_li,development_ability_li]


def operational_capacity():
    # 库存周转率
    inventoryTurnoverRatio = salesIncome / inventory

    # 应收账款周转率
    accountsReceivableTurnoverRatio = operatingIncome / accountsReceivable

    # 总资产周转率
    totalAssetTurnover = operatingIncome / totalAssets

    # 现金流量比率
    cashFlowRatio = cashFlowOpetating / operatingIncome

    # 存货周转天数
    daysInventoryOutstanding = inventory / (salesCost / 365)

    # 应收账款周转天数
    daysSalesOutstanding = accountsReceivable / (salesCost / 365)

    operational_capacity_li = [inventoryTurnoverRatio,accountsReceivableTurnoverRatio,totalAssetTurnover,
          cashFlowRatio,daysInventoryOutstanding,daysSalesOutstanding]
    # print(li)
    return operational_capacity_li

'''
盈利能力：
1. 毛利率：毛利润 ÷ 销售收入 公式：毛利率 = (销售收入 - 销售成本) ÷ 销售收入
2. 净利率：净利润 ÷ 销售收入 公式：净利率 = 净利润 ÷ 销售收入
3. 营业利润率：营业利润 ÷ 销售收入 公式：营业利润率 = 营业利润 ÷ 销售收入
4. 总资产收益率：净利润 ÷ 平均总资产 公式：总资产收益率 = 净利润 ÷ [(期初总资产 + 期末总资产) ÷ 2]
5. 每股收益：净利润 ÷ 加权平均股本 公式：每股收益 = 净利润 ÷ 加权平均股本
'''


def profit_ability():
    # 毛利率
    grossMargin = (salesIncome - salesCost) / salesIncome
    # 净利率
    netProfitMargin = netProfit / salesIncome
    # 营业利润率
    operatingProfitMargin = operatingProfit / salesIncome
    # 总资产收益率
    returnOnTotalAssets = netProfit / totalAssets
    # 每股收益
    earningsPerShare = netProfit / shareCapital

    profit_ability_li = [grossMargin,netProfitMargin,operatingProfitMargin,returnOnTotalAssets,earningsPerShare]
    # print(li)
    return profit_ability_li

'''
偿债能力：
1. 流动比率：流动资产 ÷ 流动负债 公式：流动比率 = 流动资产 ÷ 流动负债
2. 速动比率：(流动资产 - 存货) ÷ 流动负债 公式：速动比率 = (流动资产 - 存货) ÷ 流动负债
3. 负债总额与净资产比率：负债总额 ÷ 净资产 公式：负债总额与净资产比率 = 负债总额 ÷ 净资产
'''


def debt_repayment_ability():
    # 流动比率
    currentRatio = currentAssets/currentLiabilities

    # 速动比率
    quickRatio = (currentAssets-inventory)/currentLiabilities

    # 负债总额与净资产比率
    debtToEquityRatio = totalLiabilities/netAssets

    debt_repayment_ability_li = [currentRatio,quickRatio,debtToEquityRatio]
    # print(li)
    return debt_repayment_ability_li

'''
发展能力：
2. 固定资产周转率：营业收入 ÷ 平均固定资产 公式：固定资产周转率 = 营业收入 ÷ [(期初固定资产 + 期末固定资产) ÷ 2]
4. 研发费用率：研发费用 ÷ 营业收入 公式：研发费用率 = 研发费用 ÷ 营业收入
5. 资产负债率：负债总额 ÷ 总资产 公式：资产负债率 = 负债总额 ÷ 总资产
6. 现金再投资比率：经营活动现金流量净额 ÷ 投资活动现金流量净额 公式：现金再投资比率 = 经营活动现金流量净额 ÷ 投资活动现金流量净额
'''


def development_ability():
    # 固定资产周转率
    fixedAssetTurnoverRatio = operatingIncome/netFixedAssets

    # 研发费用率
    RDExpenseRatio = RDExpenses/operatingIncome

    # 资产负债率
    debtToAssetRatio = totalLiabilities/netAssets

    # 现金再投资比率
    cashReinvestmentRatio = cashFlowOpetating/cashFlowInvesting

    development_ability_li = [fixedAssetTurnoverRatio,RDExpenseRatio,debtToAssetRatio,cashReinvestmentRatio]
    # print(li)
    return development_ability_li

if __name__ == '__main__':
    income_path = r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\annualReport\data\宁德时代(300750)_利润表.CSV"
    cashflow_path = r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\annualReport\data\宁德时代(300750)_现金流量表.CSV"
    assets_path = r"C:\Users\LZP\Desktop\富途比赛算法代码\有很多注释版本（没用的功能都注释了，以后用方便）\InfomationExtraction\annualReport\data\宁德时代(300750)_资产负债表.CSV"

    calculate(income_path,cashflow_path,assets_path)
