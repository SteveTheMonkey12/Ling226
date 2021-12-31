import nltk
from nltk import word_tokenize
import sys
from nltk.corpus import stopwords

def main():
    try:
        path = sys.argv[1]
    except:
        print("no given filename")
        return

    with open(path, "r") as f:
        raw = f.read().replace('\n', ' ')

    tokens = [w.lower() for w in raw.split() if w.isalpha() and w.lower() not in stopwords.words('english')]
    fdist = nltk.FreqDist(tokens)
    with open("mostCommon.txt", 'w') as f:
        for word in fdist.most_common(100):
            f.write(f"{word}\n")


if __name__ == "__main__":
    main()
