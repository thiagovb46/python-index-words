def normalizeString (word):
    
    word = word.lower()
    word = word.rstrip()
    return word


import argparse
parser = argparse.ArgumentParser(description = "Files")
parser.add_argument("base")
parser.add_argument("consulta")
args = parser.parse_args()

base = open(args.base)
search = open(args.consulta)#Open a  file with content to be searched

wordsToSearch = search.readline();
wordsToSearch = normalizeString(wordsToSearch);

baseToSearch = base.readline();
baseToSearch = normalizeString(baseToSearch);

print(baseToSearch);
print(wordsToSearch);
