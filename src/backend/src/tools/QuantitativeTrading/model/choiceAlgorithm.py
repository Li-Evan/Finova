import argparse
import os
import sys

dir_mytest = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, dir_mytest)
from model import Bollinger
from model import momentum
from model import MACD
from model import DoubleMA
import arr2json
import csv2json

algorithm_map = {
    1: Bollinger,
    2: momentum,
    3: MACD,
    4: DoubleMA,
}

share_map = {
    1: "000002.SZ.csv",
    2: "002032.SZ.csv",
    3: "002594.SZ.csv",
    4: "300750.SZ.csv",
    5: "600519.SH.csv",
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-share_path', default=r"../share_data", help='Destination address')
    parser.add_argument('-dst', default=r"../output", help='Destination address')
    parser.add_argument('-algorithm', default="1", help='Code of the algorithm')
    parser.add_argument('-share', default="1", help='Code of the share')

    args = parser.parse_args()

    algorithmCode = eval(args.algorithm)
    shareCode = eval(args.share)
    filename = "ana_" + str(shareCode) + "_by_" + str(algorithmCode)
    dst = args.dst
    share_path = args.share_path

    # print(algorithm_map[algorithmCode].cal(dst,share_map[shareCode])[0])
    buy_arr = algorithm_map[algorithmCode].cal(share_map[shareCode])[0]
    sell_arr = algorithm_map[algorithmCode].cal(share_map[shareCode])[1]

    arr2json.arr2json(dst, buy_arr, sell_arr, share_map[shareCode], filename)
    csv2json.csv2json(os.path.join(share_path,share_map[shareCode]) , dst)
