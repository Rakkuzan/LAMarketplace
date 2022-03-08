import numpy
import pyautogui as pyag
import pytesseract.pytesseract
import pytesseract as pyt
import cv2
import time
from sheets import Sheets

pytesseract.pytesseract.tesseract_cmd = r'.\bin\Tesseract-OCR\tesseract.exe'


class Market:
    def __init__(self):
        self.__marketCoords__ = (2, 37, 1376 - 2, 860 - 37)  # x, y, w ,h

        # items
        self.__firstItem__ = (250, 173, 1112, 55)  # x, y, w, h of first item on the list
        self.__itemDims__ = (1112, 55)  # width, height
        self.__itemGap__ = 2  # gap between items
        self.__itemCnt__ = 10

        # item (x, y, w, h)
        self.__itemElCoords__ = {
            'name': (89, 4, 250, 44),
            'avgPrice': (421, 17, 100, 20),
            'recentPrice': (581, 17, 100, 20),
            'lowestPrice': (742, 17, 100, 20),
            'cheapestRem': (995, 17, 100, 20),
        }

        # pages (x, y, w, h)
        self.__pagesCntCoords__ = (790, 757, 34, 20)

        # absolute coords
        self.__nextPageBtnCoords__ = (873 + self.__marketCoords__[0], 767 + self.__marketCoords__[1])
        self.__refreshBtnCoords__ = (1329 + self.__marketCoords__[0], 107 + self.__marketCoords__[1])
        self.__firstPageBtnCoords__ = (716 + self.__marketCoords__[0], 767 + self.__marketCoords__[1])

        self.__ss__ = None
        self.__marketItems__ = {}

    def __crop__(self, img, x, y, w, h, path=None):
        im = img.crop((x, y, x + w, y + h))
        if path is not None:
            im.save(path)
        return im

    def __pil2cv__(self, im):
        im = numpy.array(im)
        im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
        return im

    def __preprocessImg__(self, im):
        im = self.__pil2cv__(im)
        im = cv2.resize(im, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
        im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        im = ~im
        return im

    def __textRecognition__(self, im, name):
        # print(f'Element: {i}: {el}')
        if name == 'name':
            text = pyt.image_to_string(im, lang='eng')
        elif name == 'pages':
            text = pyt.image_to_string(im, lang='eng',
                                       config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789/')
        else:
            text = pyt.image_to_string(im, lang='eng',
                                       config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789,.-')
        text = text.split('\n')[0]
        return text

    def __click__(self, x, y):
        pyag.click(x, y)
        time.sleep(1)

    def __scanSingleItem__(self, itemImg, whitelist=None):
        if whitelist is None:
            scanCols = self.__itemElCoords__.keys()
        else:
            scanCols = ['name']
            scanCols.extend(whitelist)

        item = []
        for el in scanCols:
            im = self.__crop__(img=itemImg,
                               x=self.__itemElCoords__[el][0],
                               y=self.__itemElCoords__[el][1],
                               w=self.__itemElCoords__[el][2],
                               h=self.__itemElCoords__[el][3])

            im = self.__preprocessImg__(im)

            text = self.__textRecognition__(im, el)
            item.append(text)
        return item

    def screenShot(self):
        self.__ss__ = pyag.screenshot(region=self.__marketCoords__)
        # self.__ss__.save(f'./screenshots/ss.png')

    def getPagesFromSS(self):
        pagesImg = self.__crop__(img=self.__ss__,
                                 x=self.__pagesCntCoords__[0],
                                 y=self.__pagesCntCoords__[1],
                                 w=self.__pagesCntCoords__[2],
                                 h=self.__pagesCntCoords__[3])
        im = self.__preprocessImg__(pagesImg)
        text = self.__textRecognition__(im, 'pages')
        text = text.split('/')
        return [int(text[0]), int(text[1])]

    def scanItemsFromSS(self, whitelist=None):
        for i in range(self.__itemCnt__):
            itemImg = self.__crop__(img=self.__ss__,
                                    x=self.__firstItem__[0],
                                    y=self.__firstItem__[1] + i * (self.__firstItem__[3] + self.__itemGap__),
                                    w=self.__firstItem__[2],
                                    h=self.__firstItem__[3])

            item = self.__scanSingleItem__(itemImg, whitelist)
            if item[0] == '':
                break

            name = item.pop(0)
            self.__marketItems__[name] = item

    def getScanedItems(self):
        ts = time.time()
        return self.__marketItems__, int(ts)

    def nextPage(self):
        self.__click__(self.__nextPageBtnCoords__[0], self.__nextPageBtnCoords__[1])

    def firstPage(self):
        self.__click__(self.__firstPageBtnCoords__[0], self.__firstPageBtnCoords__[1])

    def refresh(self):
        self.__click__(self.__refreshBtnCoords__[0], self.__refreshBtnCoords__[1])
