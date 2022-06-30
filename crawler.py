import urllib.request
import re
import ast
import random


from bs4 import BeautifulSoup


def main(imdb_url: str):
    """
    Returns dictionary with the keys(types):
    URL(string)
    link(string)
    title(string)
    length(string)
    image(string)
    plot(string)
    genre(list)
    credits(dict(arrays))
    score(string)
    """

    markup = urllib.request.urlopen(imdb_url)
    soup = BeautifulSoup(markup, 'html.parser')
    list_widget = soup.find('span', {'class': 'ab_widget'})
    script = list_widget.find('script').string
    target = '"starbars":{.+},"ribbons":'
    list = re.search(target, script)
    list = list[0].lstrip('"starbars":').rstrip(',"ribbons":')
    list = ast.literal_eval(list)
    list = [key for key in list]
    list_len = len(list)

    print(f'Choosing from {list_len} titles.')

    winner = {}

    winner['URL'] = random.choice(list)

    winner['link'] = f'https://www.imdb.com/title/{winner["URL"]}/'
    # print(winner['link'])
    winner_markup = urllib.request.urlopen(winner['link'])
    winner_soup = BeautifulSoup(winner_markup, 'html.parser')
    winner_title = winner_soup.find('title').text
    winner['title'] = winner_title.replace(' - IMDb', '')
    winner_titleblock = winner_soup.find(
        'div', {'class': re.compile('sc.+cMYixt')})
    winner['length'] = winner_titleblock.find_all(
        'li', {'class': 'ipc-inline-list__item'})[2].text
    winner['image'] = winner_soup.find('img', {'class': 'ipc-image'})['src']
    winner['plot'] = winner_soup.find(
        'span', {'class': re.compile('sc.+fMPjMP')}).text

    winner_genrechips = winner_soup.find_all(
        'li', {'class': re.compile('ipc-inline-list__item ipc-chip__text')})
    winner['genre'] = [
        i.text for i in winner_genrechips]

    cast = winner_soup.find_all(
        'div', {'class': re.compile('sc.+eVsQmt')})
    winner['cast'] = [cast_member.find('a', {'class': re.compile('sc.+gJhRzH')}).text
                      for cast_member in cast]
    winner_credits_container = winner_soup.find(
        'ul', {'class': re.compile('ipc-metadata-list ipc-metadata-list--dividers-all.+jIsryf.+?')})
    # Lambda function to get exact match on class
    winner_credits = winner_credits_container.find_all(
        lambda tag: tag.name == 'li' and tag.get('class') == ['ipc-metadata-list__item'])
    winner['credits'] = {
        i.find(
            ['span', 'a'],
            {'class': 'ipc-metadata-list-item__label'}).text:
        [i.text for i in i.find_all(
            'a',
            {'class': "ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"})]
        for i in winner_credits
    }

    imdb_rating = winner_soup.find(
        'span', {'class': re.compile('sc.+jGRxWM')}).text
    meta_rating = winner_soup.find('span', {'class': 'score-meta'}).text
    winner['score'] = f'IMDb Score: {imdb_rating}   Metacritic Score: {meta_rating}'

    for key, val in winner.items():
        print(f'{key.title()}: {val}')
    return winner
