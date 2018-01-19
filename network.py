# -*- coding: utf-8 -*-
#!/usr/bin/python
#with open('reversi.py') as source_file:
#    exec(source_file.read())

import reversi
import numpy as np
from collections import namedtuple

from random import choice

def nonlin(x,deriv=False):
    if deriv==True:
        return x*(1-x)
    return 1/(1+np.exp(-x))
    
def readOutput(tabIn,tabOut,tour):
    """convertit la table de sortie en liste de positions possibles avec leur probabilité"""
    listPos=coupPossible(tabIn,tour)
    probas=[]
    for i in range(len(listPos)):
        probas.append((listPos[i],tabOut[listPos[i]]))
    return probas

def pickBestMove(probas):
    """retourne la position avec la meilleur proba"""
    best=-1
    for i in probas:
        if i[1]>best:
            pos=i[0]
    return pos

def pickRandomMove(probas):
    """retourne une position aléatoire pondérée par les probas de la table de sortie"""
    while(True):
        for i in probas:
            if i[1]>2*np.random.random((1))-1:
                return i[0]
    


syn0=2*np.random.random((8,8))-1
syn1=2*np.random.random((8,8))-1
syn2=2*np.random.random((8,8))-1


def RandomTraining(N,portee):
    """l'IA joue contre un adversaire jouant des coups aléatoires"""
    global syn0,syn1,syn2
    winrate=0
    np.random.seed(1)
    for i in range(N):
        tab=setupTab()
        couleur=np.random.choice([-1,1])
        tour=1
        coupsJoues=[]
        nbTours=1
        nbToursJoues=0
        skip=0
        while( skip<2 ):
            l0=couleur*tab
            l1 = nonlin(np.dot(l0,syn0))
            l2 = nonlin(np.dot(l1,syn1))
            l3 = nonlin(np.dot(l2,syn2))
            if (coupPossible(tab,tour)==[]):
                skip+=1
            else:
                skip=0
            if (couleur==tour and skip==0):
                probas=readOutput(tab,l3,tour)
                coup=pickBestMove(probas)
                nbToursJoues+=1
                coupsJoues.append((coup,tab,nbToursJoues))
                tab=nextTable(coup,tab,tour)
            if (couleur==-tour and skip==0):
                coup=choice(coupPossible(tab,tour))
                tab=nextTable(coup,tab,tour)
                
            if( len(coupsJoues) > portee ):
                pos=coupsJoues[0][0]
                l0=couleur*coupsJoues[0][1]
                l1 = nonlin(np.dot(l0,syn0))
                l2 = nonlin(np.dot(l1,syn1))
                l3 = nonlin(np.dot(l2,syn2))
                if( diffPoints(coupsJoues[portee][1],couleur) > diffPoints(coupsJoues[0][1],couleur) ):
                    y=np.zeros((8,8))
                    y[pos.i,pos.j]=1
                else:
                    y=np.zeros((8,8))+1
                    y[pos.i,pos.j]=0
                    y=y/np.linalg.norm(y)
                l3_error = y - l3
                l3_delta = l3_error*nonlin(l3,deriv=True)
                l2_error = l3_delta.dot(syn2)
                l2_delta = l2_error*nonlin(l2,deriv=True)
                l1_error = l2_delta.dot(syn1)
                l1_delta = l1_error * nonlin(l1,deriv=True)
                syn2 += l2.T.dot(l3_delta)
                syn1 += l1.T.dot(l2_delta)
                syn0 += l0.T.dot(l1_delta)
                np.delete(coupsJoues,coupsJoues[0][2],0)
                    
                
            tour*=-1
            nbTours+=1
        if( i%int(N/10)==0 and i>0 ):
            print(100*winrate/(N/10),"% de victoire")
            winrate=0
        else:
            if diffPoints(tab,couleur)>0:
                winrate+=1

def SelfTraining(N):
    """l'IA joue contre elle-même"""
    global syn0,syn1,syn2
    np.random.seed(1)
    for i in range(N):
        tab=setupTab()
        tour=1
        coupsJoues1=[]
        coupsJoues2=[]
        nbTours=1
        skip=0
        while( skip<2 ):
            l0=tour*tab
            l1 = nonlin(np.dot(l0,syn0))
            l2 = nonlin(np.dot(l1,syn1))
            l3 = nonlin(np.dot(l2,syn2))
            if (coupPossible(tab,tour)==[]):
                skip+=1
            else:
                skip=0
            if skip==0:
                probas=readOutput(tab,l3,tour)
                coup=pickRandomMove(probas)
                tab=nextTable(coup,tab,tour)
            if (tour==1 and skip==0):
                coupsJoues1.append((coup,tab))
                
            if (tour==-1 and skip==0):
                coupsJoues2.append((coup,-tab))
                    
            tour*=-1
            nbTours+=1

        for c in coupsJoues1:
            pos=c[0]
            y=np.zeros((8,8))+int((np.sign(diffPoints(tab,1))<=0))
            y[pos.i,pos.j]=int(np.sign(diffPoints(tab,1))>0)
            y=y/np.linalg.norm(y)
            l0=c[1]
            l1 = nonlin(np.dot(l0,syn0))
            l2 = nonlin(np.dot(l1,syn1))
            l3 = nonlin(np.dot(l2,syn2))
            l3_error = y - l3
            l3_delta = l3_error*nonlin(l3,deriv=True)
            l2_error = l3_delta.dot(syn2)
            l2_delta = l2_error*nonlin(l2,deriv=True)
            l1_error = l2_delta.dot(syn1)
            l1_delta = l1_error * nonlin(l1,deriv=True)
            syn2 += l2.T.dot(l3_delta)
            syn1 += l1.T.dot(l2_delta)
            syn0 += l0.T.dot(l1_delta)
        for c in coupsJoues2:
            pos=c[0]
            y=np.zeros((8,8))+int((np.sign(diffPoints(tab,-1))<=0))
            y[pos.i,pos.j]=int(np.sign(diffPoints(tab,-1))>0)
            y=y/np.linalg.norm(y)
            l0=c[1]
            l1 = nonlin(np.dot(l0,syn0))
            l2 = nonlin(np.dot(l1,syn1))
            l3 = nonlin(np.dot(l2,syn2))
            l3_error = y - l3
            l3_delta = l3_error*nonlin(l3,deriv=True)
            l2_error = l3_delta.dot(syn2)
            l2_delta = l2_error*nonlin(l2,deriv=True)
            l1_error = l2_delta.dot(syn1)
            l1_delta = l1_error * nonlin(l1,deriv=True)
            syn2 += l2.T.dot(l3_delta)
            syn1 += l1.T.dot(l2_delta)
            syn0 += l0.T.dot(l1_delta)
                
#RandomTraining(5000,3)
#SelfTraining(20000)
#np.savez("syn.npz",syn0,syn1,syn2)
