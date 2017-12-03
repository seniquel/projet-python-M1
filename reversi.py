# -*- coding: utf-8 -*-
import numpy as np
from collections import namedtuple

Pos=namedtuple("Pos","i,j") #i=ligne j=colonne par convention sur les matrices

def setupTab():
    tab=np.zeros((8,8))
    tab[3][3]=1 #1=noir, -1=blanc  (noir commence)
    tab[4][4]=1
    tab[3][4]=-1
    tab[4][3]=-1
    return tab
#def checkMove(pos,tab,tour):
#    """vérifie si jouer sur la position x,y complètera une ligne"""
#    #pos=Pos(x=pos[0],y=pos[1])
#    if pos.j==0 or pos.j==1 or pos.j==7 or pos.j==6:
#        return False
#    if pos.i==0 or pos.i==1 or pos.i==7 or pos.i==6:
#        return False
#    if tab[pos.i,pos.j] == 0:
#       
   
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
        for i in tab[pos.i-2,pos.j::-1]:
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
      for i in tab[pos.i+2,pos.j:]:
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
            if i==tour:
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
        jj=range(pos.i+1,8)
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
    return checkHaut(pos,tab,tour) or checkBas(pos,tab,tour) or \
    checkGauche(pos,tab,tour) or checkDroite(pos,tab,tour) or \
    checkDiagHG(pos,tab,tour) or checkDiagBG(pos,tab,tour) or \
    checkDiagHD(pos,tab,tour) or checkDiagBD(pos,tab,tour)
def coupPossible(tab,tour):
    coups=[]
    for i1 in range(8):
        for j1 in range(8):
            pos=Pos(i=i1,j=j1)
            if checkAll(pos,tab,tour):
                coups=np.append(coups,pos,0)
    return coups
