
import nltk

linksOfFiles = open('links.txt') #Open the file with all links of files

files = [] #List of open files

stopwords = nltk.corpus.stopwords.words('portuguese') #List of stopwords

listOfFiles = linksOfFiles.readlines() # Create an array of files paths

wordsOfthisDocument = []
wordsOfEachDocument = []

filesContent = []
#Returns the string received in loweCase and without \n in the end of string
def normalizeString (word):
    word = word.lower()
    word = word.rstrip()
    return word

#Returns a list of StopWords in a tree dimention list
def removeStopwords (treeDimensionsList):
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

for i in range(0,len(listOfFiles)):
    listOfFiles[i] = listOfFiles[i].rstrip()
    files.append(open(listOfFiles[i]))

for j in range(0, len(files)):
    filesContent.append(files[j].readlines())

for i in range(0,len(filesContent)):
    for j in range(0,len(filesContent[i])):
        filesContent[i] [j] = normalizeString(filesContent[i] [j])


for i in range(0,len(filesContent)):
    for j in range(0,len(filesContent[i])):
        wordsOfthisDocument.append(nltk.word_tokenize(filesContent[i][j]))
    wordsOfEachDocument.append(wordsOfthisDocument.copy())
    wordsOfthisDocument.clear()

removeStopwords(wordsOfEachDocument);

for i in range(0,len(wordsOfEachDocument)):
        print(wordsOfEachDocument[i])

for i in range(0, len(files)):
    files[i].close()