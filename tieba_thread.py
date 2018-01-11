# encoding = utf-8

import json
import re


class Tbthread:
    url = ""
    id = 0
    replies = list()

    def __init__(self, url):
        self.url = url
        try:
            m = re.search("m\?kz=(\d+)", url)
            self.id = int(m.groups(0)[0])
        except:
            self.id = 0


    def add_reply(self, reply):
        self.replies.append(reply)

    def tojson(self):
        return ""

class Tbreply:
    content = ""
    reply_author = ""
    lzl = list()

    def __init__(self, content, author):
        self.content = content
        self.reply_author = author


    def add_lzl(self, lzl_reply):
        self.lzl.append(lzl_reply)


if __name__ == "__main__":
    url = ""
    m = re.search("m\?kz=(\d+)", url)
    print(m)