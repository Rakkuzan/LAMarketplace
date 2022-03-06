from marketplace import Market
import pprint

def main():
    pp = pprint.PrettyPrinter(indent=1)

    market = Market()
    while True:
        market.screenShot()
        ret = market.getPagesFromSS()
        maxPages = ret[1]
        currentPage = ret[0]
        print(f'Page: {currentPage}')
        market.scanItemsFromSS()

        if maxPages == currentPage:
            break
        market.nextPage()
    pp.pprint(market.getScanedItems())

if __name__ == '__main__':
    main()

