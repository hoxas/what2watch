"""
what2watch

Usage:
    what2watch [options] [URL...]

Options:

"""
import urllib.request
import re
import ast
import random
import docopt
import configparser
import os
from bs4 import BeautifulSoup

arguments = docopt.docopt(__doc__, version="0.0.0")


def main():
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

    config = configparser.ConfigParser()

    def create_config(config: configparser.ConfigParser) -> None:
        """Creates config file

        Args:
            config (ConfigParser): configparser object
        """
        config['SETTINGS'] = {'imdb_url': 'https://www.imdb.com/chart/top/'}
        config.write(open('config.ini', 'w'))

    # Creating config file if it doesn't exist
    if not os.path.exists('config.ini'):
        create_config(config)
        # Get the config file
    else:
        config.read('config.ini')
        try:
            imdb_url = config.get('SETTINGS', 'imdb_url')
        except:
            create_config(config)

    #imdb_url = 'https://www.imdb.com/user/ur56869126/watchlist'
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
    print(winner['link'])
    winner_markup = urllib.request.urlopen(winner['link'])
    winner_soup = BeautifulSoup(winner_markup, 'html.parser')
    winner_title = winner_soup.find('title').text
    winner['title'] = winner_title.replace(' - IMDb', '')
    winner_titleblock = winner_soup.find(
        'div', {'class': re.compile('TitleBlock__TitleMetaDataContainer.+')})
    winner['length'] = winner_titleblock.find_all(
        'li', {'class': 'ipc-inline-list__item'})[2].text
    winner['image'] = winner_soup.find('img', {'class': 'ipc-image'})['src']
    winner['plot'] = winner_soup.find(
        'span', {'class': re.compile('GenresAndPlot__TextContainerBreakpoint.+')}).text

    winner_genrechips = winner_soup.find_all(
        'a', {'class': re.compile('GenresAndPlot__GenreChip.+')})
    winner['genre'] = [
        i.find('span', {'class': 'ipc-chip__text'}).text for i in winner_genrechips]

    winner_credits = winner_soup.find(
        'div', {'class': re.compile('PrincipalCredits__PrincipalCredits.+')})
    winner_credits = winner_credits.find_all(
        'li', {'class': 'ipc-metadata-list__item'})
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
        'span', {'class': re.compile('AggregateRatingButton__RatingScore.+')}).text
    meta_rating = winner_soup.find('span', {'class': 'score-meta'}).text
    winner['score'] = 'IMDb Score: ' + imdb_rating + \
        '  Metacritic Score: ' + meta_rating

    print(winner)
    return winner


if __name__ == '__main__':
    main()
