# coding = utf-8

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
        ret = {}
        ret["url"] = self.url
        ret["id"] = str(self.id)
        ret["replies"] = [r.tojson() for r in self.replies]
        return ret


class Tbreply:
    content = ""
    reply_author = ""
    lzl = list()

    def __init__(self, content, author):
        self.content = content
        self.reply_author = author

    def add_lzl(self, lzl_reply):
        self.lzl.append(lzl_reply)

    def tojson(self):
        ret = {}
        ret["author"] = self.reply_author
        ret["content"] = self.content
        # ret["lzl"] = [l.tojson() for l in self.lzl]
        ret["lzl"] = self.lzl

        return ret


if __name__ == "__main__":
    url = ""
    m = re.search("m\?kz=(\d+)", url)
    print(m)
