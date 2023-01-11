import datetime
import os
import shutil
import time
from functools import partial
from tempfile import TemporaryDirectory, NamedTemporaryFile
from cryptography.fernet import Fernet


class SecMod:
    def __init__(self):
        self.files = []
        # upath = unicode("D:\\运维手册", 'utf-8')
        os.chdir("D:\\a")
        for file in os.listdir():
            # 排除“自己人”
            if file == "file.key" or file == "加密.exe" or file == "解密.exe":
                continue
            if os.path.isfile(file):
                # 获取该路径下文件的list列表
                self.files.append(file)

    def encrypt(self):
        key = Fernet.generate_key()
        with open("file.key", "wb") as thekey:
            thekey.write(key)
        for file in self.files:
            with open(file, "rb", buffering=0) as thefile:
                _dir = TemporaryDirectory()
                temp_file = NamedTemporaryFile(dir=_dir.name, mode='w+b')
                start_time = datetime.datetime.now()
                for chunk in chunked_file_reader(thefile):
                    with temp_file as f:
                        f.write(Fernet(key).encrypt(chunk))
                shutil.copy(temp_file.name, file)
                use_time = datetime.datetime.now() - start_time
                print(use_time)

    def decrypt(self):
        try:
            with open("file.key", "rb", buffering=4096) as key:
                right_key = key.read()
            # for file in self.files:
            #     with open(file, "rb") as thefile:
            #         contents = thefile.read()
            #         start_time = datetime.datetime.now()
            #         contents_decrypted = Fernet(right_key).decrypt(contents)
            #         use_time = datetime.datetime.now() - start_time
            #         print(use_time)
            #     with open('b.avi', "ab+") as thefile:
            #         thefile.write(contents_decrypted)
            for file in self.files:
                start_time = datetime.datetime.now()
                with open(file, "rb", buffering=0) as thefile:
                    for chunk in chunked_file_reader(thefile):
                        with open("b.avi", "ab+") as f:
                            f.write(Fernet(right_key).decrypt(chunk))
                use_time = datetime.datetime.now() - start_time
                print(use_time)

            print("恭喜，你的文件已成功解锁")
        except IOError:
            pass

    def test(self):
        for file in self.files:
            start_time = datetime.datetime.now()
            with open(file, "rb", buffering=0) as thefile:
                for chunk in chunked_file_reader(thefile):
                    with open('a.avi', "ab+") as t:
                        t.write(chunk)
            use_time = datetime.datetime.now() - start_time
            print(use_time)


# def chunked_file_reader(file, block_size=1398200):
def chunked_file_reader(file, block_size=1024 * 1024):
    """生成器函数：分块读取文件内容，使用 iter 函数
    """
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    # 循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    for chunk in iter(partial(file.read, block_size), b''):
        yield chunk


if __name__ == '__main__':
    sm = SecMod()
    sm.encrypt()
