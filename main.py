
from cmath import log, sqrt
from ctypes import sizeof
from re import T, search
from typing import final
from unittest import removeResult
from xml.dom.minidom import Element
import nltk
import math
import argparse

import string

from pkg_resources import WorkingSet

listofResults = []
def createTheListOfFiles(linksOfFiles):
    files = []
    listOfFiles = linksOfFiles.readlines()
    for i in range(0,len(listOfFiles)):
        listOfFiles[i] = listOfFiles[i].rstrip()
        files.append(open(listOfFiles[i]))
    return files

def storeFileContent(files):
    filesContent = []
    for j in range(0, len(files)):
        filesContent.append(files[j].readlines())
    return filesContent

#Returns the string received in lowerCase and without \n in the end of string
def normalizeString (word):
    
    word = word.lower()
    word = word.rstrip()

    return word

def normalizeList(filesContent):
    for i in range(0,len(filesContent)):
        for j in range(0,len(filesContent[i])):
            filesContent[i] [j] = normalizeString(filesContent[i] [j])

def tokenizeListOfWords(filesContent):
    wordsOfthisDocument = []
    wordsOfEachDocument = []
    for i in range(0,len(filesContent)):
        for j in range(0,len(filesContent[i])):
            wordsOfthisDocument.append(nltk.word_tokenize(filesContent[i][j]))
        wordsOfEachDocument.append(wordsOfthisDocument.copy())
        wordsOfthisDocument.clear()
    return wordsOfEachDocument

#Returns a list of StopWords in a tree dimention list
def removeStopwords (treeDimensionsList):

    stopwords = nltk.corpus.stopwords.words('portuguese') #List of stopwords in portuguese
    #Appends de ponctuation in stopwords
    for i in list(string.punctuation):
        stopwords.append(i)
    tobeDeleted = []
    for i in range(0,len(treeDimensionsList)):
        for j in range (0, len(treeDimensionsList[i])):
            for k in range(0,len(treeDimensionsList[i][j])):
                if treeDimensionsList[i][j][k] in stopwords:
                    tobeDeleted.append(treeDimensionsList[i][j][k]);
            for l in range(0,len(tobeDeleted)):
                treeDimensionsList[i][j].remove(tobeDeleted[l])
            tobeDeleted.clear()
    return treeDimensionsList;

def getWordRadical(treeDimensionsList):
    radicalExtractor =  nltk.stem.RSLPStemmer() 
    for i in range(0,len(treeDimensionsList)):
        for j in range (0, len(treeDimensionsList[i])):
            for k in range(0,len(treeDimensionsList[i][j])):
                treeDimensionsList[i][j][k] = radicalExtractor.stem(treeDimensionsList[i][j][k])
    return
    
def createsAnIndex(treeDimensionsList):

    index = {}
    for i in range(0,len(treeDimensionsList)):
        for j in range (0, len(treeDimensionsList[i])):
            for k in range(0,len(treeDimensionsList[i][j])):
                if(treeDimensionsList[i][j][k] in index and (i+1) in index[treeDimensionsList[i][j][k]].keys()):
                    index[treeDimensionsList[i][j][k]] [i+1] +=1
                else:
                    if(treeDimensionsList[i][j][k] in index):
                        index[treeDimensionsList[i][j][k]] [i+1] = 1
                    else:
                        index.update({treeDimensionsList[i][j][k]: {i+1: 1 } }) 
    return index;

def showIndex(words, index, indice):
    count = 0
    for i in words:
        for j in list(index[i].keys()):
            if(count==0):
                indice.write(str(i)+": "+str(j)+ ","+str(index[i][j])+" ")
                print(str(i)+": "+str(j)+ ","+str(index[i][j]), end=" ")
                count+=1
            else:
                indice.write (str(j)+","+str(index[i][j])+" ")
                print (str(j)+","+str(index[i][j]), end = " ")
        indice.write("\n")
        print()
        count = 0

def closeFiles (files):
    for i in range(0, len(files)):
        files[i].close()    
    return

def Tf(freq):
    return 1+math.log10(freq);

def Idf(term, totalDocs, index):
    countTerms = 0;
    if(term in index.keys()):
        countTerms = len(list(index[term].keys()))
    return math.log10(totalDocs/countTerms);

