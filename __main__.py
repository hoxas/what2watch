"""
what2watch

Usage:
    what2watch [options] [URL] [--seasons=<seasons>]


Options:
    -h --help                 Show this screen.
    --version                 Show version.
    -v --verbose              Verbose output.
    -q --quiet                Quiet output.
    -c --config               Show config file.
    -i --ignore-cache         Ignore cache.
    --imdb-path=PATH          Set default imdb path in config & exit.
    --seasons=SEASONS         Choose from specific seasons, otherwise all seasons.



Arguments:
    URL                       IMDB Watchlist, chart URL, TV show page or chart option.

Chart Options:
    top                       Top 250 Movies Chart (default)
    bottom                    Bottom 100 Movies Chart
    box_office                Top Box Office Movies Chart
    popular                   Most Popular Movies Chart
    top-tv                    Top 250 TV Shows Chart

Examples:
    # Default imdb path found in the config file:
    what2watch
    # Custom imdb path:
    what2watch https://www.imdb.com/path/to/public/watchlist/
    # Season filter:
    what2watch --seasons=2  (Get season 2)
    what2watch --seasons=1,2,3,4,5  (Get seasons 1,2,3,4,5)
    what2watch --seasons=1-5    (Get seasons 1,2,3,4,5)
    what2watch --seasons=1-5,7,9-11  (Get seasons 1,2,3,4,5,7,9,10,11)
"""

import docopt
from crawler import ImdbCrawler
from utils import ConfigManager, charts

config = ConfigManager()
arguments = docopt.docopt(__doc__, version="0.0.0")

if arguments['--imdb-path']:
    config.imdb_url = arguments['--imdb-path']
    print(f'IMDb default path set to {arguments["--imdb-path"]}')
    print('Exiting...')
    exit()

if arguments['--ignore-cache']:
    ignore_cache = True
    print('Ignoring cache!')
else:
    ignore_cache = False

if arguments['URL']:
    if arguments['URL'] in charts:
        imdb_url = charts[arguments['URL']]
    else:
        imdb_url = arguments['URL']
else:
    imdb_url = config.imdb_url

if arguments['--seasons']:
    seasons_filter = arguments['--seasons']
else:
    seasons_filter = ''


def main():
    crawler = ImdbCrawler(imdb_url, seasons_filter, ignore_cache)
    run = True
    while run:
        winner = crawler.get_winner()
        for key, val in winner.items():
            print(f'{key.title()}: {val}')
        reroll = input('Reroll? Y/N: ')
        if reroll.lower()[0] != 'y':
            print('Exiting...')
            run = False


if __name__ == '__main__':
    main()
