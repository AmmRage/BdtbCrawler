# coding=utf-8

import logging
import os

from src import general_work_env as env

class Cr_Logger:
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

    logger_debug = logging.getLogger('debug')
    logger_debug.setLevel(logging.DEBUG)

    logger_info = logging.getLogger('info')
    logger_info.setLevel(logging.INFO)

    logger_warning = logging.getLogger('warning')
    logger_warning.setLevel(logging.WARNING)

    logger_error = logging.getLogger('error')
    logger_error.setLevel(logging.ERROR)

    def __init__(self):
        pid = str(os.getpid())
        fh = logging.FileHandler(env.work_env.get_log_file_fullname(pid + '_cr_debug.log'))
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger_debug.addHandler(fh)

        fh = logging.FileHandler(env.work_env.get_log_file_fullname(pid + '_cr_info.log'))
        fh.setLevel(logging.INFO)
        fh.setFormatter(self.formatter)
        self.logger_info.addHandler(fh)

        fh = logging.FileHandler(env.work_env.get_log_file_fullname(pid + '_cr_warning.log'))
        fh.setLevel(logging.WARNING)
        fh.setFormatter(self.formatter)
        self.logger_warning.addHandler(fh)

        fh = logging.FileHandler(env.work_env.get_log_file_fullname(pid + '_cr_error.log'))
        fh.setLevel(logging.ERROR)
        fh.setFormatter(self.formatter)
        self.logger_error.addHandler(fh)

    def check_dir(self):
        if not os.path.isdir(env.work_env.log_dir):
            os.mkdir(self.logdir)

    def debug(self, log):
        self.logger_debug.debug(log)

    def info(self, log):
        self.logger_info.info(log)

    def warning(self, log):
        self.logger_warning.warning(log)

    def error(self, log):
        self.logger_error.error(log)

cr_logger = Cr_Logger()


if __name__ == '__main__':
    logger = Cr_Logger()

    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
