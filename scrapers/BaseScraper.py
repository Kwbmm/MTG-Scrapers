from bs4 import BeautifulSoup
import requests


class BaseScraper:
    # This should be protected
    def __init__(self, start_page):
        self.start_page = requests.get(start_page).content
        self.bs_obj = BeautifulSoup(self.start_page, 'html.parser')
