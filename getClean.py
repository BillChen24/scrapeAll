import sys
import os
import pandas as pd
import json
from src.getClean.json.GD_prov_jyhq import *
from src.getClean.image_to_text import *
from src.getClean.image_to_table import *
from src.getClean.pdf_to_image import *
from src.getClean.clean_table import *
import warnings


# Settings the warnings to be ignored
warnings.filterwarnings('ignore')

def main():
    """
    Should pass in the path to the folder of target raw/temp data
    eg. data/Guangdong/raw/prov_month
    """
    input_path = sys.argv[1]
    current = os.getcwd()
    input_path = os.path.join(current, input_path)
    print("input path at: "+input_path)

    try:
        output_path = sys.argv[2]
    except:
        if os.path.isdir(input_path):
            if 'raw' in input_path:
                output_path = input_path.replace('raw', 'clean')
            else:
                output_path = input_path
        elif os.path.isfile(input_path):
            if 'raw' in input_path:
                output_path = os.path.dirname(input_path).replace('raw', 'clean')
            else:
                output_path = os.path.dirname(input_path)
    data_type = input('What type of data? image/pdf/table \n')

    # if data_type == 'json':
    #     data_name = input("Guangdong prov month JYHQ? (Y/N)\n")
    #     if data_name == 'Y':
    #         #load all json files from input path
    #         df_ls = load_files(input_path)
    #         #make new folder if output path does not exist
    #         if not os.path.exists(output_path):
    #             os.mkdir(output_path)
    #         #store cleaned data
    #         store_dfs(df_ls, output_path)
    #         return
    #     else:
    #         print("No other data availble.")
    #         return

    if data_type == 'image':
        #convert one image
        if os.path.isfile(input_path):
            read_image_to_xls(input_path, os.path.split(input_path)[-1], output_path)
        elif os.path.isdir(input_path):
            is_mul_dir = input('Are there multiple folders (Yes/No)? (press enter to accept the default value: No):\n')
            if is_mul_dir == 'Yes':
                for folder in os.listdir(input_path):
                    if os.path.isdir(os.path.join(input_path, folder)):
                        image_folder = os.path.join(input_path, folder)
                        head, tail = os.path.split(image_folder)
                        temp_path = image_folder #same folder as image
                        #extract and split tables from images
                        convert_all_images(image_folder, temp_path)
                        all_tables = get_tables_from_excels(temp_path)
                        tables = split_tables(all_tables)
                        store_clean(tables, output_path, table_name = folder)
            else:
                head, tail = os.path.split(input_path)
                temp_path = input_path
                #extract and split tables from images
                convert_all_images(input_path, temp_path)
                all_tables = get_tables_from_excels(temp_path)
                tables = split_tables(all_tables)
                store_clean(tables, output_path, table_name = tail)

    if data_type == 'pdf':
        #if input path is one pdf:
        if os.path.isfile(input_path):
            head, tail = os.path.split(input_path)
            file_name = tail.split('.')[0]
            temp_path = os.path.join(os.path.dirname(input_path), 'temp_' + file_name+'/')
            if output_path == os.path.dirname(input_path):
                output_path = os.path.join(output_path, 'clean_' + file_name)
            #store pdf as image in temp folder
            save_image_from_pdf(input_path, temp_path)
            #extract and split tables from images
            convert_all_images(temp_path, temp_path)
            all_tables = get_tables_from_excels(temp_path)
            tables = split_tables(all_tables)
            store_clean(tables, output_path, file_name)
            #extract text from images
            save_text_from_image(temp_path, output_path)

        #if input path is a folder
        elif os.path.isdir(input_path):
            for item in os.listdir(input_path):
                if not item.endswith('.pdf'):
                    continue
                #get file name, file path, and temporary path to store file images.
                file_name = item.split('.')[0]
                file_path = os.path.join(input_path, item)
                temp_path = os.path.join(input_path, f'temp/{file_name}/')
                #store pdf as images in temp folder
                save_image_from_pdf(file_path, temp_path, image_name = file_name)
                #extract and split tables from images
                convert_all_images(temp_path, temp_path)
                all_tables = get_tables_from_excels(temp_path)
                tables = split_tables(all_tables)
                # save tables in output folder
                new_output_path = os.path.join(output_path, file_name)
                store_clean(tables, new_output_path)
                #extract text from images
                save_text_from_image(temp_path, new_output_path)


    if data_type == 'table':
        all_tables = get_tables_from_excels(input_path)
        tables = split_tables(all_tables)
        store_clean(tables, output_path)

if  __name__ == '__main__':
    main()
