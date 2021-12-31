import matplotlib
import matplotlib.pyplot as plt
import sys
import numpy as np
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)

def main():

    try:
        paths = sys.argv[1], sys.argv[2], sys.argv[3], 
    except:
        print("no given filename")
    datas = [[], [], []]
    for i, path in enumerate(paths):
        with open(path, 'r') as f:
            datas[i] = f.readlines()
        for index in range(len(datas[i])):
            datas[i][index] = datas[i][index].split(" ")
    
    maleData = [[], [], []]
    femaleData = [[], [], []]
    for i, dataFiles in enumerate(datas):
        for data in dataFiles:
            if "m\n" in data:
                maleData[i].append(data)
            elif "f\n" in data:
                femaleData[i].append(data)
    #print(maleData)
    dataNames = ["Average Word Frequency", 
                "Average Age of Acquisition", 
                "Average Concreteness",
                "Average Semantic Diversity Rating",
                "Average Humor Rating"]
    for i in range(len(dataNames)):
        fig = plt.figure(figsize =(15, 7))
        ax = fig.add_subplot()
        d = [list(float(d[i]) for d in maleData[0]), list(float(d[i]) for d in femaleData[0]),
            list(float(d[i]) for d in maleData[1]), list(float(d[i]) for d in femaleData[1]),
            list(float(d[i]) for d in maleData[2]), list(float(d[i]) for d in femaleData[2])]
        plt.title(dataNames[i])
        ax.grid(True)
        ax.xaxis.set_major_locator(MultipleLocator(0.2))
        ax.yaxis.set_major_locator(MultipleLocator(0.2))
        ax.xaxis.set_minor_locator(AutoMinorLocator(0.04))
        ax.yaxis.set_minor_locator(AutoMinorLocator(0.04))
        ax.grid(which='major', color='#CCCCCC', linestyle='--')
        ax.grid(which='minor', color='#CCCCCC', linestyle=':')
        ax.set_xticklabels(["Laugh Factory Male", "Laugh Factory Female", "Dry Bar Male", "Dry Bar Female", "TED Male", "TED Female"])
        plt.boxplot(d)
        plt.savefig("data/" + dataNames[i])

    emotion = ["Anger",
                "Anticipation",
                "Disgust",
                "Fear",
                "Joy",
                "Negative",
                "Positive",
                "Sadness",
                "Surprise",
                "Trust"]
    for i in range(len(emotion)):
        fig = plt.figure(figsize =(15, 7))
        ax = fig.add_subplot()
        d = [list(float(d[i+6]) for d in maleData[0]), list(float(d[i+6]) for d in femaleData[0]),
            list(float(d[i+6]) for d in maleData[1]), list(float(d[i+6]) for d in femaleData[1]),
            list(float(d[i+6]) for d in maleData[2]), list(float(d[i+6]) for d in femaleData[2])]
        plt.title(emotion[i])
        ax.grid(True)
        ax.xaxis.set_major_locator(MultipleLocator(0.02))
        ax.yaxis.set_major_locator(MultipleLocator(0.02))
        ax.xaxis.set_minor_locator(AutoMinorLocator(0.004))
        ax.yaxis.set_minor_locator(AutoMinorLocator(0.004))
        ax.grid(which='major', color='#CCCCCC', linestyle='--')
        ax.grid(which='minor', color='#CCCCCC', linestyle=':')
        ax.set_xticklabels(["Laugh Factory Male", "Laugh Factory Female", "Dry Bar Male", "Dry Bar Female", "TED Male", "TED Female"])

        plt.boxplot(d)
        plt.savefig("data/" + emotion[i])

        

if __name__ == "__main__":
    main()
