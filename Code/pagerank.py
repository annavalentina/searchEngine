import numpy as np
from scipy.sparse import csc_matrix
import sys
from collections import defaultdict
import os

def pageRank(G, d = .85, maxerr = .0001,iterations=100):
    n = G.shape[0]

    A = csc_matrix(G,dtype=np.float)#get the pairs (siteA,siteA points to)
    rsums = np.array(A.sum(1))[:,0]#how many sites does a site point to (each row)

    ri, ci = A.nonzero()#get from A ri=[siteA, siteB,....] and ci=[siteA points to, siteB points to,....]

    ro, pr = np.zeros(n), np.ones(n)#make two matrices of length n (one with ones and another  one with zeros)
    j=0
    #while it wont have a big difference through each iteration
    while (np.sum(np.abs(pr-ro)) > maxerr)and(j<iterations):
        #to compute the error
        ro = pr.copy()
        # PR(A) = (1-d) + d (PR(T1)/C(T1) + ... + PR(Tn)/C(Tn))
        #for python3
        for i in range(0, n):
        #for python2.7
        #for i in xrange(0,n):
            sum=0
            counter=0
            for c in ci:
                if(c==i):
                    sum=sum+pr[ri[counter]]/rsums[ri[counter]]
                counter=counter+1
            pr[i]=(1-d)+d*sum
            j=j+1
    # return normalized pagerank
    s=0
    for i in pr:
        s=s+i
    # for python3
    for i in range(0, n):
    # for python2.7
    #for i in xrange(0, n):
        pr[i]=pr[i]/s
    return pr

def makeGraph(path):
    #make the graph
    urlSet = np.load(path + 'crawlSet.npy').item()
    urlList=[]
    for i in urlSet:
        urlList.append(i)
    g=np.zeros((len(urlList),len(urlList)), dtype=np.int)
    d = np.load(path + 'crawlURLrelations.npy').item()
    links=d["links"]
    for i in links:
        url=i["url"]
        x=0
        for l in urlList:
            if(l==url):
                break;
            x=x+1
        #if a link has no children OR if it was in the final depth of crawling it will automaticly be all 0
        #wont lose time iterating because i["children"] is empty
        for child in i["children"]:
            y=0
            for k in urlList:
                if (k == child):
                    break;
                y = y + 1
            g[x,y]=1
    return g,urlList


def create_index(urlList,p,url,id, index):
    #find id for url
    i=0
    s=0
    for u in urlList:
        if(u==url):
            s=i
            break;
        i=i+1
    index[id].append(p[s])
    return index;


if __name__=='__main__':
    path = sys.argv[1]
    G,urlList=makeGraph(path)
    p=pageRank(G,d=.85,iterations=100)

    index = defaultdict(list)
    files = sorted(os.listdir(path+"uploads/"), key=lambda a: int(a.split("_")[0]))
    numberOfFiles=0
    for filename in files:
        if "_idURL" in filename:
            f = open(path+"uploads/" + filename, "r")
            url=f.readline()
            index=create_index(urlList, p,url,numberOfFiles, index)
            f.close()
        numberOfFiles += 1

    print (index)
    np.save('pagerank.npy', index)

    
