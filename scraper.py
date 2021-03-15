import os
import requests
from bs4 import BeautifulSoup

from core.functions import Links

dir_path = os.path.dirname(os.path.realpath(__file__))
file = f"{dir_path}/src/links.txt"

with open(file, 'w') as f:
    # page 1 to 924
    for i in range(1, 924):
        print(i)
        daru_kade = Links()
        response = daru_kade.request(i)
        soup = daru_kade.get_content(response)
        daru_kade.find_links(soup)
        for link in daru_kade.clean_data:
            f.write('{}\n'.format(link))
