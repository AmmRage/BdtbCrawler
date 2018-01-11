# encoding=utf-8

from requestium import Session, Keys
import re

from tieba_thread import Tbthread, Tbreply

tbDase = r'http://tieba.baidu.com/'
class TbCrawler():

    s = Session(webdriver_path='./chromedriver/chromedriver.exe', browser='chrome', default_timeout=15)
    threadJson = {}

    def __init__(self):
        # self.s.driver.set_window_position(-
        pass

    def getPage(self, url):
        self.s.driver.get(url)
        # elements = self.s.driver.xpath("//div[@class='i']")
        elements = self.s.driver.find_elements_by_class_name('i')
        t_List = list(map(lambda e: e.find_element_by_tag_name('a').get_attribute("href"), elements))

        for t in t_List: #threads
            # print(t)
            self.getThread(t)
            pass

    def getThread(self, t_url):
        self.s.driver.get(t_url)

        tb_thread = Tbthread(self.s.driver.current_url)

        replies = self.s.driver.find_elements_by_class_name('i')
        for r in replies:
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
            except:
                pass

            tb_thread.add_reply(tb_reply)

    def getLouzhonglou(self, lzlUrl):
        self.s.driver.get(lzlUrl)
        replies = self.s.driver.find_elements_by_class_name('i')
        return list(map(lambda e: e.text, replies))


if __name__ == '__main__':

    print(re.match("回复\(\d+\)", "回复(3)") == None)