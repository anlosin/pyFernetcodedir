import datetime
import os
import shutil
from functools import partial
from tempfile import TemporaryDirectory

from cryptography.fernet import Fernet


class SecMod:
    def __init__(self):
        self.files = []
        for file in os.listdir():
            # 排除特定文件
            if file == "加密.exe" or file == "解密.exe":
                continue
            if os.path.isfile(file):
                # 获取该路径下文件的list列表
                self.files.append(file)

    def encrypt(self):
        """
        加密文件
        """
        key = Fernet.generate_key()
        temp_dir = TemporaryDirectory()
        start_time = datetime.datetime.now()
        for file in self.files:
            with open(file, "rb", buffering=0) as t, open(temp_dir.name + file, "ab+") as f:
                # 文件头2位写入key的长度，之后写入key，然后通过流形式写入一个临时文件，完成后替换当前文件
                f.write(len(key).to_bytes(2, 'big'))
                f.write(key)
                for chunk in chunked_file_reader(t):
                    # print(len(Fernet(key).encrypt(chunk)))
                    f.write(Fernet(key).encrypt(chunk))
                shutil.copy(temp_dir.name + file, file)
        use_time = datetime.datetime.now() - start_time
        print(use_time)

    def decrypt(self):
        """
        解密文件
        :return:
        """
        try:
            temp_dir = TemporaryDirectory()
            start_time = datetime.datetime.now()
            for file in self.files:
                with open(file, "rb", buffering=0) as t, open(temp_dir.name + file, "ab+") as f:
                    # 通过文件头两位得知key长度，之后读取key并解密
                    key_len = t.read(2)
                    right_key = t.read(int.from_bytes(key_len, 'big'))
                    for chunk in chunked_file_reader(t, block_size=22369720):
                        f.write(Fernet(right_key).decrypt(chunk))
                    shutil.copy(temp_dir.name + file, file)
            use_time = datetime.datetime.now() - start_time
            print(use_time)

            print("恭喜，你的文件已成功解锁")
        except IOError:
            pass


def chunked_file_reader(file, block_size=1024 * 1024 * 16):
    """生成器函数：分块读取文件内容，使用 iter 函数
    """
    # 首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    # 循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    # 加密段每次读取1M 解密段每次需读取1398200字节
    # 1 1398200
    # 4 5592504
    # 16 22369720
    # 64 89478584
    for chunk in iter(partial(file.read, block_size), b''):
        yield chunk


if __name__ == '__main__':
    os.chdir("D:\\a")
    sm = SecMod()
    sm.encrypt()
    sm.decrypt()
