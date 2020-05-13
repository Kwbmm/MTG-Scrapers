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
    print("Input a set to display the cards in it")
    sets = scraper.get_sets()

    is_quit = False
    while not is_quit:
        for s in sets:
            print(s)
        set_name = input("Set name (or 'q' to quit): ")
        is_quit = set_name == 'q'
        if is_quit:
            continue
        for c in scraper.get_cards_for_set(set_name):
            print(c)


if __name__ == '__main__':
    main()
