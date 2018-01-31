# coding=utf-8
import traceback

from flask import Flask
from hurry.filesize import size, si
import ctypes
import os
import platform
import sys
from flask import render_template
import datetime
from src.general_work_env import work_env


if len(sys.argv) != 2:
    print('wrong arguements')
    sys.path.insert(0, sys.argv[1])



work_env.setup_env(sys.argv[1])

from src.crawler.db.tb_store import get_oss_size
from src.general_work_env import work_env as env

app = Flask(__name__)


@app.route("/")
def hello():
    try:
        totalSize = 0
        for f in os.listdir(env.db_dir):
            fullname = os.path.join(env.db_dir, f)
            _fname, file_extension = os.path.splitext(fullname)
            if str.lower(file_extension) == '.json':
                totalSize += os.path.getsize(fullname)
        downloaded = size(totalSize)
        disc_spare = get_free_space_mb("C:\\")
        if disc_spare < 1000000000:
            # raise BaseException("no spare space")
            spare = "no spare space"
        else:
            spare = size(disc_spare, system=si)

        updated_time = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
        return render_template('index.html', size=downloaded, spare=spare, time=updated_time)
    except BaseException as ex:
        return traceback.format_exc()

@app.route("/oss")
def get_oss():
    oss_size = size(get_oss_size(), system=si)
    return render_template('oss.html', osssize=oss_size)


def get_free_space_mb(dirname):
    if platform.system() == 'Windows':
        free_bytes = ctypes.c_ulonglong(0)
        ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(dirname), None, None, ctypes.pointer(free_bytes))
        return free_bytes.value
    else:
        st = os.statvfs(dirname)
        return st.f_bavail * st.f_frsize

def run_main():
    try:
        # p = Process(target=run_crawler)
        # p.start()
        # p.join()
        app.run(host='0.0.0.0', port=10086)
    except BaseException as ex:
        print(str(ex))
        try:
            # p.terminate()
            pass
        except:
            pass
        pass

def test_network():
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":

    if len(sys.argv) != 2:
        print('wrong arguements')
    else:
        # src.general_work_env.work_env.setup_env(sys.argv[1])
        print('run main')
        run_main()
