# encoding = utf-8

from tinydb import TinyDB, Query

def read():
    db = TinyDB(str.format(r'.\stored\thread_{0}.json', 10))
    table = db.table('threads')

    print(table.all())

if __name__ == '__main__':
    read()