import time

from marketplace import Market

class Bot:
    def __init__(self):
        self.__market__ = Market()

    def runOnce(self):
        while True:
            self.__market__.screenShot()
            ret = self.__market__.getPagesFromSS()
            maxPages = ret[1]
            currentPage = ret[0]
            self.__market__.scanItemsFromSS(['recentPrice'])  # scanning recentPrice only

            if maxPages == currentPage:
                break
            self.__market__.nextPage()

        self.__market__.saveToSheets()

    def runContinuously(self, delay=300):
        while True:
            self.__market__.firstPage()
            self.__market__.refresh()
            self.runOnce()
            time.sleep(delay)
