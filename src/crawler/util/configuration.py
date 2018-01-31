# coding=utf-8
import configparser

from src import general_work_env as env


class CrConfig:
    oss_key = ''
    oss_secret = ''
    oss_endpoint = ''
    oss_bucket_name = ''

    local_store_dir = ''
    need_local_store = False

    def __init__(self):
        config = configparser.ConfigParser()
        config.read(env.work_env.get_config_file(), encoding='utf-8')

        self.oss_key = config['alioss']['key']
        self.oss_secret = config['alioss']['secret']
        self.oss_endpoint = config['alioss']['endpoint']
        self.oss_bucket_name = config['alioss']['bucket_name']

        self.local_store_dir = config['general']['local_store_dir']
        self.need_local_store = bool(config['general']['need_local_store'])


cr_proj_conf = CrConfig()

if __name__ == '__main__':

    print(cr_proj_conf.oss_key)
    print(cr_proj_conf.oss_secret)
    print(cr_proj_conf.oss_endpoint)
    print(cr_proj_conf.oss_bucket_name)

    print(cr_proj_conf.local_store_dir)
    print(cr_proj_conf.need_local_store)