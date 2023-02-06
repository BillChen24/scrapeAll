import pandas as pd
import os
import json
import re

def transfer(a, month_start, month_end, Year):
    df = pd.DataFrame(a)
    dic = {'jjdlData':'Bid_quant','priceData':'avg_diff','cxdlData':'Total_quant','jjjcData':'bid_diff'}
    df = df.rename(columns=dic)
    #df = df.replace('',None)
    #df = df.dropna()
    df['Month']= range(month_start,month_end+1)
    df['Year'] = [Year]*(month_end-month_start+1)
    return df

def load_files(filepath):
    file_lst = os.listdir(filepath)
    df_ls = []
    for file in file_lst:
        if file == '.ipynb_checkpoints':
            continue
        year = int(re.findall('\d+', file)[0])
        with open(os.path.join(filepath, file)) as f:
            data = json.load(f)
            df = transfer(data, 1, 12, year)
            df_ls.append(df)
    return df_ls

def output(lst, path):
    df_first = pd.concat(lst)
    df_result = df_first.reset_index(drop = True)
    df_result.to_csv(os.path.join(path, 'jyhq_prov_data.csv'),index = False)
    return df_result