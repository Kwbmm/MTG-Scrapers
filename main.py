from argparse import ArgumentParser
from scrapers.Gatherer import Gatherer
from scrapers.MagiccardsInfo import MagiccardsInfo


def main():
    parser = ArgumentParser(description="Magic the Gathering Card Scraper")
    allowed_scrapers = {"mtg-gatherer": Gatherer, "magiccards.info": MagiccardsInfo}
    parser.add_argument("-s", "--scraper", help="Scraper to use", type=str, choices=list(allowed_scrapers.keys()),
                        default="mtg-gatherer")
    args = parser.parse_args()
    scraper = allowed_scrapers[args.scraper]()


if __name__ == '__main__':
    main()
