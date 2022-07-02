"""
what2watch

Usage:
    what2watch [options] [URL]


Options:
    -h --help                 Show this screen.
    --version                 Show version.
    -v --verbose              Verbose output.
    -q --quiet                Quiet output.
    -c --config               Show config file.
    --imdb-path=PATH          Set default imdb path in config & exit.

Arguments:
    URL                       IMDB Watchlist, chart URL, TV show page or chart option.

Chart Options:
    top                       Top 250 Movies Chart (default)
    bottom                    Bottom 100 Movies Chart
    box_office                Top Box Office Movies Chart
    popular                   Most Popular Movies Chart

Examples:
    # Default imdb path found in the config file:
    what2watch
    # Custom imdb path:
    what2watch https://www.imdb.com/path/to/public/watchlist/
"""

import docopt
from crawler import main as crawler_main
from utils import ConfigManager, charts

config = ConfigManager()
arguments = docopt.docopt(__doc__, version="0.0.0")

if arguments['--imdb-path']:
    config.imdb_url = arguments['--imdb-path']
    print(f'IMDb default path set to {arguments["--imdb-path"]}')
    print('Exiting...')
    exit()

if arguments['URL']:
    if arguments['URL'] in charts:
        imdb_url = charts[arguments['URL']]
    else:
        imdb_url = arguments['URL']
else:
    imdb_url = config.imdb_url


def main():
    # Run the crawler
    return crawler_main(imdb_url)


if __name__ == '__main__':
    winner = main()
    for key, val in winner.items():
        print(f'{key.title()}: {val}')
