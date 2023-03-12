import sys
import os
import pandas as pd
import json
from src.getClean.json.GD_prov_jyhq import *
from src.getClean.image_to_text import *
from src.getClean.image_to_table import *
from src.getClean.pdf_to_image import *
from src.getClean.clean_table import *

def main():
    """
    Should pass in the path to the folder of target raw/temp data
    eg. data/Guangdong/raw/prov_month
    """
    input_path = sys.argv[1]
    current = os.getcwd()
    input_path = os.path.join(current, input_path)

    try:
        output_path = sys.argv[2]
    except:
        output_path = input_path.replace('raw', 'clean')
    print(input_path)
    print(output_path)
    data_type = input('What type of data? image/pdf/table \n')

    if data_type == 'json':
        data_name = input("Guangdong prov month JYHQ? (Y/N)\n")
        if data_name == 'Y':
            #load all json files from input path
            df_ls = load_files(input_path)
            #make new folder if output path does not exist
            if not os.path.exists(output_path):
                os.mkdir(output_path)
            #store cleaned data
            store_dfs(df_ls, output_path)
            return
        else:
            print("No other data availble.")
            return

    if data_type == 'image':
        head, tail = os.path.split(input_path)
        temp_path = os.path.join(os.path.dirname(input_path), tail + '_temp/')
        #extract and split tables from images
        convert_all_images(input_path, temp_path)
        all_tables = get_tables_from_excels(temp_path)
        tables = split_tables(all_tables)
        store_clean(tables, output_path)
        #extract text from images
        save_text_from_image(input_path, output_path)

    if data_type == 'text':
        ...

    if data_type == 'pdf':
        head, tail = os.path.split(input_path)
        temp_path = os.path.join(os.path.dirname(input_path), tail + '_temp/')
        print(temp_path)
        #store pdf as image in temp folder
        save_image_from_pdf(input_path, temp_path)
        #extract and split tables from images
        convert_all_images(temp_path, temp_path)
        all_tables = get_tables_from_excels(temp_path)
        tables = split_tables(all_tables)
        store_clean(tables, output_path)
        #extract text from images
        save_text_from_image(temp_path, output_path)

    if data_type == 'table':
        all_tables = get_tables_from_excels(input_path)
        tables = split_tables(all_tables)
        store_clean(tables, output_path)





if  __name__ == '__main__':
    main()
