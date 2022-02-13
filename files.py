from locale import normalize
import string
import nltk

linksOfFiles = open('links.txt') #Open the file with all links of files

files = [] #List of open files

stopwords = nltk.corpus.stopwords.words('portuguese') #List of stopwords

listOfFiles = linksOfFiles.readlines() # Create an array of files paths

wordsOfthisDocument = []
wordsOfEachDocument = []

filesContent = []

def normalizeString (word):
    word = word.lower()
    word = word.rstrip()
    return word

for i in range(0,len(listOfFiles)):
    listOfFiles[i] = listOfFiles[i].rstrip()
    files.append(open(listOfFiles[i]))

for j in range(0, len(files)):
    filesContent.append(files[j].readlines())

for i in range(0,len(filesContent)):
    for j in range(0,len(filesContent[i])):
        # filesContent[i] [j] = filesContent[i] [j].rstrip()
        filesContent[i] [j] = normalizeString(filesContent[i] [j])

for i in range(0,len(filesContent)):
    for j in range(0,len(filesContent[i])):
        #wordsOfEachDocument.append(nltk.word_tokenize(filesContent[i][j]))
        wordsOfthisDocument.append(nltk.word_tokenize(filesContent[i][j]))
    wordsOfEachDocument.append(wordsOfthisDocument.copy())
    wordsOfthisDocument.clear()

# for i in range(0,len(wordsOfEachDocument)):
#      for j in range (0, len(wordsOfEachDocument[i])):
#         for k in range(0,len(wordsOfEachDocument[j])):
#             #if wordsOfEachDocument[i][j][k] in stopwords:
#             print(wordsOfEachDocument[i][j][k])

for i in range(0,len(wordsOfEachDocument)):
         print(wordsOfEachDocument[i])

for i in range(0, len(files)):
    files[i].close()