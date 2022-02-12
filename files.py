import nltk

linksOfFiles = open('links.txt') #Open the file with all links of files

files = [] #List of open files

stopwords = nltk.corpus.stopwords.words('portuguese') #List of stopwords

listOfFiles = linksOfFiles.readlines() # Create an array of files paths

wordsOfthisDocument = []
wordsOfEachDocument = []

filesContent = []

for i in range(0,len(listOfFiles)):
    listOfFiles[i] = listOfFiles[i].rstrip()
    files.append(open(listOfFiles[i]))

for j in range(0, len(files)):
    filesContent.append(files[j].readlines())

for i in range(0,len(filesContent)):
    for j in range(0,len(filesContent[i])):
        filesContent[i] [j] = filesContent[i] [j].rstrip()

for i in range(0,len(filesContent)):
    for j in range(0,len(filesContent[i])):
        #wordsOfEachDocument.append(nltk.word_tokenize(filesContent[i][j]))
        wordsOfthisDocument.append(nltk.word_tokenize(filesContent[i][j]))
    wordsOfEachDocument.append(wordsOfthisDocument.copy())
    wordsOfthisDocument.clear()

for i in range(0,len(wordsOfEachDocument)):
    for j in range (0, len(wordsOfEachDocument[i])):
        if wordsOfEachDocument[i][j] in stopwords:
            wordsOfEachDocument[i].remove(wordsOfEachDocument[i][j])

for i in range(0,len(wordsOfEachDocument)):
    for j in range (0, len(wordsOfEachDocument[i])):
        print(wordsOfEachDocument[i])
for i in range(0, len(files)):
    files[i].close()