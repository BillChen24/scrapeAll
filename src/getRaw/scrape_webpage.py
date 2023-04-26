import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
import urllib
from PIL import ImageFile

def getImageSize(url):
    """
    get file size *and* image size (None if not known)
    """
    file = urllib.request.urlopen(url)
    size = file.headers.get("content-length")
    if size: size = int(size)
    p = ImageFile.Parser()
    while 1:
        data = file.read(1024)
        if not data:
            break
        p.feed(data)
        if p.image:
            return size, p.image.size
            break
    file.close()
    return size, None

def download_images(url, output_path, size_threshold = 15000):
    """
    download images that have size over threshold from webpage
    """
    if not os.path.exists(output_path):
        os.makedirs(output_path)

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
            img_data = requests.get(image_url).content
            img_size = getImageSize(image_url)[0]
        except:
            continue
        if img_size < size_threshold: # filter out irrelevant images
            continue
        with open(os.path.join(output_path,f'image_{i}.jpg'), 'wb') as handler:
            handler.write(img_data)
        i += 1
    print('Images successfully saved at ' + output_path)

def scrape_tables(url, output_path):
    """
    scrape tables from webpage
    """
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
