import sys
import requests
from collections import defaultdict
import json
from os import listdir
import nltk 
from nltk import word_tokenize
import random
from os.path import isfile, join
import threading
import time
import concurrent.futures

def get_word_rating_resource(url):
    """helper function to get lexical resources for LING226 students
    resources are hosted on github as .txt in the form of Word\tValue\n
    """
    # read the raw text and split on newlines
    raw = requests.get(url).text.split('\n')

    # split each pair and convert value to rounded float
    # the if statement is there to avoid indexing errors when a row in a resource doesn't have complete data
    raw_list = [(pair.split('\t')[0], round(float(pair.split('\t')[1]), 3)) for pair in raw if len(pair.split('\t')) == 2]

    # create a dictionary and return it
    return dict(raw_list)


def lexicalResource(words, dic):
    avg = 0
    for index, word in enumerate(words):
        avg += dic.get(word, 0)
        #print(f"\t{index/len(words)*100:.2f}%")
    avg = avg/len(words)
    return avg
    
def averageEmotionRating(words, dic):
    avgs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    emotions = ["anger",
                "anticipation",
                "disgust",
                "fear",
                "joy",
                "negative",
                "positive",
                "sadness",
                "surprise",
                "trust"]
    for word in words:
        for index, emotion in enumerate(emotions):
            avgs[index] += dic.get(word, {}).get(emotion, 0)
    for i in range(len(avgs)):
        avgs[i] = avgs[i]/len(words)
    return avgs


def thread_function(outputs, dicts, emotion_dict, path, maleWords, femaleWords):
    words = []
    output = []
    with open(path, 'r') as f2:
        data = json.load(f2)
        for text in data:
            for word in word_tokenize(text.get('text')):
                words.append(word)
    print("words loaded")
    for i, dic in enumerate(dicts):
        output.append(lexicalResource(words, dic))
        #print(f'lexicon {i} added')
    emotions = averageEmotionRating(words, emotion_dict)
    #print(emotions)
    for emotion in emotions:
        #print(f"emotion {emotion} added")
        output.append(emotion)
    print("emotions added")
    numMaleWords = 0
    numFemaleWords = 0
    for word in words:
        if word in maleWords:
            numMaleWords += 1
        if word in femaleWords:
            numFemaleWords += 1
    output.append(numMaleWords)
    output.append(numFemaleWords)
    print("male/female words added")
    if "/male" in path:
        output.append("m\n")
    elif "/female" in path:
        output.append("f\n")
    outputs.append(output)
    


def main():
    urls = ['https://raw.githubusercontent.com/scs-vuw/LING226/main/subtlxus_frequency.txt',
            'https://raw.githubusercontent.com/scs-vuw/LING226/main/AoA_Brysbart.txt',
            'https://raw.githubusercontent.com/scs-vuw/LING226/main/concreteness.txt',
            'https://raw.githubusercontent.com/scs-vuw/LING226/main/semantic_diversity.txt',
            'https://raw.githubusercontent.com/scs-vuw/LING226/main/humor.txt',
            'https://raw.githubusercontent.com/scs-vuw/LING226/main/AFINN-111.txt']
            
    dicts = []
    
    emotion_url = 'https://raw.githubusercontent.com/scs-vuw/LING226/main/emotion_lexicon.txt'
    raw_emotion = requests.get(emotion_url).text.split('\n')
    emotion_list = [(triple.split('\t')[0], triple.split('\t')[1], round(float(triple.split('\t')[2]),2)) for triple in raw_emotion]
    emotion_dict = defaultdict(dict)
    for index, triple in enumerate(emotion_list):
        word, category, value = triple
        emotion_dict[word][category] = value
    
    for url in urls:
    	dicts.append(get_word_rating_resource(url))

    try:
        path = sys.argv[1]
    except:
        print("no given filename")
        
    try:
        maleFiles = [f for f in listdir(path+"/male") if isfile(join(path+"/male", f))]
    except:
        print("male files invalid")
        return

    try:
        femaleFiles = [f for f in listdir(path+"/female") if isfile(join(path+"/female", f))]
    except:
        print("files invalid")
        return
    with open(path + "/mostCommonMale.txt") as f:
        maleWords = word_tokenize(f.read())
    with open(path + "/mostCommonFemale.txt") as f:
        femaleWords = word_tokenize(f.read())
    #print(maleFiles)
    threads = list()
    outputs = []
    for index, f in enumerate(maleFiles):
        print(f'{index/len(maleFiles)*100:.2f}% complete')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(thread_function, outputs, dicts, emotion_dict, path + "/male/" + f, maleWords, femaleWords)
    for index, f in enumerate(femaleFiles):
        print(f'{index/len(femaleFiles)*100:.2f}% complete')
        with concurrent.futures.ThreadPoolExecutor() as executor:
            executor.submit(thread_function, outputs, dicts, emotion_dict, path + "/female/" + f, maleWords, femaleWords)
    with open("testingData.txt", 'w') as f:
        f.write('')
    with open("trainingData.txt", 'w') as f:
        f.write('')
    with open("allData.txt", 'w') as f:
        f.write('')
    for output in outputs:
        randomNum = random.randint(1,10)
        with open("allData.txt", 'a') as f:
            f.write(' '.join(str(e) for e in output))
        if randomNum == 10:
            with open("testingData.txt", 'a') as f:
                f.write(' '.join(str(e) for e in output))
        else:
            with open("trainingData.txt", 'a') as f:
                f.write(' '.join(str(e) for e in output))


if __name__ == "__main__":
    main()
