# coding=utf-8
import traceback

from requestium import Session
import re
import time
import random

from selenium.webdriver.common.keys import Keys

from src.crawler.db.tb_store import store_page_url, thread_existed, store_thread
from src.crawler.model.model_tieba_thread import Tbthread, Tbreply
from src.crawler.util.cr_logging import cr_logger
from src import general_work_env as env

tbDase = r'http://tieba.baidu.com/'

class TbCrawler():
    s = Session(webdriver_path=env.work_env.chromedirver,
                browser='chrome',
                default_timeout=15
                # , webdriver_options={'arguments': ['headless']}
                # , webdriver_options={'arguments': ['headless', 'disable-gpu']}
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
            threads_url_list = list(map(lambda e: e.find_element_by_tag_name('a').get_attribute("href"), elements))

            for t in threads_url_list:  # threads
                t_index = threads_url_list.index(t)
                if t_index > 3:
                    break
                try:
                    self.getThread(t)
                    cr_logger.info('finish on thread: ' + t)
                except BaseException as tex:
                    cr_logger.error('error in process thread: ' + t)
                    cr_logger.debug('error in process thread: ' + t)
                    cr_logger.debug('getThread error detail: ' + traceback.format_exc())
            store_page_url(url)
        except BaseException as pex:
            cr_logger.error('error in process page: ' + url)
            cr_logger.debug('error in process page: ' + url)
            cr_logger.debug('getPage error detail: ' + str(pex))

    # process a thread
    def getThread(self, t_url):
        if thread_existed(t_url):
            return

        try:
            self.navigate(t_url)
            tb_thread = Tbthread(self.s.driver.current_url)
            replies = self.s.driver.find_elements_by_class_name('i')
        except BaseException as ex:
            raise BaseException('error in get thread and all replies: ' + str(ex))

        for r in replies:
            reply_index = replies.index(r)
            if reply_index > 2:
                break
            try:
                author = r.find_element_by_tag_name('span').find_element_by_tag_name('a').text
                tb_reply = Tbreply(r.text, author)
            except BaseException as ex:
                raise BaseException('error in get reply info: ' + str(ex))

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
                if len(tb_thread.replies) != 0:
                    cr_logger.debug('error in getting lou zhong lou under: ' + t_url)
                    cr_logger.debug('error detail: ' + str(lex))

            tb_thread.add_reply(tb_reply)
        store_thread(tb_thread)

    # get lou zhu lou replies
    def getLouzhonglou(self, lzlUrl):
        try:
            # new tab
            self.s.driver.execute_script("window.open('about:blank', 'tab2');")
            self.s.driver.switch_to.window("tab2")
            self.navigate(lzlUrl)
            replies = self.s.driver.find_elements_by_class_name('i')
            lzl_li = list(map(lambda e: e.text, replies))
            self.s.driver.execute_script("window.close('tab2');")

            tab_before = self.s.driver.window_handles[0]
            self.s.driver.switch_to.window(tab_before)

            return lzl_li
        except:
            return list()


if __name__ == '__main__':
    # print(re.match("回复\(\d+\)", "回复(3)") == None)

    # import datetime
    # print('start' + datetime.datetime.now().__str__())
    # sleeptime = random.randint(1, 10)
    # print (sleeptime)
    # time.sleep(0.1 * sleeptime)
    # print('exit' + datetime.datetime.now().__str__())

    # cr = TbCrawler()
    # cr.navigate('https://www.google.com.sg')
    #
    # ret = cr.s.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
    # print(ret)
    # cr.navigate('http://stackoverflow.com/')
    # ret = cr.s.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')
    # print(ret)
    # cr.close()
    pass
