import requests
from bs4 import BeautifulSoup
import os
import pandas as pd

def download_images(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    image_urls = [i['src'] for i in soup.find_all('img')]

    i = 0
    for image_url in image_urls:
        try:
            img_data = requests.get(image_url).content
        except:
            continue
        with open(os.path.join(output_path,f'image_{i}.jpg'), 'wb') as handler:
            handler.write(img_data)
        i += 1
    print('Images successfully saved at ' + output_path)

def scrape_tables(url, output_path):
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    r = requests.get(url, verify = False)
    print(r)
    soup = BeautifulSoup(r.text, 'lxml')
    all_tables = soup.find_all('table')

    count = 1
    for table in all_tables:
        headers = []
        for i in table.find_all('th'):
            title = i.text
            headers.append(title)

        df = pd.DataFrame(columns = headers)
        for j in table.find_all('tr')[1:]:
            row_data = j.find_all('td')
            row = [i.text for i in row_data]
            length = len(df)
            df.loc[length] = row
        if len(df) > 1:
            df.to_excel(os.path.join(output_path,f'table_{count}.xlsx'))
            print(f"table_{count} successfully saved at " + output_path)
            count += 1
