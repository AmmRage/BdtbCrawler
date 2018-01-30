# coding=utf-8
import random

import src.crawler.tb_crawler
from src.crawler.util.cr_logging import cr_logger

baseUrlBeiguo = r'http://tieba.baidu.com/mo/m?kw=%E8%83%8C%E9%94%85'
baseUrlKangya = r'http://tieba.baidu.com/mo/m?kw=%E6%8A%97%E5%8E%8B'
baseUrlKangyaTemp = r'http://tieba.baidu.com/mo/m?kw=%E6%8A%97%E5%8E%8B&pn={0}'
baseUrlKangyaTemp = 'http://tieba.baidu.com/mo/m?pnum={0}&kw=%E6%8A%97%E5%8E%8B&lp=5009&pinf=1_2_0&sub=%E8%B7%B3%E9%A1%B5'

currentMaxPage = 74363


def run_crawler():
    pnList = list(range(0, 25000))
    listLen = len(pnList)

    cr = src.crawler.tb_crawler.TbCrawler()

    while (listLen > 0):
        index = pnList[random.randrange(0, len(pnList))]
        cr_logger.info("will process index: " + str(index))
        print("index: " + str(index))

        pageUrl = str.format(baseUrlKangyaTemp, str(index))
        try:
            cr.getPage(pageUrl)
            cr_logger.info('finish on page: ' + pageUrl)
            break
        except BaseException as ex:
            cr_logger.warning('getPage error detail: ' + str(ex))

        pnList.remove(index)
        listLen = len(pnList)
    cr.close()


if __name__ == '__main__':
    print("start crawling")
    run_crawler()
