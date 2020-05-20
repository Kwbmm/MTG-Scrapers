import base64
import json
import re

import requests
from bs4 import Tag


class Card:
    __image_url = "https://gatherer.wizards.com/Handlers/Image.ashx?type=card&multiverseid={}"

    def __init__(self, bs_card_item: Tag, set_name: str) -> None:
        self.set = set_name
        self.name = bs_card_item.select_one("div.cardInfo > span.cardTitle > a").text
        self.image = bs_card_item.select_one(
            "img#ctl00_ctl00_ctl00_MainContent_SubContent_SubContent_ctl00_listRepeater_ctl00_cardImage").attrs["src"]

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        self._name = re.sub(r".*\((.*)\)", r"\1", value)

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, value: str) -> None:
        self._image = ""
        match = re.match(r".*multiverseid=(\d+).*", value)
        if match:
            img_url = self.__image_url.format(match.group(1))
            response = requests.get(img_url)
            if response.status_code == 200:
                self._image = base64.b64encode(response.content).decode("ascii")

    def to_json(self) -> None:
        with open('test.json', 'w') as file:
            json.dump(self.__dict__, file)
