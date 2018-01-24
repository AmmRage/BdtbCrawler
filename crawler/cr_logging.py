# coding=utf-8

import logging

import os

logdir = r'.\cr_logdir'

if not os.path.isdir(logdir):
    os.mkdir(logdir)

logging.basicConfig(filename=r'.\cr_logdir\error.log', level=logging.ERROR)
logging.basicConfig(filename=r'.\cr_logdir\info.log', level=logging.INFO)
logging.basicConfig(filename=r'.\cr_logdir\warning.log', level=logging.WARNING)

logger = logging.getLogger('cr_log')

logger.setLevel(logging.DEBUG)
# create file handler which logs even debug messages
fh = logging.FileHandler('spam.log')
fh.setLevel(logging.DEBUG)
# create console handler with a higher log level
# ch = logging.StreamHandler()
# ch.setLevel(logging.ERROR)
# create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# ch.setFormatter(formatter)
fh.setFormatter(formatter)
# add the handlers to logger
# logger.addHandler(ch)
logger.addHandler(fh)



def log_info(log):
    logging.info(log)

def log_error(log):
    logging.error(log)

def log_warning(log):
    logging.warning(log)



if __name__ == '__main__':
    # log_error('This message should go to the log file')
    # log_info('So should this')
    # log_warning('And this, too')

    # 'application' code
    logger.debug('debug message')
    logger.info('info message')
    logger.warn('warn message')
    logger.error('error message')
    logger.critical('critical message')