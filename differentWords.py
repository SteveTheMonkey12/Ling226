import sys
import nltk
from nltk import word_tokenize

def main():
    try:
        path = sys.argv[1]
    except:
        print("no given filename")
        return

    with open(path+"mostCommonMale.txt", "r") as f:
        male = f.readlines()
    with open(path+"mostCommonFemale.txt", "r") as f:
       female = f.readlines()

    malestr = ""
    femalestr = ""
    for word in male:
        for letter in word:
            if letter.isalpha():
                malestr += letter
        malestr += " "
    for word in female:
        for letter in word:
            if letter.isalpha():
                femalestr += letter
        femalestr += " "
    print("\n\nfemale: ")

    for word in femalestr.split():
        if word not in malestr:
            print(word)
    print("\n\nmale: ")
    for word in malestr.split():
        if word not in femalestr:
            print(word)


if __name__ == "__main__":
    main()
