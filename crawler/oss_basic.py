# -*- coding: utf-8 -*-

import oss2

from crawler.configuration import CrConfig


class oss_store():

    conf = CrConfig()
    auth = None
    bucket = None

    def __init__(self):
        self.auth = oss2.Auth(self.conf.oss_key, self.conf.oss_secret)
        # 创建Bucket对象，所有Object相关的接口都可以通过Bucket对象来进行
        self.bucket = oss2.Bucket(self.auth, self.conf.oss_endpoint, self.conf.oss_bucket_name)

    def  get_buckets(self):
        service = oss2.Service(self.auth, self.conf.oss_endpoint)
        # 查看Bucket列表
        print([b.name for b in oss2.BucketIterator(service)])


    def upload_str(self, str):
        # 上传一段字符串。Object名是motto.txt，内容是一段名言。
        # self.bucket.put_object('motto.txt', 'Never give up. - Jack Ma')
        # 下载到本地文件
        # self.bucket.get_object_to_file('motto.txt', '本地文件名.txt')
        pass


    def download(self):
        # 把刚刚上传的Object下载到本地文件 “座右铭.txt” 中
        # 因为get_object()方法返回的是一个file-like object，所以我们可以直接用shutil.copyfileobj()做拷贝
        # with open(oss2.to_unicode('本地座右铭.txt'), 'wb') as f:
        #     shutil.copyfileobj(self.bucket.get_object('motto.txt'), f)
        pass


    def upload_file(self, oss_name, local_db_file):
        # 把本地文件 “座右铭.txt” 上传到OSS，新的Object叫做 “我的座右铭.txt”
        # 注意到，这次put_object()的第二个参数是file object；而上次上传是一个字符串。
        # put_object()能够识别不同的参数类型
        # with open(oss2.to_unicode('本地座右铭.txt'), 'rb') as f:
        #     self.bucket.put_object('云上座右铭.txt', f)

        # or

        # 上面两行代码，也可以用下面的一行代码来实现
        result = self.bucket.put_object_from_file(oss_name, local_db_file)
        return result.status == 200

    def enum_bucket_objects(self):
        # 列举Bucket下10个Object，并打印它们的最后修改时间、文件名
        # for i, object_info in enumerate(oss2.ObjectIterator(bucket)):
        #     print("{0} {1}".format(object_info.last_modified, object_info.key))
        #
        #     if i >= 9:
        #         break
        pass

    def delete_object(self):
        # 删除名为motto.txt的Object
        # self.bucket.delete_object('motto.txt')
        pass

    def batch_delete_objects(self):
        # 也可以批量删除
        # 注意：重复删除motto.txt，并不会报错
        # bucket.batch_delete_objects(['motto.txt', '云上座右铭.txt'])
        pass

    def exist_object(self):
        # 确认Object已经被删除了
        # assert not self.bucket.object_exists('motto.txt')
        pass

    def get_obj_safe(self):
        # 获取不存在的文件会抛出oss2.exceptions.NoSuchKey异常
        try:
            self.bucket.get_object('云上座右铭.txt')
        except oss2.exceptions.NoSuchKey as e:
            print(u'已经被删除了：request_id={0}'.format(e.request_id))
        else:
            assert False

    def get_bucket_stat(self):
        # 获取bucket相关信息
        bucket_info = self.bucket.get_bucket_info()
        print('name: ' + bucket_info.name)
        print('storage class: ' + bucket_info.storage_class)
        print('creation date: ' + bucket_info.creation_date)

        # 查看Bucket的状态
        bucket_stat = self.bucket.get_bucket_stat()
        print('storage: ' + str(bucket_stat.storage_size_in_bytes))
        print('object count: ' + str(bucket_stat.object_count))
        print('multi part upload count: ' + str(bucket_stat.multi_part_upload_count))


    def get_bucket_size(self):
        bucket_stat = self.bucket.get_bucket_stat()
        return bucket_stat.storage_size_in_bytes

if __name__ == '__main__':
    oss = oss_store()
    print(oss.upload_file("crawler_stat_db.json", r'.\stored\crawler_stat_db.json'))
    pass