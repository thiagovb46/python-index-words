
from ctypes import sizeof
from re import search
from typing import final
from xml.dom.minidom import Element
import nltk
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

def booleanSearch (wordsToSearch, words, index):
    
    notSearches = []
    andSearches = []

    dictOfEachWord ={}
   
    for i in wordsToSearch:
         if(i in words):
             for j in index[i].keys():
                if(i  in dictOfEachWord):
                    dictOfEachWord[i].append(j)
                else:
                    dictOfEachWord[i] = [j]
    results = [];
    
    if('!' not in wordsToSearch and '&' not in wordsToSearch):
        for i in wordsToSearch:
            if(i in dictOfEachWord):
                for j in dictOfEachWord[i]:
                    results.append(j);
        return  results;

    results.clear();
    for i in list(dictOfEachWord.keys()):
        for j in  range (0, len(dictOfEachWord[i])):
            if(dictOfEachWord[i][j] not in results):
                results.append(dictOfEachWord[i][j]);
    
    #Appends on list notSearches all the words with not operator after
    for i in range(0,len(wordsToSearch)):
        if(wordsToSearch[i] == '!'):
            notSearches.append(wordsToSearch[i+1]);
    
    for i in list(dictOfEachWord.keys()):
        if(i in notSearches):
            for j in range(0,len(dictOfEachWord[i])):
                results.remove(dictOfEachWord[i][j]);
    #Removes from  the  result dictionary, documents that contains words with not operator
    # for i in notSearches:
    #     dictOfEachWord.pop(i);

    for i in range(len(wordsToSearch)):
        if(wordsToSearch[i] == '&'):
            if(wordsToSearch[i+1] == '!'):
                andSearches.append((wordsToSearch[i-1],wordsToSearch[i-1]));
            else:
                andSearches.append((wordsToSearch[i-1],wordsToSearch[i+1]));
    docsAnd = []
    docs = []
    docs1 = []
    indexestoRemove = []

    for i in  range(0,len(andSearches)):
         if((andSearches[i][0] in dictOfEachWord) and  (andSearches[i][1] in dictOfEachWord)):
            docs = dictOfEachWord[andSearches[i][0]].copy(); 
            docs1 = dictOfEachWord[andSearches[i][1]].copy();
            #  print(docs);
            #  print(docs1);
    docsAnd =  list(set(docs) & set(docs1));
            
    # # for j in range(0,len(docsAnd)):
    # #     if(docsAnd[j] not in results):
    # #         indexestoRemove.append(j);

    # for k in indexestoRemove:
    #             results.pop(k);
    # for k in results:
    #      if k not in docsAnd:
    #             results.remove(k);
    return list ( set(results) & set (docsAnd));

def main():
    parser = argparse.ArgumentParser(description = "Files")
    parser.add_argument("base")
    parser.add_argument("consulta")
    args = parser.parse_args()

    linksOfFiles = open(args.base);
    search = open(args.consulta)#Open a  file with content to be searched

    
    wordsToSearch = search.readline();
    wordsToSearch = normalizeString(wordsToSearch);
    wordsToSearch = wordsToSearch.split('|');

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
    
    indice.close()
    closeFiles(files)

    resultsOfBooleanSearch = []
    for i in range(0,len(wordsToSearch)):
       resultsOfBooleanSearch.append(booleanSearch(wordsToSearch[i], words, index));
       
    finalResult = []
    for i in  range( len(resultsOfBooleanSearch)):
        for j in range(len(resultsOfBooleanSearch[i])):
            if(files[resultsOfBooleanSearch[i][j]-1].name not in finalResult):
                finalResult.append(files[resultsOfBooleanSearch[i][j]-1].name);
    finalResult.sort()

    answer =open('resposta.txt', 'w+')
    print(len(finalResult));
    answer.writelines(str(len(finalResult)));
    answer.writelines('\n');
    for i in finalResult:
        print(i);
        answer.writelines(i+'\n');
    answer.close();
            # print(resultsOfBooleanSearch[i][j]-1)

main()