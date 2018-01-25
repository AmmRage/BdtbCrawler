# coding=utf-8
import configparser


class CrConfig():

    oss_key = ''
    oss_secret = ''
    oss_endpoint = ''
    oss_bucket_name = ''

    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./config/proj.cfg', encoding='utf-8')

        self.oss_key = config['alioss']['key']
        self.oss_secret = config['alioss']['secret']
        self.oss_endpoint = config['alioss']['endpoint']
        self.oss_bucket_name = config['alioss']['bucket_name']


if __name__ == '__main__':
    conf = CrConfig()
    print(conf.oss_key)
    print(conf.oss_secret)
    print(conf.oss_endpoint)
    print(conf.oss_bucket_name)
