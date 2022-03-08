from marketplace import Market
from sheets import Sheets
import pprint

testData = ({'Harmony Shard Pouch (L)': ['0', '1', '0', '0'],
             'Honor Shard Pouch (L)': ['0', '2', '0', '0'],
             'Life Shard Pouch (L)': ['0', '3', '0', '0'],
             # 'Metallurgy: Basic Casting': ['0', '4', '0', '0'],
             # 'Metallurgy: Basic Folding': ['0', '5', '0', '0'],
             "Moon's Breath": ['0', '6', '0', '0'],
             'Powder of Sage': ['0', '7', '0', '0'],
             'abc': ['0', '10', '0', '0'],
             'Solar Protection': ['0', '8', '0', '0'],
             "Star's Breath": ['0', '9', '0', '0'],
             'Tailoring: Basic Design': ['0', '10', '0', '0'],
             'Tailoring: Basic Knots': ['0', '11', '0', '0'], },
            1646690620)


def main():
    pp = pprint.PrettyPrinter(indent=1)
    market = Market()

    while True:
        market.screenShot()
        ret = market.getPagesFromSS()
        maxPages = ret[1]
        currentPage = ret[0]
        print(f'Page: {currentPage}')
        market.scanItemsFromSS(['recentPrice'])  # scanning recentPrice only

        if maxPages == currentPage:
            break
        market.nextPage()

    ret = market.getScanedItems()
    pp.pprint(ret)


def testing1():
    sheets = Sheets()
    marketData, ts = testData

    # prepare row1
    row1 = sheets.readSheet('RAW DATA!A1:1')[0]
    list = ['ts']
    list.extend(marketData.keys())  # timestamp + marketData keys
    row1.extend(key for key in list if key not in row1)  # extends row1 by list omitting duplicated elements

    # prepare row to insert
    # makes sure elements are inserted under correct items
    insRow = []
    for i in range(len(row1)):
        insRow.append('')
    insRow[0] = ts
    for key in marketData:
        insRow[row1.index(key)] = marketData[key][1]  # inserting only recentPrice

    sheets.updateRow(row1, 'RAW DATA!A1:1')
    sheets.insertRow(insRow, 'RAW DATA!A2:2')


if __name__ == '__main__':
    main()
    # testing()
