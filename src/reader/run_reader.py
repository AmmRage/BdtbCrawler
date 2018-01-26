# coding = utf-8

from tinydb import TinyDB, Query

def func():
    return True

def read():
    db = TinyDB(str.format(r'.\stored\database_{0}.json', 1))
    table = db.table('table_threads')
    # allthreads = table.all()
    # print(len(allthreads))

    # print(table.all()[0])

if __name__ == '__main__':
    read()