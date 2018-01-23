# coding=utf-8
import random

from crawler.store import store_page_url
from crawler.tb_crawler import TbCrawler

baseUrlBeiguo = r'http://tieba.baidu.com/mo/m?kw=%E8%83%8C%E9%94%85'
baseUrlKangya = r'http://tieba.baidu.com/mo/m?kw=%E6%8A%97%E5%8E%8B'
baseUrlKangyaTemp = r'http://tieba.baidu.com/mo/m?kw=%E6%8A%97%E5%8E%8B&pn={0}'
baseUrlKangyaTemp = 'http://tieba.baidu.com/mo/m?pnum={0}&kw=%E6%8A%97%E5%8E%8B&lp=5009&pinf=1_2_0&sub=%E8%B7%B3%E9%A1%B5'

currentMaxPage = 74363


def run_crawler():

    pnList = list(range(0, 25000))
    listLen = len(pnList)

    cr = TbCrawler()

    while (listLen > 0):
        index = pnList[random.randrange(0, len(pnList))]
        print("index: " + str(index))

        pageUrl = str.format(baseUrlKangyaTemp, str(index))
        try:
            cr.getPage(pageUrl)
            store_page_url(pageUrl)
            pass
        except BaseException as ex:
            print(ex)

        pnList.remove(index)
        listLen = len(pnList)
    cr.close()



if __name__ == '__main__':
    run_crawler()


