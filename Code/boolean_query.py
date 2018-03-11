# -*- coding: utf-8 -*-

import numpy as np
import nltk
import collections
import os
import sys
import re
from nltk.corpus import stopwords
import simplejson as json

def notFunction(right_operand, current):
    #If right_list is empty the it returns the same result
    if (not right_operand):
        return current
    
    result = []
    result= [token for token in current if token not in right_operand]#Returns the difference 
    return result


def orFunction(right_operand,left_operand):
    result=[]
    result=list(set(right_operand) | set(left_operand))#Returns the section
    return result

def andFunction(right_operand,left_operand):
    result=[]
    result=list(set(right_operand) & set(left_operand))#Returns the union
    return result


def process_query(query,dictionary,listOfDocs,DIR):
    stemmer = nltk.stem.porter.PorterStemmer() #Instantiates stemmer
    nltk.download('stopwords', quiet=True)#Downloads the stopwords
    stopword = set(stopwords.words('english'))
    #Prepares query list
    query = query.replace('(', '( ')
    query = query.replace(')', ' )')
    query = query.split(' ')

    results_stack = []
    postfix_queue = collections.deque(shunting_yard(query)) #Get query in postfix notation as a queue

    while postfix_queue:
        
        token = postfix_queue.popleft()
        result = [] #The final result at each stage
        #If token is a term then add it's appearance list to result
        if (token != 'AND' and token != 'OR' and token != 'NOT'):
            token = stemmer.stem(token.lower()) #Stems the token
            token=re.sub('\W|\d|_', '', token)
            if ((token!='') and (token not in stopword) and (token in dictionary)):
                insertTuples=index[token] 
                for (i,j) in insertTuples:
                        result.append(i)#Adds the documents in which the term appaears, in the result   
        #Else if AND operator
        elif (token == 'AND'):
            #Gets the results of the terms at the right and left of the operator
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            result = andFunction(left_operand, right_operand)  

        #Else if OR operator
        elif (token == 'OR'):
            #Gets the results of the terms at the right and left of the operator
            right_operand = results_stack.pop()
            left_operand = results_stack.pop()
            result = orFunction(left_operand, right_operand)

        #Else if NOT operator
        elif (token == 'NOT'):
            right_operand=results_stack.pop()#Gets the result of the term at the right of the operator
            if(results_stack):
                current= results_stack.pop()#Gets current result
            else:
                current=listOfDocs#If there isn't any previous result sets as result all of the documents

            result =notFunction(right_operand, current) 
            
        #Push result back to stack
        results_stack.append(result)

    #At the end the stack should only have one result which is the final
    if len(results_stack) != 1: print ("ERROR: results_stack. Please check valid query") # check for errors
    
    output=results_stack.pop()#Gets result
    path = DIR+'uploads/'
    prefixed=[]
    for i in output:
        id=str(i)+"_id"
        prefixed.append([filename for filename in os.listdir(path) if filename.startswith(id)])#Add the name of the documents that were in the result, in a list
    
    return prefixed


#Function to manage boolean query and organize it into a queue
def shunting_yard(infix_tokens):
    #Define precedences
    precedence = {}
    precedence['NOT'] = 3
    precedence['AND'] = 2
    precedence['OR'] = 1
    precedence['('] = 0
    precedence[')'] = 0    

    output = []
    operator_stack = []

    #While there are tokens to be read
    for token in infix_tokens:
        
        #If left bracket
        if (token == '('):
            operator_stack.append(token)
        
        #If right bracket, pops all operators from operator stack onto output until a left bracket
        elif (token == ')'):
            operator = operator_stack.pop()
            while operator != '(':
                output.append(operator)
                operator = operator_stack.pop()
        
        #If operator, pops operators from operator stack to queue if they are of higher precedence
        elif (token in precedence):
            #If operator stack is not empty
            if (operator_stack):
                current_operator = operator_stack[-1]
                while (operator_stack and precedence[current_operator] > precedence[token]):
                    output.append(operator_stack.pop())
                    if (operator_stack):
                        current_operator = operator_stack[-1]

            operator_stack.append(token) #Adds token to stack
        
        #Else if operands, adds to output list
        else:
            output.append(token.lower())

    #While there are still operators on the stack, pops them into the queue
    while (operator_stack):
        output.append(operator_stack.pop())
    return output


#When pagerank is selected
def orderByPageRank(result,path):
    pagerankIndex=np.load(DIR+'pagerank.npy').item()#Loads pagerank results
    newResult=[]
    newResultRanks=[]
    for i in result:
        if 'URL' in str(i):#Gets only the files that were crawled
            id=int(i[0].split("_")[0])#Gets document id
            newResult.append(i)
            newResultRanks.append( pagerankIndex[id][0])
    newResult = [x for _,x in sorted(zip(newResultRanks,newResult))]#Sorts results
    return newResult
            
    

 #_____________Start of the Script_______________
DIR=sys.argv[2]#Gets path
pageRank=int(sys.argv[3])#Gets 1 if pagerank was selected or 0 otherwise
#Creates list of all the ids of the documents
listOfDocs=[]

#for python2:
#path, dirs, files = os.walk(DIR+"uploads/").next()
#for python3:
path, dirs, files = os.walk(DIR+"uploads/").__next__()

#for python2:
#for i in xrange(len(files)):
#for python3:
for i in range(len(files)):
    listOfDocs.append(i)#listofDocs contains the ids of all the documents

#Loads index
index = np.load(DIR+'index.npy').item()
query=sys.argv[1]#Gets query

result=process_query(query,index,listOfDocs,DIR)#Finds result
if(pageRank==1):#If pagerank was selected
    result=orderByPageRank(result,DIR+'uploads/')

#Returns result
dict = {'list':result}
print (json.dumps(dict))

