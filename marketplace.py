import numpy
import pyautogui as pyag
import pytesseract.pytesseract
import pytesseract as pyt
import cv2
import time

pytesseract.pytesseract.tesseract_cmd = r'.\bin\Tesseract-OCR\tesseract.exe'


def crop(img, x, y, w, h, path=None):
    im = img.crop((x, y, x + w, y + h))
    if path is not None:
        im.save(path)
    return im


def pil2cv(im):
    im = numpy.array(im)
    im = cv2.cvtColor(im, cv2.COLOR_RGB2BGR)
    return im


def preprocessImg(im):
    im = pil2cv(im)
    im = cv2.resize(im, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
    im = ~im
    return im


def textRecognition(im, name):
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


class Market:
    def __init__(self):
        self.marketCoords = (2, 37, 1376 - 2, 860 - 37)  # x, y, w ,h

        # items
        self.firstItem = (250, 173)  # x, y of first item on the list
        self.itemDims = (1112, 55)  # width, height
        self.itemGap = 2  # gap between items
        self.itemCnt = 10

        # item (x, y, w, h)
        self.itemElCoords = {
            'name': (89, 4, 250, 44),
            'avgPrice': (421, 17, 100, 20),
            'recentPrice': (581, 17, 100, 20),
            'lowestPrice': (742, 17, 100, 20),
            'cheapestRem': (995, 17, 100, 20),
        }

        # pages (x, y, w, h)
        self.pagesCntCoords = (790, 757, 34, 20)

        self.nextPageBtnCoords = (873 + self.marketCoords[0], 767 + self.marketCoords[1])  # absolute coords
        self.refreshBtnCoords = (1329 + self.marketCoords[0], 107 + self.marketCoords[1])  # absolute coords
        self.firstPageBtnCoords = (716 + self.marketCoords[0], 767 + self.marketCoords[1])  # absolute coords

        self.ss = None
        self.marketItems = {}

    def screenShot(self):
        self.ss = pyag.screenshot(region=self.marketCoords)
        # self.ss.save(f'./screenshots/ss.png')

    def getPagesFromSS(self):
        pagesImg = crop(self.ss, self.pagesCntCoords[0], self.pagesCntCoords[1], self.pagesCntCoords[2],
                        self.pagesCntCoords[3])
        im = preprocessImg(pagesImg)
        text = textRecognition(im, 'pages')
        text = text.split('/')
        return [int(text[0]), int(text[1])]

    def scanItemsFromSS(self):
        ts = time.time()

        for i in range(self.itemCnt):
            itemImg = crop(self.ss, self.firstItem[0], self.firstItem[1] + i * (self.itemDims[1] + self.itemGap),
                           self.itemDims[0], self.itemDims[1])
            # itemImg = crop(self.ss, self.firstItem[0], self.firstItem[1] + i * (self.itemDims[1] + self.itemGap),
            #                self.itemDims[0], self.itemDims[1], f'./screenshots/test{i}.png')

            item = []
            for el in self.itemElCoords:
                # im = crop(itemImg, self.itemElCoords[el][0], self.itemElCoords[el][1], self.itemElCoords[el][2],
                #           self.itemElCoords[el][3], f'./screenshots/test{i}_{el}.png')
                im = crop(itemImg, self.itemElCoords[el][0], self.itemElCoords[el][1], self.itemElCoords[el][2],
                          self.itemElCoords[el][3])

                im = preprocessImg(im)
                # cv2.imwrite(f'./screenshots/test{i}_{el}.png', im)

                text = textRecognition(im, el)
                item.append(text)
            if item[0] == '':
                break
            self.marketItems[item[0]] = {'time': int(ts), 'avgPrice': item[1], 'recentPrice': item[2],
                                         'lowestPrice': item[3], 'cheapestRem': item[4]}

    def getScanedItems(self):
        return self.marketItems

    def nextPage(self):
        pyag.click(self.nextPageBtnCoords[0], self.nextPageBtnCoords[1])
        time.sleep(1)

    def firstPage(self):
        pyag.click(self.firstPageBtnCoords[0], self.firstPageBtnCoords[1])
        time.sleep(1)

    def refresh(self):
        pyag.click(self.refreshBtnCoords[0], self.refreshBtnCoords[1])
        time.sleep(1)

