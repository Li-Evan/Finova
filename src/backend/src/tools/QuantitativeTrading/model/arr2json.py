import json
import pandas as pd
import os

def _arr2json(arr,color,formatter,output_path):
    data = []
    for val in arr:
        data.append({
            'xAxis': val,
            'lineStyle': {
                'color': color,
                'type': 'solid'
            },
            'label': {
                'formatter': formatter,
                'color': color
            }
        })
    output = {'data': data}
    with open(output_path, 'w') as outfile:
        json.dump(output, outfile)

def arr2json(dst,buy_arr,sell_arr,share,filename):

    df = pd.read_csv(os.path.join(os.path.dirname(os.getcwd()), "share_data", share))
    df = df[['trade_date']]
    df = df.values.tolist()
    df_li = []
    for li in df:
        df_li.append(li[0])
    # print(df_li)
    buy_day = []
    sell_day = []

    for element in buy_arr:
        pos = [i for i in range(len(df_li)) if df_li[i] == element]
        buy_day.append(pos[0])
    for element in sell_arr:
        pos = [i for i in range(len(df_li)) if df_li[i] == element]
        sell_day.append(pos[0])

    if not os.path.exists(dst):
        os.mkdir(dst)

    buy_path = os.path.join(dst,filename+"_buy.json")
    sell_path = os.path.join(dst,filename+"_sell.json")

    _arr2json(buy_day,"red","买",buy_path)
    _arr2json(sell_day,"green","卖",sell_path)




if __name__ == '__main__':
    buy = [19971016, 19980105, 19980325, 19980915, 19981109, 19990305, 19990526, 19991108, 20000110, 20000627, 20001020, 20010622, 20010823, 20020307, 20020624, 20021105, 20030227, 20030717, 20031022, 20031204, 20040702, 20040920, 20041229, 20050627, 20050727, 20060703, 20060816, 20070403, 20071011, 20080114, 20080320, 20081020, 20081205, 20090204, 20090505, 20091019, 20100302, 20100712, 20101011, 20101221, 20110621, 20111027, 20120119, 20120412, 20120706, 20121101, 20130416, 20130911, 20140321, 20140528, 20140905, 20141112, 20150318, 20150525, 20150811, 20151104, 20170221, 20170314, 20170525, 20170828, 20180329, 20180921, 20181119, 20190129, 20190611, 20190912, 20200304, 20200602, 20201105, 20210108, 20211011, 20220104, 20220401, 20220629, 20220906, 20221125]
    sell = [19970811, 19971121, 19980113, 19980604, 19981021, 19981204, 19990514, 19990816, 19991209, 20000510, 20000831, 20010525, 20010730, 20011011, 20020402, 20020723, 20021112, 20030523, 20030904, 20031113, 20040428, 20040827, 20041029, 20050316, 20050629, 20060428, 20060731, 20070202, 20070911, 20071122, 20080121, 20080416, 20081104, 20081226, 20090427, 20090729, 20091127, 20100416, 20100909, 20101112, 20110427, 20110725, 20111121, 20120326, 20120625, 20120802, 20130225, 20130607, 20130926, 20140421, 20140820, 20141027, 20150206, 20150506, 20150619, 20150824, 20161207, 20170302, 20170427, 20170725, 20180207, 20180426, 20181008, 20181221, 20190506, 20190731, 20200120, 20200317, 20201028, 20201209, 20210406, 20211028, 20220215, 20220606, 20220803, 20221011, 20230206]
    share = "000002.SZ.csv"
    arr2json(dst="1",buy_arr=buy,sell_arr=sell,share=share)