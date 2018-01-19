# -*- coding: utf-8 -*-
#with open('reversi.py') as source_file:
#    exec(source_file.read())
#
#with open('network.py') as source_file:
#    exec(source_file.read())
import reversi,network
import pygame
from pygame.locals import *
pygame.init()

data = np.load('syn.npz')
syn0 = data["arr_0"]
syn1 = data["arr_1"]
syn2 = data["arr_2"]

noir = (0, 0, 0)
blanc = (255, 255, 255)
vert = (0, 150, 0)
vert_clair = (50,200,50)
gris = (50,50,50)

taille = 100
marge = 2

tailleFenetre = (8*taille + 9*marge, 8*taille + 9*marge)
fenetre = pygame.display.set_mode(tailleFenetre)
pygame.display.set_caption("Reversi")

done=False
clock = pygame.time.Clock()

couleurJoueur = np.random.choice([-1,1])
tab = setupTab()
tour=1
skip=0

def drawTab(couleur,tour):
    fenetre.fill(gris)
    for i in range(8):
        for j in range(8):
            color = vert
            if tab[i][j] == 1:
                color = noir
            elif tab[i][j] == -1:
                color = blanc
            elif Pos(i=i,j=j) in coupPossible(tab,couleurJoueur) and couleur == tour:
                color=vert_clair
            pygame.draw.rect(fenetre,
                             color,
                             [(marge + taille) * j + marge,
                              (marge + taille) * i + marge,
                              taille,
                              taille])
    pygame.display.flip()

while not done:
    clock.tick(60)
    pygame.event.clear()
    while( skip<2 ):
        drawTab(couleurJoueur,tour)
        if (coupPossible(tab,tour)==[]):
            skip+=1
        else:
            skip=0
        if (couleurJoueur==tour and skip==0):
            clicked=False
            while not clicked:
                event = pygame.event.wait()
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // (taille + marge)
                    lig = pos[1] // (taille + marge)
                    coup = Pos(i=lig,j=col)
                    if coup in coupPossible(tab,tour):
                        tab=nextTable(coup,tab,tour)
                        drawTab(couleurJoueur,tour)
                        clicked= True
                    print("Clic ", pos, "Coordonnées: ", lig, col)
        if (couleurJoueur==-tour and skip==0):
            pygame.time.wait(1000)
            l0=-couleurJoueur*tab
            l1 = nonlin(np.dot(l0,syn0))
            l2 = nonlin(np.dot(l1,syn1))
            l3 = nonlin(np.dot(l2,syn2))
            probas=readOutput(tab,l3,tour)
            coup=pickBestMove(probas)
            tab=nextTable(coup,tab,tour)
            drawTab(couleurJoueur,tour)
        tour*=-1
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        done = True

print("Vos points :",calcPoints(tab,couleurJoueur)," Points de l'adversaire :",calcPoints(tab,-couleurJoueur))
pygame.quit()

