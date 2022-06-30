"""
what2watch

Usage:
    what2watch [options] [URL...]

Options:

"""

import configparser
import os
import docopt
from crawler import main as crawler_main

arguments = docopt.docopt(__doc__, version="0.0.0")

config = configparser.ConfigParser()


def create_config(config: configparser.ConfigParser) -> None:
    """Creates config file

    Args:
        config (ConfigParser): configparser object
    """
    config['SETTINGS'] = {'imdb_url': 'https://www.imdb.com/chart/top/'}
    config.write(open('config.ini', 'w'))


def main():
    # Creating config file if it doesn't exist
    if not os.path.exists('config.ini'):
        create_config(config)

    # Get the config file
    config.read('config.ini')
    try:
        imdb_url = config.get('SETTINGS', 'imdb_url')
    except:
        create_config(config)
        imdb_url = config.get('SETTINGS', 'imdb_url')

    # Run the crawler
    return crawler_main(imdb_url)


if __name__ == '__main__':
    main()
