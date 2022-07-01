import os
import configparser

charts = {
    'top': 'https://www.imdb.com/chart/top/',
    'bottom': 'https://www.imdb.com/chart/bottom/',
    'box_office': 'https://www.imdb.com/chart/boxoffice/',
    'popular': 'https://www.imdb.com/chart/moviemeter/',
}


class ConfigManager():
    """
    ConfigManager Class

    Properties:
        config (configparser.ConfigParser): ConfigParser object
        imdb_url (str): IMDB URL
    """

    def __init__(self):
        self.config = configparser.ConfigParser()
        self.parse_config()

    def parse_config(self):
        """
        Parse or create the config file (config.ini)
        -> Ran automatically during __init__
        """
        self.config.read('config.ini')
        try:
            self.config['SETTINGS']
        except KeyError:
            self.config.add_section('SETTINGS')

        try:
            self._imdb_url = self.config.get('SETTINGS', 'imdb_url')
        except:
            self._imdb_url = charts['top']

    @property
    def imdb_url(self):
        return self._imdb_url

    @imdb_url.setter
    def imdb_url(self, url):
        self.config.set('SETTINGS', 'imdb_url', url)
        self.config.write(open('config.ini', 'w'))


configuration = ConfigManager()
