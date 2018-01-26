# coding = utf-8
import re
import os
from os import path
from zipfile import ZipFile, ZIP_DEFLATED
from tinydb import TinyDB, Query
from src.general_work_env import work_env

from src.crawler.db.oss_basic import Oss_store
from src.crawler.util.cr_logging import cr_logger



oss = Oss_store()
__table_loaded_pages_name__ = 'table_loaded_pages'
__table_thread_name__ = 'table_threads'
__table_database_id_name__ = 'table_database_id'

def store_page_url(pageUrl):
    db = TinyDB(work_env.stat_db_fullname)
    table = db.table(__table_loaded_pages_name__)
    query = Query()
    if not table.search(query.url == pageUrl):
        table.insert({'url': pageUrl})
    else:
        cr_logger.warning(str.format('already loaded page. url: {0}', pageUrl))
        print('exists')
    db.close()


# store a thread object to database
def store_thread(thread):
    dbId = get_database_id()
    dbfile = work_env.get_db_file_fullname(str.format('database_{0}.json', str(dbId)))

    if os.path.isfile(dbfile):
        if path.getsize(dbfile) > 10000000:  # > 100 M
            dbzipfile = work_env.get_db_file_fullname(str.format('database_{0}.zip', dbId))
            with ZipFile(dbzipfile, 'w', compression=ZIP_DEFLATED) as dbzip:
                dbzip.write(dbfile, arcname=str.format(r'database_{0}.json', dbId))
            if oss.upload_file(str.format('database_{0}.zip', dbId), dbzipfile):
                os.remove(dbzipfile)
                os.remove(dbfile)
                cr_logger.info(str.format('finished uploading {0}', dbfile))

            dbfile = work_env.get_db_file_fullname(str.format('database_{0}.json', dbId + 1))
            dbId += 1

    if not db_id_exist(dbId):
        store_database_id(dbId)

    db = TinyDB(dbfile)
    table = db.table(__table_thread_name__)
    query = Query()
    if not table.search(query.id == str(thread.id)):
        table.insert({'id': str(thread.id), 't_url': thread.url, 'thread': thread.tojson()})
    db.close()
    cr_logger.info('finish store thread object with id: ' + str(thread.id) + ' to ' + dbfile)


def thread_existed(t_url):
    m = re.search("m\?kz=(\d+)", t_url)
    id = int(m.groups(0)[0])
    if not os.path.isfile(work_env.stat_db_fullname):
        return False
    db = TinyDB(work_env.stat_db_fullname)
    table = db.table(__table_database_id_name__)
    query = Query()
    if table.search(query.t_id == id):
        db.close()
        return True
    else:
        store_thread_id(id)
        db.close()
        return False


def store_thread_id(id):
    db = TinyDB(work_env.stat_db_fullname)
    table = db.table(__table_database_id_name__)
    query = Query()
    if not table.search(query.t_id == id):
        table.insert({'t_id': id})
    db.close()


def db_id_exist(dbid):
    db = TinyDB(work_env.stat_db_fullname)
    table = db.table(__table_database_id_name__)
    query = Query()
    if table.search(query.db_id == dbid):
        db.close()
        return True
    else:
        store_database_id(dbid)
        db.close()
        return False


def store_database_id(dbid):
    db = TinyDB(work_env.stat_db_fullname)
    table = db.table(__table_database_id_name__)
    query = Query()
    if not table.search(query.db_id == dbid):
        table.insert({'db_id': dbid})
    db.close()


def get_database_id():
    db = TinyDB(work_env.stat_db_fullname)
    table = db.table(__table_database_id_name__)
    all_ids = table.all()
    if len(all_ids) == 0:
        return 0
    id = max(all_ids)
    db.close()
    return id['db_id']


def get_oss_size():
    return oss.get_bucket_size()


if __name__ == '__main__':
    # db = TinyDB(db_dir + 'db.json')
    # table = db.table('name')
    # table.insert({'value': True})
    # print(table.all())

    # store_page(r'www.baidu.com')

    # print(get_database_id())
    # store_database_id(1)

    # with ZipFile(r'.\stored\x.zip', 'w', compression=ZIP_DEFLATED) as dbzip:
    #     dbzip.write(r'.\stored\crawler_stat_db.json', arcname='x.json')


    if not db_id_exist(0):
        store_database_id(0)
    print(db_id_exist(0))
    pass
