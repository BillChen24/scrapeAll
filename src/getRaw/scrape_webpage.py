import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import urllib
from PIL import ImageFile
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
import json

# def getImageSize(url):
#     """
#     get file size *and* image size (None if not known)
#     """
#     file = urllib.request.urlopen(url)
#     size = file.headers.get("content-length")
#     if size: size = int(size)
#     p = ImageFile.Parser()
#     while 1:
#         data = file.read(1024)
#         if not data:
#             break
#         p.feed(data)
#         if p.image:
#             return size, p.image.size
#             break
#     file.close()
#     return size, None
#
# def download_images(url, output_path, size_threshold = 15000):
#     """
#     download images that have size over threshold from webpage
#     """
#     if not os.path.exists(output_path):
#         os.makedirs(output_path)
#
#     r = requests.get(url)
#     soup = BeautifulSoup(r.text, 'lxml')
#     image_urls = []
#     for i in soup.find_all('img'):
#         try:
#             image_urls.append(i['original'])
#         except:
#             image_urls.append(i['src'])
#
#     i = 0
#     for image_url in image_urls:
#         try:
#             img_data = requests.get(image_url).content
#             img_size = getImageSize(image_url)[0]
#         except:
#             continue
#         if img_size < size_threshold: # filter out irrelevant images
#             continue
#         with open(os.path.join(output_path,f'image_{i}.jpg'), 'wb') as handler:
#             handler.write(img_data)
#         i += 1
#     print('Images successfully saved at ' + output_path)

def scrape_urls(url=None, div_class=None, keyword=None, urls_dict=None, page_num=1, next_page_xpath=None):
    if keyword == '':
        keyword = None
    if next_page_xpath == '':
        next_page_xpath = None
    if page_num == '':
        page_num = 1
    if urls_dict is None:
        urls_dict = {}
    driver = webdriver.Chrome()
    try:
        driver.get(url)
        wait = WebDriverWait(driver, 10)

        for _ in range(page_num):
            if next_page_xpath is None and _ > 0:
                print("Warning: No next page XPath provided. Only scraping the first page.")
                break

            soup = BeautifulSoup(driver.page_source, 'html.parser')
            if div_class is not None:
                url_div = soup.find_all('div', class_=div_class)
            else:
                url_div = soup.find_all('table')

            for div in url_div:
                for link in div.find_all('a'):
                    if keyword is None or (keyword is not None and keyword in link.text):
                        try:
                            urls_dict.update({link.text: link['href']})
                        except:
                            continue

            if next_page_xpath is not None:
                try:
                    next_page_element = wait.until(EC.element_to_be_clickable((By.XPATH, next_page_xpath)))
                    next_page_element.click()
                except WebDriverException:
                    print("Warning: Next page button not clickable or not found. Stopping the scraping.")
                    break

    finally:
        driver.quit()

    return urls_dict

def store_urls_as_json(urls_dict, output_file):
    # Check if the output path is a full path
    if not os.path.isabs(output_file):
        # If it's not a full path, join it with the current working directory
        output_file = os.path.abspath(os.path.join(os.getcwd(), output_file))

    # Check if the output_file is a directory
    if os.path.isdir(output_file):
        # If it's a directory, create the full file path
        output_file = os.path.join(output_file, "urls_info.json")

    # Create the directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    os.makedirs(output_dir, exist_ok=True)

    try:
        with open(output_file, 'w', encoding = 'utf-8') as file:
            json.dump(urls_dict, file, indent=4, ensure_ascii = False)
        print(f"URLs stored as JSON in file: {output_file}")
    except IOError as e:
        print(f"Error occurred while writing to file: {output_file}")
        print(f"Error details: {str(e)}")
    except Exception as e:
        print("An error occurred during the file operation.")
        print(f"Error details: {str(e)}")

def download_images(url, output_path, size_threshold = 15000, name = 'image', image_format='both'):
     """
     download images that have size over threshold from webpage
     """
     output_path = os.path.join(output_path, f'{name}/')
     size_threshold = int(size_threshold)
     if not os.path.exists(output_path):
         os.makedirs(output_path)

     #get all image url from the webpage
     r = requests.get(url)
     soup = BeautifulSoup(r.text, 'lxml')
     image_urls = []
     for i in soup.find_all('img'):
         try:
             image_urls.append(i['original'])
         except:
             image_urls.append(i['src'])

     i = 0
     for image_url in image_urls:
         try:
             file = urllib.request.urlopen(image_url)
             img_size = file.headers.get("content-length")
             img_size = int(img_size)
         except:
             continue
         if img_size >= size_threshold: # filter out irrelevant images
            image_extension = image_url.split('.')[-1]
            if image_format == 'both':
                image_format = image_extension
            if image_format in image_url:
                image_filename = f"{name}_{i}.{image_format}"
                #with open(image_filename, 'wb') as handler:
                #    handler.write(img_data)
                urllib.request.urlretrieve(image_url, os.path.join(output_path, image_filename))
                print('Images successfully saved at ' + output_path)
            i += 1



def scrape_tables(url, output_path = None, name=None, min_rows = 2):
    """
    Scrape tables from a webpage and save as Excel files.
    """
    if output_path is None:
        output_path = os.getcwd()
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if name is None:
        name = 'table'

    try:
        r = requests.get(url, verify=False, headers={"User-Agent": "Mozilla/5.0"})
        r.raise_for_status()  # Check for any request errors

        soup = BeautifulSoup(r.text, 'lxml')
        all_tables = soup.find_all('table')

        count = 1
        for table in all_tables:
            if table.find_parent('table') is not None:
                continue  # Skip tables that are inside another table
            rows = table.find_all('tr')
            max_row_length = max(len(row.find_all(['th', 'td'])) for row in rows) if len(rows) > 0 else 0
            df = pd.DataFrame(columns=range(max_row_length))

            try:
                for j, row in enumerate(rows):
                    row_data = row.find_all(['th', 'td'])
                    row_values = [data.text for data in row_data]

                    # Pad the row with empty values if its length is less than the maximum row length
                    row_values += [''] * (max_row_length - len(row_data))
                    df.loc[j] = row_values
            except Exception as e:
                print(f"Error occurred while scraping table {count}: {str(e)}")
                continue

            if len(df) >= min_rows:
                file_path = os.path.join(output_path, f"{name}_{count}.xlsx")
                try:
                    df.to_excel(file_path, index=False, header=False)
                    print(f"{name}_{count} successfully saved at {output_path}")
                    count += 1
                except Exception as e:
                    print(f"Error occurred while saving {name}_{count} at {output_path}: {str(e)}")

        if count == 1:
            print("No tables found on the webpage.")

    except requests.RequestException as e:
        print(f"Error occurred while making the request: {str(e)}")
    except Exception as e:
        print(f"An error occurred during the scraping process: {str(e)}")
