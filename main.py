import os

from CryptMod import CryptMod

if __name__ == '__main__':
    os.chdir(os.getcwd())
    sm = CryptMod(faster=True)
    for file in os.listdir():
        # 特定文件
        if file == "1.rmvb":
        #     continue
        # if os.path.isfile(file):
            sm.decrypt(file)
