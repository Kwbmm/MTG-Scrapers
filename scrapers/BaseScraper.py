import requests
from bs4 import BeautifulSoup


class BaseScraper:
    def __init__(self, start_page):
        self.start_page = requests.get(start_page).content
        self.parser = BeautifulSoup(self.start_page, 'html.parser')
