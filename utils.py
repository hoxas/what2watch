import os
import configparser

DEFAULT_URL = 'https://www.imdb.com/chart/top/'


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
            self._imdb_url = DEFAULT_URL

    @property
    def imdb_url(self):
        return self._imdb_url

    @imdb_url.setter
    def imdb_url(self, url):
        self.config.set('SETTINGS', 'imdb_url', url)
        self.config.write(open('config.ini', 'w'))


configuration = ConfigManager()
