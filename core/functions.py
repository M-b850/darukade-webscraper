import requests
from bs4 import BeautifulSoup


class Links:
    def __init__(self):
        self.url = 'https://www.darukade.com/UserControls/_Search_ProductResault2'
        self.clean_data = []

    def request(self, pn):  # pn is page number
        payload = {'URL': '/products/supplement-100004', 'URLQS': '', 'word': '', 'Page': f'{pn}'}
        response = requests.post(self.url, data=payload)
        return response

    @staticmethod
    def get_content(response):
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup

    def find_links(self, soup):
        items = soup.find_all(
            'a', class_='product-img'
        )
        for item in items:
            link = item.get('href')
            if 'products' in link:
                self.clean_data.append(
                    f"https://www.darukade.com{link}"
                )


def find_mic_detail(status, pos):
    if pos == 2:
        tmp = status.split()
        tmp.pop(1)
        tmp.pop(0)
        res = ' '.join(tmp)
        return res
    if pos == 1:
        tmp = status.split()
        tmp.pop(0)
        res = ' '.join(tmp)
        return res
