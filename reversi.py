# -*- coding: utf-8 -*-
#!/usr/bin/python
import numpy as np
from collections import namedtuple

Pos=namedtuple("Pos","i,j") #i=ligne j=colonne

def setupTab():
    tab=np.zeros((8,8))
    tab[3][3]=1 #1=noir, -1=blanc  (noir commence)
    tab[4][4]=1
    tab[3][4]=-1
    tab[4][3]=-1
    return tab

def checkGauche(pos,tab,tour):
    count=0
    if pos.j<=1:
        return False
    if tab[pos.i,pos.j-1]==-tour:
        for i in tab[pos.i,pos.j-2::-1]:
            count+=1
            if i==tour:
                return count
            if i==0:
                return False
    return False
def checkDroite(pos,tab,tour):
    count=0
    if pos.j>=6:
        return False
    if tab[pos.i,pos.j+1]==-tour:
        for i in tab[pos.i,pos.j+2:]:
            count+=1
            if i==tour:
                return count
            if i==0:
                return False
    return False
def checkHaut(pos,tab,tour):
    count=0
    if pos.i<=1:
        return False
    if tab[pos.i-1,pos.j]==-tour: #vérifie en haut
        for i in tab[pos.i-2::-1,pos.j]:
            count+=1
            if i==tour:
                return count
            if i==0:
                return False
    return False
def checkBas(pos,tab,tour):
    count=0
    if pos.i>=6:
        return False
    if tab[pos.i+1,pos.j]==-tour: #vérifie en bas
      for i in tab[pos.i+2:,pos.j]:
          count+=1
          if i==tour:
              return count 
          if i==0:
              return False
    return False
def checkDiagHG(pos,tab,tour):
    count=0
    if pos.i<=1 or pos.j<=1:
        return False
    if tab[pos.i-1,pos.j-1]==-tour: #vérifie diagonale en haut à gauche
        ii=range(pos.i-1,-1,-1)
        jj=range(pos.j-1,-1,-1)
        for i,j in zip(ii,jj):
            count+=1
            if tab[i,j]==tour:
                return count
            if tab[i,j]==0:
                return False
    return False
def checkDiagHD(pos,tab,tour):
    count=0
    if pos.i<=1 or pos.j>=6:
        return False
    if tab[pos.i-1,pos.j+1]==-tour: #vérifie diagonale en haut à droite
        ii=range(pos.i-1,-1,-1)
        jj=range(pos.j+1,8)
        for i,j in zip(ii,jj):
            count+=1
            if tab[i,j]==tour:
                return count    
            if tab[i,j]==0:
                return False           
    return False
def checkDiagBG(pos,tab,tour):
    count=0
    if pos.i>=6 or pos.j<=1:
        return False
    if tab[pos.i+1,pos.j-1]==-tour: #vérifie diagonale en bas à gauche
        ii=range(pos.i+1,8)
        jj=range(pos.j-1,-1,-1)
        for i,j in zip(ii,jj):
            count+=1
            if tab[i,j]==tour:
                return count   
            if tab[i,j]==0:
                return False            
    return False
def checkDiagBD(pos,tab,tour):
    count=0
    if pos.i>=6 or pos.j>=6:
        return False
    if tab[pos.i+1,pos.j+1]==-tour: #vérifie diagonale en bas à droite
        ii=range(pos.i+1,8)
        jj=range(pos.j+1,8)
        for i,j in zip(ii,jj):
            count+=1
            if tab[i,j]==tour:
                return count
            if tab[i,j]==0:
                return False
    return False
def checkAll(pos,tab,tour):
    if tab[pos.i,pos.j]==0:
        return checkHaut(pos,tab,tour) or checkBas(pos,tab,tour) or \
        checkGauche(pos,tab,tour) or checkDroite(pos,tab,tour) or \
        checkDiagHG(pos,tab,tour) or checkDiagBG(pos,tab,tour) or \
        checkDiagHD(pos,tab,tour) or checkDiagBD(pos,tab,tour)
    else:
        return False
def coupPossible(tab,tour):
    coups=[]
    for i1 in range(8):
        for j1 in range(8):
            pos=Pos(i=i1,j=j1)
            if checkAll(pos,tab,tour):
                coups.append(pos)
    return coups
def nextTable(pos,tabEntree,tour):
    tab=np.copy(tabEntree)
    tab[pos.i,pos.j]=tour
    for k in range(1,checkGauche(pos,tab,tour)+1):
        tab[pos.i,pos.j-k]*=-1
    for k in range(1,checkDroite(pos,tab,tour)+1):
        tab[pos.i,pos.j+k]*=-1
    for k in range(1,checkHaut(pos,tab,tour)+1):
        tab[pos.i-k,pos.j]*=-1
    for k in range(1,checkBas(pos,tab,tour)+1):
        tab[pos.i+k,pos.j]*=-1
    for k in range(1,checkDiagHG(pos,tab,tour)):
        tab[pos.i-k,pos.j-k]*=-1
    for k in range(1,checkDiagHD(pos,tab,tour)):
        tab[pos.i-k,pos.j+k]*=-1
    for k in range(1,checkDiagBG(pos,tab,tour)):
        tab[pos.i+k,pos.j-k]*=-1
    for k in range(1,checkDiagBD(pos,tab,tour)):
        tab[pos.i+k,pos.j+k]*=-1
    return tab

def calcPoints(tab,tour):
    count=0
    for i in range(8):
        for j in range(8):
            if tab[i,j]==tour:
                count+=1
    return count

def diffPoints(tab,tour):
    return calcPoints(tab,tour) - calcPoints(tab,-tour)