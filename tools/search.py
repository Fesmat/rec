import urllib.request
import requests
from bs4 import BeautifulSoup
from pprint import pprint


def get_info(film_t):
    film_js = {}
    r2 = requests.get('https://www.imdb.com/title' + film_t)
    film_js['url'] = r2.url
    soup2 = BeautifulSoup(r2.text, 'html.parser')
    image = soup2.find_all(property="og:image")
    if image:
        url = str(image[0]).split('"')[1]
        poster = urllib.request.urlopen(url).read()
        film_js['image_url'] = url
    title = (str(soup2.find_all(property="og:title")).split('"')[1])[:-7]
    film_js['title'] = title
    description = str(soup2.find_all(property="og:description")).split('<meta content=')[1].split(' property=')[0]
    film_js['director'] = ''
    film_js['cast'] = ''
    film_js['synopsis'] = ''
    if description:
        description = description[1:-1]
        director = ''
        cast = ''
        synopsis = ''
        if 'Directed by' in description or 'Created by' in description:
            director = description.split('by ')[1].split('.  ')[0]
            description = description.split('by ')[1].split('.  ')[1]
        film_js['director'] = director
        if 'With' in description:
            cast = description.split('With ')[1].split('. ')[0]
            count = 1
            while cast[-1].isupper():
                count += 1
                cast = '. '.join(description.split('With ')[1].split('. ')[:count])
            description = description.split(cast + '. ')
            if len(description) > 1:
                description = description[1]
            else:
                description = ''

        film_js['cast'] = cast
        if description:
            synopsis = description
        film_js['synopsis'] = synopsis
    duration = soup2.find_all('time')
    if duration:
        duration = str(duration[0]).split('>')[1].split('<')[0].strip()
    else:
        duration = '0min'
    film_js['duration'] = duration
    rating = soup2.find_all('strong')
    if rating:
        rating = str(rating[0]).split('"')
        if len(rating) > 1 and rating[1].split()[0][0].isdigit():
            rating = rating[1].split()[0]
        else:
            rating = '0.0'
    else:
        rating = '0.0'
    film_js['rating'] = rating
    return film_js


def find_films(data):
    r = requests.get('https://www.imdb.com/find?q=' + '+'.join(data.split()) + '&ref=_nv_sr_sm')
    soup = BeautifulSoup(r.text, 'html.parser')
    found_films = []
    for i in soup:
        for x in str(i).split('\n'):
            if '<a href="/title' in str(x):
                x = str(x)
                g = x
                g = (g.split('<a href="/title'))
                k = 0
                for film in g:
                    k += 1
                    if k % 2 == 0:
                        continue
                    if film.startswith('/tt'):
                        found_films.append(get_info(film.split('"')[0]))
                break
    return found_films


pprint(find_films(input()))
