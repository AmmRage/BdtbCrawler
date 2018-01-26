# coding=utf-8
import configparser

from src.general_work_env import work_env

class CrConfig:

    oss_key = ''
    oss_secret = ''
    oss_endpoint = ''
    oss_bucket_name = ''

    localstore = ''

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(work_env.get_config_file(), encoding='utf-8')

        self.oss_key = config['alioss']['key']
        self.oss_secret = config['alioss']['secret']
        self.oss_endpoint = config['alioss']['endpoint']
        self.oss_bucket_name = config['alioss']['bucket_name']

        self.localstore = config['general']['localstore']

if __name__ == '__main__':
    conf = CrConfig()
    print(conf.oss_key)
    print(conf.oss_secret)
    print(conf.oss_endpoint)
    print(conf.oss_bucket_name)

    print(conf.localstore)
