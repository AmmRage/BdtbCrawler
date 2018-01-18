# coding = utf-8
import re
from tinydb import TinyDB, Query


def store_page(pageUrl):
    db = TinyDB(r'.\stored\t_pages.json')
    table = db.table('loaded_pages')

    query = Query()

    if not table.search(query.url == pageUrl):
        table.insert({'url': pageUrl})
    else:
        print('exists')

def store_thread(thread):
    dbId = str(thread.id % 100)
    db = TinyDB(str.format(r'.\stored\thread_{0}.json', dbId))
    table = db.table('threads')

    query = Query()

    if not table.search(query.id == str(thread.id)):
        table.insert({'id': str(thread.id), 't_url': thread.url, 'thread': thread.tojson()})

def thread_existed(t_url):
    m = re.search("m\?kz=(\d+)", t_url)
    id = int(m.groups(0)[0])
    db = TinyDB(r'.\stored\t_id.json')
    table = db.table('thread_id')

    query = Query()
    if table.search(query.id == id):
        return True
    else:
        store_id(id)
        return False

def store_id(id):
    db = TinyDB(r'.\stored\thread_id.json')
    table = db.table('thread_id')
    query = Query()
    if not table.search(query.id == id):
        table.insert({'id': id})


if __name__ == '__main__':
    # db = TinyDB(r'.\stored\db.json')
    # table = db.table('name')
    # table.insert({'value': True})
    # print(table.all())
    store_page(r'www.baidu.com')
    pass