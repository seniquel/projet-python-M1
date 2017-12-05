# -*- coding: utf-8 -*-
with open('reversi.py') as source_file:
    exec(source_file.read())
    
N=10000

def nonlin(x,deriv=False):
    if deriv==True:
        return x*(1-x)
    return 1/(1+np.exp(-x))
    
def readOutput(tabIn,tabOut,tour):
    """convertit la table de sortie en liste de positions possibles avec leur probabilité"""
    listPos=coupPossible(tabIn,tour)
    probas=[]
    for i in range(len(listPos)):
        probas.append((listPos[i],tabIn[listPos[i]]))
    return probas
    
tab=setupTab()

syn0=2*random((8,8))
syn1=2*random((8,8))

for i in range(N)