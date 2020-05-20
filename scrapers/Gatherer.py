import re
from typing import Iterable

import requests
from bs4 import BeautifulSoup

from data_objects.Card import Card
from scrapers.BaseScraper import BaseScraper


class Gatherer(BaseScraper):
    __url = "https://gatherer.wizards.com/Pages/Default.aspx"
    __search_url = "https://gatherer.wizards.com/Pages/Search/Default.aspx?page={page_num}&"

    def __init__(self):
        super().__init__(self.__url)
        self.cards_2_set = {opt['value']: list() for opt in
                            self.parser.select(
                                "select#ctl00_ctl00_MainContent_Content_SearchControls_setAddText option") if
                            opt['value'] != ''}

    def get_sets(self) -> Iterable[str]:
        return self.cards_2_set.keys()

    def get_cards_for_set(self, set_name: str) -> Iterable[str]:
        if set_name in self.cards_2_set:
            if not self.cards_2_set[set_name]:
                self.__fetch_cards_for_set(set_name)
            return self.cards_2_set[set_name]
        return []

    def __fetch_cards_for_set(self, set_name: str) -> None:
        set_url = self.__search_url.format(page_num=0) + "set=[\"{0}\"]".format(set_name.replace(" ", "+"))
        set_page = requests.get(set_url).content
        set_page_parser = BeautifulSoup(set_page, 'html.parser')
        number_of_pages = len(
            set_page_parser.select("div#ctl00_ctl00_ctl00_MainContent_SubContent_topPagingControlsContainer > a")) - 1
        card_list = [re.sub(r".*\((.*)\)", r"\1", r.text) for r in
                     set_page_parser.select("table.cardItemTable div.cardInfo > span.cardTitle a")]
        for c in set_page_parser.select("tr.cardItem"):
            card = Card(c, set_name)
            card.to_json()
        for i in range(1, number_of_pages):
            set_url = self.__search_url.format(page_num=i) + "set=[\"{0}\"]".format(set_name.replace(" ", "+"))
            set_page = requests.get(set_url).content
            set_page_parser = BeautifulSoup(set_page, 'html.parser')
            card_list = card_list + [re.sub(r".*\((.*)\)", r"\1", r.text) for r in
                                     set_page_parser.select("table.cardItemTable div.cardInfo > span.cardTitle a")]
        self.cards_2_set[set_name] = card_list
