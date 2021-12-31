from os import listdir
from os.path import isfile, join
import nltk
from nltk.corpus import names
import sys
from nltk import word_tokenize
from shutil import copyfile


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
    male_names = names.words('male.txt')
    female_names = names.words('female.txt')
    for f in files:
        filepath = path + "/" + f
        words = word_tokenize(f)
        hasSorted = False
        for word in words:
            if word in male_names and word in female_names:
                moveFile(filepath, "unknown/"+word+" "+f)
                hasSorted = True
                break
            elif word in male_names:
                moveFile(filepath, "male/"+word +" "+f)
                hasSorted = True
                break
            elif word in female_names:
                moveFile(filepath, "female/"+word+" "+f)
                hasSorted = True
                break
        if not hasSorted:
            moveFile(filepath, "unknown/"+f)


if __name__ == "__main__":
    main()
