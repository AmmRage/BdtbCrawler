# coding=utf-8

from requestium import Session
import re
import time
import random

from util.cr_logging import cr_logger
from db.store import thread_existed, store_thread, store_page_url
from model.model_tieba_thread import Tbreply, Tbthread

tbDase = r'http://tieba.baidu.com/'


class TbCrawler():
    s = Session(webdriver_path='./../chromedriver/chromedriver.exe',
                browser='chrome',
                default_timeout=15
                , webdriver_options={'arguments': ['headless', 'disable-gpu']}
                )
    threadJson = {}

    def __init__(self):
        pass

    def close(self):
        self.s.driver.close()
        self.s.close()

    def navigate(self, url):
        sleeptime = random.randint(1, 10)
        time.sleep(0.1 * sleeptime)
        self.s.driver.get(url)

    # process a page
    def getPage(self, url):
        try:
            self.navigate(url)
            # elements = self.s.driver.xpath("//div[@class='i']")
            elements = self.s.driver.find_elements_by_class_name('i')
            t_List = list(map(lambda e: e.find_element_by_tag_name('a').get_attribute("href"), elements))

            for t in t_List:  # threads
                try:
                    self.getThread(t)
                    cr_logger.info('finish on thread: ' + t)
                except BaseException as tex:
                    cr_logger.error('error in process thread: ' + t)
                    cr_logger.debug('error in process thread: ' + t)
                    cr_logger.debug('getThread error detail: ' + str(tex))
            store_page_url(url)
        except BaseException as pex:
            cr_logger.error('error in process page: ' + url)
            cr_logger.debug('error in process page: ' + url)
            cr_logger.debug('getPage error detail: ' + str(pex))

    # process a thread
    def getThread(self, t_url):
        if thread_existed(t_url):
            return
        self.navigate(t_url)
        tb_thread = Tbthread(self.s.driver.current_url)
        replies = self.s.driver.find_elements_by_class_name('i')
        for r in replies:
            reply_index = replies.index(r)
            author = r.find_element_by_tag_name('span').find_element_by_tag_name('a').text
            tb_reply = Tbreply(r.text, author)
            try:
                # check if has lou zhong lou
                huifu = r.find_element_by_class_name('reply_to').text

                if re.match("回复\(\d+\)", huifu) != None:
                    lzlUrl = r.find_elements_by_tag_name('a')[-1].get_attribute("href")
                    lzl_replies = self.getLouzhonglou(lzlUrl)
                    for lzl_r in lzl_replies:
                        tb_reply.add_lzl(lzl_r)
            except BaseException as lex:
                # if 0, it's the 1st reply, that no 'reply_to' there
                # to avoid the misleading error info in the log. we'd better not record it
                if len(tb_thread.replies) != 0 and reply_index == 0:
                    cr_logger.debug('error in getting lou zhong lou under: ' + t_url)
                    cr_logger.debug('error detail: ' + str(lex))
            tb_thread.add_reply(tb_reply)
        store_thread(tb_thread)

    # get lou zhu lou replies
    def getLouzhonglou(self, lzlUrl):
        self.navigate(lzlUrl)
        replies = self.s.driver.find_elements_by_class_name('i')
        return list(map(lambda e: e.text, replies))


if __name__ == '__main__':
    # print(re.match("回复\(\d+\)", "回复(3)") == None)

    # import datetime
    # print('start' + datetime.datetime.now().__str__())
    # sleeptime = random.randint(1, 10)
    # print (sleeptime)
    # time.sleep(0.1 * sleeptime)
    # print('exit' + datetime.datetime.now().__str__())

    pass
