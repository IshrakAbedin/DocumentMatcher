from os import listdir
import doxamE
from time import time as clock
from sys import argv
from math import log
import copy

helptext = 'Keep your documents inside Dir folder. Type in just the name of the document with extension you want to find match with.'
helpwords = ['h', 'H', 'help', '-h', '-H', '-help', '--h', '--H', '--help',]
if len(argv) < 2 or len(argv) > 2:
    print('Type \'-h or -help\' to get help')
    print('\nPress any key to exit ... ...')
    input()
    exit()
elif argv[1] in helpwords:
    print(helptext)
    print('\nPress any key to exit ... ...')
    input()

target = argv[1]

tf = {}
df = {}
tfidf = {}
tokens = {}
path = './Dir'
files = []

print('Finding trivial matches with ', target, ' ... ... ...')

for file in listdir(path):
    if ('.pdf' in file) or ('.doc' in file) or ('.docx' in file) or ('.txt' in file) or ('.pptx' in file):
            files.append(file)

if target not in files:
    print('Cannot find the file ', target)
    print('\nPress any key to exit ... ...')
    input()
    exit()

filecount = len(files)
realfilecount = filecount
print("Searching through %d files" % (filecount))
start_time = clock()
current_time = 0
minus = 0

done_counter = 1
for file in files:
    tf[file], minus = doxamE.getTF('./Dir/'+file)
    realfilecount -= minus
    current_time = clock()
    remaining_time = ((current_time - start_time) / done_counter) * (filecount - done_counter)
    print('%d/%d done ... ... %dM %dS remaining' % (done_counter, filecount , remaining_time / 60, remaining_time % 60))
    done_counter += 1

df = doxamE.getDF(tf)

tfidf = copy.deepcopy(df)

for file in tfidf:
        for word in tfidf[file]:
            tfw = tf[file][word]
            dfw = df[file][word]
            tfidf[file][word] = tfw * log(realfilecount / dfw)# relation here

for file in files:
    tokens[file] = doxamE.getNword(tfidf[file], 20)

print('Parsing Complete.')
res = {}
for file in files:
    if file != target and len(tokens[file]) != 0:
        res[file] = len(tokens[target].intersection(tokens[file])) / len(tokens[target].union(tokens[file])) 

print('Processing Complete, showing results:\n')
rank = 1
for key, value in sorted(res.items(), key=lambda item: item[1], reverse = True):
    #print(rank, value * 100, key, sep = '\t')
    print('%d\t%5.5f%s\t%s\t' % (rank, value, 'u', key))
    rank = rank + 1
print('\nPress any key to exit ... ...')
input()
exit()
