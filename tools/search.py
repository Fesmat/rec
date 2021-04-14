import urllib.request
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def search_film(film):
    film_js = {}
    r2 = requests.get(film)
    film_js['url'] = r2.url
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    image = soup2.find_all(property="og:image")
    url = str(image[0]).split('"')[1]
    film_js['pict_url'] = url
    poster = urllib.request.urlopen(url).read()
    title = (str(soup2.find_all(property="og:title")).split('"')[1])[:-7]
    film_js['title'] = title
    description = (str(soup2.find_all(property="og:description")).split('"')[1]).split('. ')
    director = description[0][12:]
    film_js['director'] = director
    cast = description[1][6:]
    film_js['cast'] = cast
    synopsis = '. '.join(description[2:])
    film_js['synopsis'] = synopsis
    duration = str(soup2.find_all('time')[0]).split('>')[1].split('<')[0].strip()
    film_js['duration'] = duration
    rating = str(soup2.find_all('strong')[0]).split('"')[1].split()[0]
    film_js['rating'] = rating
    return film_js


pprint(search_film('https://www.imdb.com/title/tt6723592/'))
