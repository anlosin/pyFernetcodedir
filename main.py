import os

from CryptMod import CryptMod

if __name__ == '__main__':
    os.chdir(os.getcwd())
    sm = CryptMod(faster=True)
    for file in os.listdir():
        # 特定文件
        if file == "client-50072-chinatrc.com.cn.FTD-lidawei01_20231208035922.log":
        #     continue
        # if os.path.isfile(file):
            sm.decrypt(file)
