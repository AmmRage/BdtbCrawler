# coding=utf-8

import os
from flask import Flask
from multiprocessing import Process
from os import walk
from hurry.filesize import size, si
from run_crawler import run_crawler
import ctypes
import os
import platform
import sys
from flask import render_template

app = Flask(__name__)


@app.route("/")
def hello():
    totalSize = 0
    for f in os.listdir('./stored/'):
        fullname = os.path.join(os.curdir, 'stored', f)
        _fname, file_extension = os.path.splitext(fullname)
        if str.lower(file_extension) == '.json':
            totalSize += os.path.getsize(fullname)
    downloaded = size(totalSize)
    disc_spare = get_free_space_mb("C:\\")
    if disc_spare < 1000000000:
        raise BaseException("no spare space")
    spare = size(disc_spare, system=si)
    return render_template('index.html', size=downloaded, spare=spare)


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
        p = Process(target=run_crawler)
        p.start()
        # p.join()
        app.run(host='0.0.0.0', port=10086)
    except:
        try:
            p.terminate()
        except:
            pass
        pass

def test_network():
    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    arglen = len(sys.argv)
    if arglen == 1:
        run_main()
    elif arglen == 2:
        print('test network')
        test_network()