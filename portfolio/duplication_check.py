from PIL import Image
import hashlib
import os


def check(filename):
    a = None
    md5hash1 = hashlib.md5(Image.open(filename).tobytes())
    md5hash1.hexdigest()
    dir = cwd+'/media/Files'
    list1 = []
    for root, dirs, files in os.walk(dir):
        for file in files:
            path = os.path.join(dir, file)
            md5hash = hashlib.md5(Image.open(path).tobytes())
            md5hash.hexdigest()
            if md5hash.hexdigest() == md5hash1.hexdigest():
                a = 'Similar'
    return a
