import os

from securedir import SecMod

if __name__ == '__main__':
    os.chdir(os.getcwd())
    sm = SecMod()
    for file in os.listdir():
        # 排除特定文件
        if file == "加密.exe" or file == "解密.exe":
            continue
        if os.path.isfile(file):
            # 获取该路径下文件的list列表
            sm.encrypt(file)
