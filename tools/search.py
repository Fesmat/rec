import urllib.request
import requests
from bs4 import BeautifulSoup

r = requests.get('https://www.imdb.com/find?q=' + '+'.join(input().split()) + '&ref=_nv_sr_sm')
soup = BeautifulSoup(r.text, 'html.parser')
for i in soup:
    for x in str(i).split('\n'):
        if '<a href="/title' in str(x):
            x = str(x)
            g = (x.split('<a href="')[1]).split('"')[0]
            r2 = requests.get('https://www.imdb.com' + g)
            soup2 = BeautifulSoup(r2.text, 'html.parser')
            image = soup2.find_all(property="og:image")
            url = str(image[0]).split('"')[1]
            poster = urllib.request.urlopen(url).read()
            title = (str(soup2.find_all(property="og:title")).split('"')[1])[:-7]
            print(title)
            description = (str(soup2.find_all(property="og:description")).split('"')[1]).split('. ')
            director = description[0][12:]
            print(director)
            cast = description[1][6:]
            print(cast)
            synopsis = '. '.join(description[2:])
            print(synopsis)
            duration = str(soup2.find_all('time')[0]).split('>')[1].split('<')[0].strip()
            print(duration)
            rating = str(soup2.find_all('strong')[0]).split('"')[1].split()[0]
            print(rating)
            break