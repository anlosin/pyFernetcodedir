import fernet
import os

files = []
for file in os.listdir():
    if file == "加密.py" or file == "thekey.key" or file == "解密.py" or file == "加密.exe" or file == "解密.exe":
        continue
    if os.path.isfile(file):
        files.append(file)
with open("thekey.key", "rb") as key:
    rightkey = key.read()
a = "luck安"
b = input("请输入正确的口令：\n")
if a == b:
    for file in files:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_decrypted = fernet.Fernet(rightkey).decrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_decrypted)
        print("恭喜，你的文件已成功解锁")
else:
    print("口令出错")
