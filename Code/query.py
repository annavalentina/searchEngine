# -*- coding: utf-8 -*-
#!/usr/bin/python
import numpy as np
from math import log,sqrt
import os
import nltk
from heapq import heappush, heappop, heapreplace
import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import sys
import simplejson as json


def search(query,k,DIR,pagerank):
    ps = PorterStemmer()
    heap=[]#Holds top k results
    index = np.load(DIR+'index.npy').item() #Loads index
    ld=np.load(DIR+'ld.npy')#Loads ld dictionary (length of documents)
    if(pagerank==1):
        pagerankIndex=np.load(DIR+'pagerank.npy').item()#Loads pagerank results

         

    #for python2:
    # path, dirs, files = os.walk(DIR+"uploads/").next()
    #for python3:
    path, dirs, files = os.walk(DIR+"uploads/").__next__()
    
    N=len(files)#Number of files
    S=[None]*N#Accumulators for documents
    for i in range(N):
        S[i]=0.0
    
    Tq=[]#List of words
    query = query.split(' ')
    nltk.download('stopwords', quiet=True)#Downloads the stopwords
    stopword = set(stopwords.words('english'))
    for word in query:
            word=re.sub('\W|\d|_', '', word)#Removes symbols from the topic name
            word = ps.stem(word.lower())#Stemming the word

            if((word!='') and (word not in stopword)):
                if (word in index):
                    Tq.append(word)#Adds word in list

        
    for word in Tq:
            nt=len(index[word])#Number of files that contain the word
            IDFt=log(1+N/nt)#Finds IDF of the word
            insertTuples=index[word] #Gets the list of the word
            for (i,j) in insertTuples: #For each document that contains a word
                TFtd=1+log(j)#Finds the TF
                id=i
                S[id]=S[id]+(TFtd*IDFt)#Calculates new score

   
    for i in range(N):
        if(pagerank==1):#If pagerank was selected
            id=str(i)+"_id"
            if 'URL' not in str([filename for filename in os.listdir(path) if filename.startswith(id)]):#Gets only the files that were crawled
                continue
            
	                   			
        Ld=ld[i]
        Ld=sqrt(Ld)
        S[i]=S[i]/Ld#Finds normalized score of the document

        if(pagerank==1):
            pageR=pagerankIndex[i]#Gets pagerank score
            S[i]=2*((S[i]*pageR[0])/(S[i]+pageR[0]))#Harmonic mean to calculate final score
        
        if(len(heap)<k):#Fills the heap until there are at least k entries
            heappush(heap,(S[i],i))
        else: 
            if(S[i]>heap[0][0]):#If the score is larger than the minimum score in the heap replace it
                heapreplace(heap,(S[i],i))
             

    
    path = DIR+'uploads/'
    prefixed=[]
    
    if(k>len(heap)):
        k=len(heap)#If there aren't k files show as many as were found
    for i in range(k):
        id=str(heappop(heap)[1])+"_id"
        prefixed.append([filename for filename in os.listdir(path) if filename.startswith(id)])#Adds the names of the most similar documents to the result
    
    result=(list(reversed(prefixed)))

    dict = {'list': result}
    print (json.dumps(dict))#Returns result






#_______Start of the Script_________
query=sys.argv[1]#Gets query
k=int(sys.argv[2])#Gets number of results the user asked for
DIR=sys.argv[3]#Gets path
pagerank=int(sys.argv[4])#Gets 1 if pagerank was selected or 0 otherwise

search(query,k,DIR,pagerank)
