import requests
from bs4 import BeautifulSoup

r = requests.get('https://kino.mail.ru/search/?q=1+1&region_id=107')
soup = BeautifulSoup(r.text, 'html.parser')
for i in soup:
    for x in str(i).split('\n'):
        if '<div class="text text_light_normal text_fixed margin_top_5 color_gray"' in x:
            x = x[x.find('<div class="text text_light_normal text_fixed margin_top_5 color_gray"'):]
            x = x[:x.find('/div') - 1]
            title = x[x.rfind('>') + 1:]
            print(title)
            break
