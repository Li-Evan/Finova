import json
import pandas as pd
import os

def arr2json(arr,dst,filename):
    name_arr = ["收入与业绩", "借款担保", "产品市场", "平台业务", "商誉与减值",
                "项目建设", "子公司", "履约合同", "业绩承诺", "政府补助"]
    if not os.path.exists(dst):
        os.mkdir(dst)
    dst_path = os.path.join(dst,filename+".json")
    with open(dst_path,"w") as f:
        json.dump({"possibility":arr[0].tolist(),"name":name_arr},f)
    # possibility_dst_path = os.path.join(dst,filename+"_possibility.json")
    # name_dst_path = os.path.join(dst,filename+"_name.json")
    # with open(possibility_dst_path,"w") as f:
    #     json.dump({"possibility":arr[0].tolist()},f)
    #
    # with open(name_dst_path, "w") as f:
    #     json.dump({"name": name_arr}, f)



if __name__ == '__main__':
    pass