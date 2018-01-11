# encoding = utf-8

from tinydb import TinyDB, Query


def store_page(pageUrl):
    db = TinyDB(r'.\stored\pages.json')
    table = db.table('loaded_pages')

    query = Query()

    if not table.search(query.url == pageUrl):
        table.insert({'url': pageUrl})
    else:
        print('exists')

def store_thread(id, url, thread):
    dbId = str(id % 100)
    db = TinyDB(str.format(r'.\stored\thread_{0}.json', dbId))
    table = db.table('threads')

    query = Query()

    if not table.search(query.id == str(id)):
        table.insert({'id': str(id), 't_url': url, 'thread': thread})

if __name__ == '__main__':
    # db = TinyDB(r'.\stored\db.json')
    # table = db.table('name')
    # table.insert({'value': True})
    # print(table.all())
    store_page(r'www.baidu.com')
    pass