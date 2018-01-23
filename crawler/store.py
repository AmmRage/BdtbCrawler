# coding = utf-8
import re
import os
from os import path
from zipfile import ZipFile, ZIP_DEFLATED
from tinydb import TinyDB, Query
from crawler.oss_basic import oss_store

stat_db_name = r'.\stored\crawler_stat_db.json'
oss = oss_store()

def store_page_url(pageUrl):
    db = TinyDB(stat_db_name)
    table = db.table('table_loaded_pages')
    query = Query()
    if not table.search(query.url == pageUrl):
        table.insert({'url': pageUrl})
    else:
        print('exists')
    db.close()

def store_thread(thread):
    dbId = str(get_database_id())
    dbfile = str.format(r'.\stored\database_{0}.json', dbId)

    if os.path.isfile(dbfile):
        if path.getsize(dbfile) > 100000000: # > 100 M
            dbzipfile = str.format(r'.\stored\database_{0}.zip', dbId)
            with ZipFile(dbzipfile, 'w', compression=ZIP_DEFLATED) as dbzip:
                dbzip.write(dbfile)
            oss.upload_file(str.format('database_{0}.zip', dbId), dbzipfile)

            dbfile = str.format(r'.\stored\database_{0}.json', dbId+1)

    if not db_id_exist(dbId):
        store_database_id(dbId)

    db = TinyDB(dbfile)
    table = db.table('table_threads')
    query = Query()
    if not table.search(query.id == str(thread.id)):
        table.insert({'id': str(thread.id), 't_url': thread.url, 'thread': thread.tojson()})
    db.close()

def thread_existed(t_url):
    m = re.search("m\?kz=(\d+)", t_url)
    id = int(m.groups(0)[0])
    db = TinyDB(stat_db_name)
    table = db.table('table_thread_id')
    query = Query()
    if table.search(query.t_id == id):
        db.close()
        return True
    else:
        store_thread_id(id)
        db.close()
        return False

def store_thread_id(id):
    db = TinyDB(stat_db_name)
    table = db.table('table_thread_id')
    query = Query()
    if not table.search(query.t_id == id):
        table.insert({'t_id': id})
    db.close()

def db_id_exist(dbid):
    db = TinyDB(stat_db_name)
    table = db.table('table_database_id')
    query = Query()
    if table.search(query.db_id == dbid):
        db.close()
        return True
    else:
        store_database_id(dbid)
        db.close()
        return False

def store_database_id(dbid):
    db = TinyDB(stat_db_name)
    table = db.table('table_database_id')
    query = Query()
    if not table.search(query.db_id == dbid):
        table.insert({'db_id': dbid})
    db.close()

def get_database_id():
    db = TinyDB(stat_db_name)
    table = db.table('table_database_id')
    all_ids =table.all()
    if len(all_ids) == 0:
        return 0
    id = max(all_ids)
    db.close()
    return id

def get_oss_size():
    return oss.get_bucket_size()

if __name__ == '__main__':
    # db = TinyDB(r'.\stored\db.json')
    # table = db.table('name')
    # table.insert({'value': True})
    # print(table.all())

    # store_page(r'www.baidu.com')

    pass

