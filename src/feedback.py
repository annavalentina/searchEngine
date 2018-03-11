# -*- coding: utf-8 -*-
import json
import sys
import base64
import math
import re
import nltk
from nltk.corpus import stopwords


def relevanceFeedback(relevantFiles,k,DIR):
    N=int(math.ceil((20 * k) / 100.0)) #Gets 20% of the pages
    words = {}#Dictionary of the frequency of each word
    nltk.download('stopwords', quiet=True)#Downloads the stopwords
    stopword = set(stopwords.words('english'))
    stemmer = nltk.stem.porter.PorterStemmer() #Instantiates stemmer
    for i in relevantFiles:
        #Opens file
        filename=DIR+"uploads/"+str(i[0])
        f = open(filename, "r")
        for line in f:
            for word in line.split():
                word=re.sub('\W|\d|_', '', word)#Removes symbols from the topic name
                word = word.lower()
                wordStem = stemmer.stem(word) #Stems the token
                if( (word!='')and (wordStem not in stopword)):
                    if (word in words):
                        words[word]+=1
                    else:
                        words[word]=1
    N=int(math.ceil((10 * len(words)) / 100.0))#Gets 10% of the words (most frequent)                  
    top_words =sorted(words,key=words.get,reverse=True)[:N]#Returns N words
    return top_words



#_____________Start of the Script_______________
DIR=sys.argv[3]#Gets path
relevantFiles = json.loads(base64.b64decode(sys.argv[1]).decode('utf-8'))#Gets result of the previous serach
type_of_search=int(sys.argv[2])#Gets type of search(1 for vector-0for boolean)

if(type_of_search==0):#If the search is type vector
    k=int(sys.argv[4])#Gets number of results the user asked for
    query=sys.argv[5]#Gets query
else:#If the search is type boolean
    k=len(relevantFiles)#Sets k as the number of the results

pyDIR = sys.argv[6]#Gets python directory
pageRank=int(sys.argv[7])#Gets 1 if pagerank was selected or 0 otherwise
        

top_words=relevanceFeedback(relevantFiles,k,DIR)#Gets top words from the results
result=[]

if(type_of_search==0):#If the search is type vector
   for j,word in enumerate(top_words):
       query=query+" "+word#Add words to query
   import subprocess
   proc = subprocess.Popen([pyDIR, DIR+'query.py', '"'+query+'"', str(k), DIR, str(pageRank)], stdout=subprocess.PIPE,stderr=subprocess.STDOUT)#Calls the search script with the new query as input
   result=proc.communicate()[0]
   r = json.loads(result.decode('utf-8'))
   print (json.dumps(r))#Returns result
else:#If the search is type boolean
    for j,i in enumerate(top_words):
        s=[]
        s.append(i)
        result.append(s)#Returns a list with words that the user may want to add to his query
    dict = {'list': result}
    print (json.dumps(dict))