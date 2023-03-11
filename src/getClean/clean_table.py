import numpy as np
import pandas as pd
import os

def row_vec(arr):
    return [not pd.isna(i) for i in arr]

def get_table_from_excel(df, result = []):
    df_data = df.to_numpy()

    for i in range(len(df_data)):
        row_val = row_vec(df_data[i])
        if sum(row_val) < 2:
            continue

        result.append(df_data[i][row_val])
    return result

def get_tables_from_excels(table_path):
    file_ls = os.listdir(table_path)
    result = []
    temp = []
    row_key = None
    for file in file_ls:
        if file.endswith('xls'):
            df = pd.read_excel(table_path+file, header=None)
            result = get_table_from_excel(df, result)
    return result

def isTitle(arr):
    arr = arr.astype('str')
    notDigit = all(~np.array([x.replace('.', '').isdigit() for x in arr]))
    notInt = all(~np.array([isinstance(x, int) for x in arr]))
    notFloat = all(~np.array([isinstance(x, float) for x in arr]))
    return all([notDigit, notInt, notFloat])

def split_tables(array):
    title_index = []
    tables = []
    for i, d in enumerate(array):
        if isTitle(d):
            title_index.append(i)
    if len(title_index) == 0:
        return pd.DataFrame(array)
    for i in range(len(title_index)):
        if i == len(title_index) - 1:
            if title_index[i] == len(array) - 1:
                continue
            tables.append(pd.DataFrame(array[title_index[i]:]))
            continue
        if title_index[i+1] == title_index[i] + 1:
            continue

        tables.append(pd.DataFrame(array[title_index[i]:title_index[i+1]]))
    return tables

def store_clean(tables, outpath):
    if not os.path.exists(outpath):
        os.makedirs(outpath)
    for i, table in enumerate(tables):
        table.to_excel(os.path.join(outpath, f'table_{i}.xlsx'))
    print('Cleaned tables successfully saved at ' + outpath)
