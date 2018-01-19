# coding=utf-8

import logging

import os

logdir = r'.\logdir'

if not os.path.isdir(logdir):
    os.mkdir(logdir)

logging.basicConfig(filename=r'.\cr_logdir\example.log',level=logging.ERROR)



logging.error('This message should go to the log file')
logging.info('So should this')
logging.warning('And this, too')