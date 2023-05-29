import datetime
import shutil
from functools import partial
from tempfile import TemporaryDirectory

import cryptography


class SecMod(cryptography):
    def __init__(self):
        super.__init__(self)

    def encrypt(self, file):
        """
        加密文件
        """
        key = self.fernet.Fernet.generate_key()
        temp_dir = TemporaryDirectory()
        start_time = datetime.datetime.now()
        with open(file, "rb", buffering=0) as t, open(temp_dir.name + file, "ab+") as f:
            # 文件头2位写入key的长度，之后写入key，然后通过流形式写入一个临时文件，完成后替换当前文件
            f.write(len(key).to_bytes(2, 'big'))
            f.write(key)
            for chunk in chunked_file_reader(t):
                f.write(self.fernet.Fernet(key).encrypt(chunk))
            shutil.copy(temp_dir.name + file, file)
        use_time = datetime.datetime.now() - start_time
        print("Time costed : " + str(use_time))

    def decrypt(self, file):
        """
        解密文件
        """
        try:
            temp_dir = TemporaryDirectory()
            start_time = datetime.datetime.now()
            with open(file, "rb", buffering=0) as t, open(temp_dir.name + file, "ab+") as f:
                # 通过文件头两位得知key长度，之后读取key并解密
                key_len = t.read(2)
                right_key = t.read(int.from_bytes(key_len, 'big'))
                for chunk in chunked_file_reader(t, block_size=5592504):
                    f.write(self.fernet.Fernet(right_key).decrypt(chunk))
                shutil.copy(temp_dir.name + file, file)
            use_time = datetime.datetime.now() - start_time
            print("Time costed : " + str(use_time))
        except IOError:
            pass


def chunked_file_reader(file, block_size=1024 * 1024 * 4):
    """
    生成器函数：分块读取文件内容，使用 iter 函数
    首先使用 partial(fp.read, block_size) 构造一个新的无需参数的函数
    循环将不断返回 fp.read(block_size) 调用结果，直到其为 '' 时终止
    加密段每次读取1M 解密段每次需读取1398200字节
    1 1398200
    4 5592504
    16 22369720
    64 89478584
    """
    for chunk in iter(partial(file.read, block_size), b''):
        yield chunk
