# coding=utf-8
from os import path
import os
import sys


class Cr_work_env:
    db_dir = ''
    log_dir = ''
    config_file = ''
    chromedirver = ''

    __stat_db_name__ = 'crawler_stat_db.json'
    stat_db_fullname = ''

    def __init__(self, base_dir):
        self.setup_env(base_dir)

    def setup_env(self, base_dir):
        if not path.isdir(base_dir):
            raise BaseException('specified base_dir not found')

        self.db_dir = path.join(base_dir, '__stored')
        if not path.isdir(self.db_dir):
            os.mkdir(self.db_dir)
        self.stat_db_fullname = path.join(self.db_dir, self.__stat_db_name__)

        self.log_dir = path.join(base_dir, '__log_dir')
        if not path.isdir(self.log_dir):
            os.mkdir(self.log_dir)

        self.config_file = path.join(base_dir, '__config', 'proj.cfg')

        self.chromedirver = path.join(base_dir, 'chromedriver', 'chromedriver.exe')

    def get_db_file_fullname(self, name):
        if not path.isdir(self.db_dir):
            raise BaseException('specified db_dir not found')
        return path.join(self.db_dir, name)

    def get_log_file_fullname(self, name):
        if not path.isdir(self.log_dir):
            raise BaseException('specified db_dir not found')
        return path.join(self.log_dir, name)

    def get_config_file(self):

        if path.isfile(self.config_file):
            return self.config_file
        raise BaseException('not found config file: ' + self.config_file)


if sys.argv.__len__() != 2:
    raise Exception('wrong count of arguments')

work_env = Cr_work_env(sys.argv[1])
