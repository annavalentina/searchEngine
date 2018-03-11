# -*- coding: utf-8 -*-
import os
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from collections import defaultdict
import numpy as np
import sys


def create_index (word,id,index):
       
    insertTuples=index[word]#Gets index entry of the word    
    existsInTuples=[item for item in insertTuples if item[0]==id]#Gets tuple (doc_id,frequency) from the previous list
    
    if(not existsInTuples):#If the word wasn't found in this document before
        insertTup=(id,1)
        index[word].append(insertTup)#Appends it to index
    else:       
         num= existsInTuples[0][1]+1#Increases the frequency
         insertTup=(id,num)        
         insertTuples =[item for item in insertTuples if item[0]!=id]#Gets all the other tuples from the word's list
         index[word]=insertTuples
         index[word].append(insertTup)#Appends new tuple to index

    return index


 #_____________Start of the Script_______________
DIR=sys.argv[1]#Gets path
path = DIR+'uploads/'

index = defaultdict(list)#Index of files
numberOfFiles=0

nltk.download('stopwords', quiet=True)#Downloads the stopwords
stopwords = set(stopwords.words('english'))
ps = PorterStemmer()
Ld=[]#Lengths of documents

files=sorted(os.listdir(path), key=lambda a: int(a.split("_")[0]) )#Gets files from path in sorted order
for filename in files:
    terms=0
    f= open(path+filename, "r")#Opens file
    for line in f:#For each line
        for word in line.split():#For each word
            terms+=1
            word=re.sub('\W|\d|_', '', word)#Removes symbols from the word
            word = ps.stem(word.lower())
            if ((word!='') and (word not in stopwords)):
                create_index(word,numberOfFiles,index)#Adds word to index
    f.close()
    Ld.append(terms)#Adds length of docum
    numberOfFiles+=1#Holds the id of the file
print (index)
np.save('index.npy', index)
np.save('ld.npy',Ld)


