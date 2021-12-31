from os import listdir
from os.path import isfile, join
import nltk
import sys
from nltk import word_tokenize
from shutil import copyfile
import json

def moveFile(src, dst):
    copyfile(src, dst)
    print(dst)


def main():
    try:
        path = sys.argv[1]
    except:
        print("no given filename")
        return
    try:
        files = [f for f in listdir(path) if isfile(join(path, f))]
    except:
        print("files invalid")
        return
    with open("allwords.txt", 'w') as allwords:
        for f in files:
            filepath = path + "" + f
            #print(filepath)
            try:
                with open(filepath, 'r') as f2:
                    print("file opened")
                    data = json.load(f2)
                    for text in data:
                        allwords.write(text.get('text') + "\n")
            except:
                print("file opening failed")

if __name__ == "__main__":
    main()