def main():
    parser = argparse.ArgumentParser(description = "Files")
    parser.add_argument("base")
    parser.add_argument("consulta")
    args = parser.parse_args()

    linksOfFiles = open(args.base);
    search = open(args.consulta)#Open a  file with content to be searched

    
    wordsToSearch = search.readline();
    wordsToSearch = normalizeString(wordsToSearch);
    wordsToSearch = wordsToSearch.split('&');

    for i in range(0, len(wordsToSearch)):
        wordsToSearch[i] = nltk.word_tokenize(wordsToSearch[i]);
    radicalExtractor =  nltk.stem.RSLPStemmer() 

    #Gets the radical of each word in ListOfWordsToSearch
    for i in range(0,len(wordsToSearch)):
        for j in range(0,len(wordsToSearch[i])):
            wordsToSearch[i][j] = radicalExtractor.stem(wordsToSearch[i][j]);
    
    stopwords = nltk.corpus.stopwords.words('portuguese') #List of stopwords in portuguese
    #Appends de ponctuation in stopwords
    ponc = list(string.punctuation);
    ponc.remove('!');
    ponc.remove('|');
    ponc.remove('&');

    for i in ponc:
        stopwords.append(i)

     #Open a file with links to the files that will be indexed

    files = createTheListOfFiles(linksOfFiles) #Declaration of array that store the list of files

    filesContent = storeFileContent(files)    
    normalizeList(filesContent)
    
    wordsOfEachDocument = tokenizeListOfWords(filesContent);
    removeStopwords(wordsOfEachDocument);
    getWordRadical(wordsOfEachDocument);
    
    index = createsAnIndex(wordsOfEachDocument);
    
    indice = open('indice.txt', 'w+')
    words = list(index.keys())
    words.sort()

    
    showIndex(words, index, indice);
    #print(index);
    closeFiles(files);

    indice.close()
    listOfWeigthVectors = []
    DocWeigthVector = []
    
    for j in range(1,len(files)+1):
        for  i in index.keys():
            if(j in index[i]):
                DocWeigthVector.append(round(Tf(index[i][j]) * Idf(i, len(files), index),4));
            else:
                DocWeigthVector.append(0);
        listOfWeigthVectors.append(DocWeigthVector.copy());
        DocWeigthVector.clear();

        pesos = open('pesos.txt','w+');


    for i in range(len(files)):
        print(files[i].name,end=": ");
        pesos.write(files[i].name+": ");
        for j in range(len(listOfWeigthVectors[i])):
            if(listOfWeigthVectors[i][j] != 0):
                pesos.write(words[j]+", "+str("%.4f"%listOfWeigthVectors[i][j])+" ");
                print(words[j]+", "+str("%.4f"%listOfWeigthVectors[i][j]), end=" ");
        print();
        pesos.write('\n');
    
    pesos.close();


    searches_ = []
    weigthSearchV = []
    for i in wordsToSearch:
        for j in i:
            searches_.append(j);
    
    for i in range(len(words)):
        if(words[i] in searches_):
            weigthSearchV.append(round(Tf(1)*Idf(words[i],len(files), index),4));
        else:
            weigthSearchV.append(0);

    listOfDistanceSearchToVector = []
    denoSumWeigthDoc = 0;
    denoSumWeigthSearch = 0;
    numerador = 0;

    for i in listOfWeigthVectors:
        for j in range(len(i)):
            numerador += i[j] * weigthSearchV[j];
            denoSumWeigthDoc += (i[j]**2);
            denoSumWeigthSearch+= (weigthSearchV[j]**2);
        listOfDistanceSearchToVector.append(numerador/(pow(denoSumWeigthDoc,1/2) * pow(denoSumWeigthSearch,1/2)));
        denoSumWeigthDoc = 0;
        denoSumWeigthSearch = 0;
        numerador = 0;
    numberOfResults = 0;
    
    for i in listOfDistanceSearchToVector:
        if(i>0.001):
            numberOfResults+=1;
    print(numberOfResults);
  
    listOfDistanceSearchToVector_aux = listOfDistanceSearchToVector.copy();
    result_ = []
    while(len(listOfDistanceSearchToVector)>0):
        for i in range (len(listOfDistanceSearchToVector)):
            if(i==0):
                max = listOfDistanceSearchToVector[0];
            else:
                if(listOfDistanceSearchToVector[i]>max):
                    max = listOfDistanceSearchToVector[i];
        result_.append((max,listOfDistanceSearchToVector_aux.index(max)));
        listOfDistanceSearchToVector.remove(max);
    
    resposta = open('resposta.txt','w+');
    for i in result_:
        if(i[0]>0.001):
            print(files[i[1]].name+" "+str("%.4f"%i[0]));
            resposta.write(files[i[1]].name+" "+str("%.4f"%i[0]));
            resposta.write("\n");
    
    resposta.close();
main()  