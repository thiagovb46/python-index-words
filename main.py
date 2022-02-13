
import nltk

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
    indexFileCount = {}
    for i in range(0,len(treeDimensionsList)):
        for j in range (0, len(treeDimensionsList[i])):
            for k in range(0,len(treeDimensionsList[i][j])):
                if(treeDimensionsList[i][j][k] in index):
                    indexFileCount.update({i+1:indexFileCount[i+1]+1})
                else:
                    indexFileCount.update({i+1:1});
                    index.update({treeDimensionsList[i][j][k]:indexFileCount[i+1]}) 
    return index;
    
def closeFiles (files):
    for i in range(0, len(files)):
        files[i].close()
    return
    
def main():

    linksOfFiles = open('links.txt') #Open a file with links to the files that will be indexed

    files = createTheListOfFiles(linksOfFiles) #Declaration of array that store the list of files
    filesContent = storeFileContent(files)    
    normalizeList(filesContent)
    
    wordsOfEachDocument = tokenizeListOfWords(filesContent)
    removeStopwords(wordsOfEachDocument);
    getWordRadical(wordsOfEachDocument);

    index = createsAnIndex(wordsOfEachDocument);
    print(index)

    closeFiles(files)

main()