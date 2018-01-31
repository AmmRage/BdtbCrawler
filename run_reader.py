# coding = utf-8

from tinydb import TinyDB, Query
from src import general_work_env as env


__table_loaded_pages_name__ = 'table_loaded_pages'
__table_thread_name__ = 'table_threads'
__table_database_id_name__ = 'table_database_id'



def read():
    dbfile = env.work_env.get_db_file_fullname(str.format('database_{0}.json', '0'))

    db = TinyDB(dbfile)
    table = db.table(__table_thread_name__)
    query = Query()

    dblen = len(table.all())
    print(dblen)

    # th = table.all()
    for th in table.all():
        print(len(th['thread']['replies']))
        print(th)

    db.close()


if __name__ == '__main__':
    read()