from scrapers.BaseScraper import BaseScraper


class Gatherer(BaseScraper):
    __url = "https://gatherer.wizards.com/Pages/Default.aspx"

    def __init__(self):
        super().__init__(self.__url)
        self.__sets = [opt['value'].replace(" ", "+") for opt in self.bs_obj.select("select#ctl00_ctl00_MainContent_Content_SearchControls_setAddText option") if opt['value'] != '']
        print(self.__sets)
