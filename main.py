import os

from CryptMod import CryptMod

if __name__ == '__main__':
    os.chdir(os.getcwd())
    sm = CryptMod()
    for file in os.listdir():
        # 特定文件
        if file == "main.py" or file == 'CryptMod.py':
            continue
        if os.path.isfile(file) and file == 'key words.txt':
            sm.decrypt(file)
