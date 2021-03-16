import os

import requests
from bs4 import BeautifulSoup
import pandas as pd

from alive_progress import alive_bar

from core.functions import find_mic_detail

u = []

dir_path = os.path.dirname(os.path.realpath(__file__))
file = f"{dir_path}/src/link2.txt"

with open(file, "r", newline=None) as f:
    with alive_bar(3709) as bar:  # declare your expected total

        for link in f:

            detail = {
                        'code': None,
                        'name_farsi': None,
                        'name_english': None,
                        'brand_farsi': None,
                        'brand_english': None,
                        'price': None,
                        'kind': None,
                        'gender': None,
                        'group': None,
                        'country': None,
                        'company': None,
                        'properties': None,
                        'guide': None,
                        'reason': None,
                    }

            url = link.replace("\n", "")

            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            detail['code'] = soup.find('span', class_='code').text.strip()
            detail['name_farsi'] = soup.find('div', class_='title-fa').text.strip()
            detail['name_english'] = soup.find('h2', class_='title-en').text.strip()

            brand_tmp = soup.find('div', class_='productExtera8').text.strip()
            detail['brand_farsi'] = brand_tmp.split('-')[0].strip()
            detail['brand_english'] = brand_tmp.split('-')[1].strip()
            
            try:
                detail['price'] = soup.find('div', class_='price-label').text.strip().split()[0]
            except AttributeError:
                detail['price'] = soup.find('div', class_='off-price-label').text.split()[2]
            
            for i in soup.find_all('div', class_='each-row'):
                status = i.text.strip()

                if 'نوع محصول' in status:
                    detail['kind'] = find_mic_detail(status, 2)
                elif 'جنسیت مصرف' in status:
                    detail['gender'] = find_mic_detail(status, 2)
                elif 'گروه' in status:
                    detail['group'] = find_mic_detail(status, 1)
                elif 'کشور سازنده' in status:
                    detail['country'] = find_mic_detail(status, 1)
                elif 'شرکت سازنده' in status:
                    detail['company'] = find_mic_detail(status, 2)

            for i in soup.find_all('ul', class_='inner-tab-title'):
                status = i.text.strip()

                if 'مشخصه ها' in status:
                    detail['properties'] = soup.find('div', id='inner-tab-1').text.strip()
                if 'روش مصرف' in status:
                    detail['guide'] = soup.find('div', id='inner-tab-2').text.strip()
                if 'موارد مصرف' in status:
                    detail['reason'] = soup.find('div', id='inner-tab-3').text.strip()
                if 'هشدار مصرف' in status:
                    detail['warn'] = soup.find('div', id='inner-tab-4').text.strip()
                if 'توضیحات' in status:
                    detail['info'] = soup.find('div', id='inner-tab-6').text.strip()

            u.append(detail)
            bar()                  # call after consuming one item

df = pd.json_normalize(u)
file2 = f"{dir_path}/src/cosmetic1.csv"
df.to_csv(file2, index=False, encoding='utf-8')


'''
کد محصول - نام محصول فارسی - نام محصول انگلیسی - نام برند فارسی -
نام برند انگلیسی - قیمت به تومان - نوع محصول - جنسیت مصرف -
گروه - کشور سازنده - شرکت سازنده - مشخصه ها - روش مصرف - موارد مصرف -
هشدار مصرف - توضیحات

'''