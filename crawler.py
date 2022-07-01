import urllib.request
import re
import ast
import random


from bs4 import BeautifulSoup


def get_watchlist(soup: BeautifulSoup) -> list:
    """
    Returns a list of IMDB IDs from the watchlist

    Won't raise an exception if the url is a public watchlist

    Args:
        soup (BeautifulSoup): BeautifulSoup object
    """

    list_widget = soup.find('span', {'class': 'ab_widget'})
    script = list_widget.find('script').string
    target = '"starbars":{.+},"ribbons":'
    movie_list_search = re.search(target, script)
    # scraping movie list from script starbars sections
    cleaned_movie_list = movie_list_search[0].lstrip(
        '"starbars":').rstrip(',"ribbons":')
    movie_list_dict = ast.literal_eval(cleaned_movie_list)
    movie_list = [key for key in movie_list_dict]

    return movie_list


def get_chart(soup: BeautifulSoup) -> list:
    """
    Returns a list of IMDB IDs from the chart

    Won't raise an exception if the url is a chart

    Args:
        soup (BeautifulSoup): BeautifulSoup object
    """

    list_widget = soup.find('span', {'class': 'ab_widget'})
    titles_td = list_widget.find_all('td', {'class': 'titleColumn'})
    movie_list = [title.find('a')['href'].split('?')[0].strip(
        '/').replace('title/', '') for title in titles_td]

    title = list_widget.find('h1', {'class': 'header'}).text
    print(f'Choosing from chart: {title}')

    return movie_list


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
    print(imdb_url)
    markup = urllib.request.urlopen(imdb_url)
    soup = BeautifulSoup(markup, 'html.parser')

    # Get the watchlist
    try:
        movie_list = get_watchlist(soup)
    except:
        movie_list = get_chart(soup)

    print(f'Choosing from {len(movie_list)} titles.')

    winner = dict()

    winner['URL'] = random.choice(movie_list)

    winner['link'] = f'https://www.imdb.com/title/{winner["URL"]}/'
    print(winner['link'])
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
    try:
        meta_rating = winner_soup.find('span', {'class': 'score-meta'}).text
    except:
        meta_rating = 'N/A'
    winner['score'] = f'IMDb Score: {imdb_rating}   Metacritic Score: {meta_rating}'

    return winner
