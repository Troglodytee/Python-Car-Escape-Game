import pygame
from pygame.locals import *
from math import cos,sin,atan,radians,degrees,sqrt
from random import randint
import sys
import time

def affich() :
    pygame.time.Clock().tick(40)
    if ecran == 1 :
        pygame.draw.rect(fenetre,(0,0,0),(0,0,600,600))
        texte = myfont3.render("ESCAPE",False,(255,0,0))
        fenetre.blit(texte,(300-texte.get_width()/2,290-texte.get_height()))
        texte = myfont2.render("> Push return",False,(255,255,255))
        fenetre.blit(texte,(300-texte.get_width()/2,310))
    elif ecran in [2,3] :
        pygame.draw.rect(fenetre,(80,170,40),(0,0,600,600))
        for i in l_obstacles :
            if abs(i[0]-x) < 400 and abs(i[1]-y) < 400 : pygame.draw.rect(fenetre,(127,127,127),(300+(i[0]-x),300+(i[1]-y),50,50))
        for i in l_ennemis :
            if abs(i[1]-x) < 400 and abs(i[2]-y) < 400 :
                if i[0] == 0 : v = pygame.transform.rotate(police,i[3]-90)
                else : v = pygame.transform.rotate(explosion[i[0]-1],i[3]-90)
                fenetre.blit(v,(300+(i[1]-x)-v.get_width()/2,300+(i[2]-y)-v.get_height()/2))
        if etat == 0 : v = pygame.transform.rotate(voiture,direc-90)
        else : v = pygame.transform.rotate(explosion[etat+2],direc-90)
        fenetre.blit(v,(300-v.get_width()/2,300-v.get_height()/2))
        if ecran == 2 :
            if etat == 0 : texte = myfont.render("Score : "+str(int(time.time()-temps)),False,(255,255,255))
            else : texte = myfont.render("Score : "+str(temps),False,(255,255,255))
            fenetre.blit(texte,(5,5))
        else :
            texte = myfont2.render("GAME OVER",False,(255,0,0))
            fenetre.blit(texte,(300-texte.get_width()/2,290-texte.get_height()))
            texte = myfont2.render("Score : "+str(temps),False,(255,255,255))
            fenetre.blit(texte,(300-texte.get_width()/2,310))

    pygame.display.flip()

def mouv() :
    global ecran
    global temps
    global x
    global y
    global etat
    global l_obstacles
    global l_ennemis
    if etat == 0 :
        x += int(cos(radians(direc))*10)
        y += int(-sin(radians(direc))*10)
        for j in l_obstacles :
            if j[0]-14 <= x+int(cos(radians(direc))*25) <= j[0]+64 and j[1] <= y+int(-sin(radians(direc))*25) <= j[1]+50 :
                temps,etat = int(time.time()-temps),1
                break
    elif etat == 3 : ecran,etat = 3,4
    elif etat != 4 : etat += 1

    if ecran in [2,3] :
        if randint(0,1) == 0 :
            b = randint(1,4)
            if b == 1 : xo,yo = randint(x-1000,x+950),y-1000
            elif b == 2 : xo,yo = x+1000,randint(y-1000,y+950)
            elif b == 3 : xo,yo = randint(x-1000,x+950),y+1000
            elif b == 4 : xo,yo = x-1000,randint(y-1000,y+950)
            non = 0
            for i in l_obstacles :
                if i[0] <= xo < i[0]+50 and i[1] <= yo < i[1]+50 or i[0] <= xo+50 < i[0]+50 and i[1] <= yo < i[1]+50 or i[0] <= xo < i[0]+50 and i[1] <= yo+50 < i[1]+50 or i[0] <= xo+50 < i[0]+50 and i[1] <= yo+50 < i[1]+50 :
                    non = 1
                    break
            if non == 0 :
                l_obstacles += [[xo,yo]]
        i = 0
        while i < len(l_obstacles) :
            if l_obstacles[i][0] < x-1000 or l_obstacles[i][0] > x+1000 or l_obstacles[i][1] < y-1000 or l_obstacles[i][1] > y+1000 : del l_obstacles[i]
            else : i += 1

        if randint(0,60) == 0 or len(l_ennemis) == 0 :
            b = randint(1,4)
            if b == 1 : xe,ye = randint(x-1000,x+1000),y-1000
            elif b == 2 : xe,ye = x+1000,randint(y-1000,y+1000)
            elif b == 3 : xe,ye = randint(x-1000,x+1000),y+1000
            elif b == 4 : xe,ye = x-1000,randint(y-1000,y+1000)
            non = 0
            if non == 0 :
                if xe < x and ye > y :
                    if x-xe <= ye-y : d = 1
                    else : d = 0
                elif xe < x and ye < y :
                    if x-xe <= y-ye : d = 3
                    else : d = 0
                elif xe > x and ye > y :
                    if xe-x <= ye-y : d = 1
                    else : d = 2
                elif xe > x and ye < y :
                    if xe-x <= y-ye : d = 3
                    else : d = 2
                l_ennemis += [[0,xe,ye,d*90]]

        for i in l_ennemis :
            if i[0] == 0 :
                dx,dy = abs(x-i[1]),abs(y-i[2])
                if dx != 0 :
                    angle = degrees(atan(dy/dx))
                    if i[1] < x and i[2] < y : angle = 270+90-angle
                    elif i[1] > x and i[2] > y : angle = 180-angle
                    elif i[1] > x and i[2] < y : angle += 180
                elif x > i[1] : angle = 90
                else : angle = 270
                if i[3] > angle and i[3]-angle < 180 or i[3] < angle and i[3]-(angle-360) < 180 : i[3] -= 3
                else : i[3] += 3
                if i[3] == -3 : i[3] = 357
                elif i[3] == 360 : i[3] = 0
                i[1] += int(cos(radians(i[3]))*10)
                i[2] += int(-sin(radians(i[3]))*10)
                for j in l_obstacles :
                    if j[0]-14 <= i[1]+int(cos(radians(i[3]))*25) <= j[0]+64 and j[1] <= i[2]+int(-sin(radians(i[3]))*25) <= j[1]+50 :
                        i[0] = 1
                        break
                for j in l_ennemis :
                    if j != i and sqrt((i[1]-j[1])**2+(i[2]-j[2])**2) < 25 :
                        i[0] = 1
                        if j[0] == 0 : j[0] = 1
                if sqrt((i[1]-x)**2+(i[2]-y)**2) < 25 :
                    i[0] = 1
                    if etat == 0 : temps,etat = int(time.time()-temps),1
            elif i[0] == 3 : del l_ennemis[l_ennemis.index(i)]
            else : i[0] += 1

        i = 0
        while i < len(l_ennemis) :
            if l_ennemis[i][1] < x-2000 or l_ennemis[i][1] > x+2000 or l_ennemis[i][2] < y-2000 or l_ennemis[i][2] > y+2000 : del l_ennemis[i]
            else : i += 1

    affich()

pygame.init()

raccourci = sys.argv[0][0:-8]+"fichiers\\"

fenetre = pygame.display.set_mode((600,600))
pygame.display.set_caption("Escape")
pygame.display.set_icon(pygame.image.load(raccourci+"sprite\\voiture.png"))

voiture = pygame.image.load(raccourci+"sprite\\voiture.png").convert()
voiture.set_colorkey((255,255,255))
police = pygame.image.load(raccourci+"sprite\\police.png").convert()
police.set_colorkey((255,255,255))
explosion = [pygame.image.load(raccourci+"sprite\\explosion"+str(i+1)+".png").convert() for i in range (7)]
explosion[0].set_colorkey((255,255,255))
explosion[1].set_colorkey((255,255,255))
explosion[2].set_colorkey((255,255,255))
explosion[3].set_colorkey((255,255,255))
explosion[4].set_colorkey((255,255,255))
explosion[5].set_colorkey((255,255,255))
explosion[6].set_colorkey((255,255,255))
myfont,myfont2,myfont3 = pygame.font.Font(raccourci+"font\\Minecraft.ttf",18),pygame.font.Font(raccourci+"font\\Minecraft.ttf",36),pygame.font.Font(raccourci+"font\\Minecraft.ttf",60)

ecran = 1

affich()

pygame.key.set_repeat(50,25)

b = 1
while b == 1 :
    for event in pygame.event.get() :
        if event.type == QUIT :
            b = 0
            pygame.quit()
        elif event.type == KEYDOWN :
            if event.key == K_RETURN :
                if ecran == 1 : ecran,temps,etat,direc,x,y,l_obstacles,l_ennemis = 2,time.time(),0,90,0,0,[],[]
                elif ecran == 3 : ecran = 1
            elif event.key == K_LEFT and ecran == 2 and etat == 0 :
                direc += 5
                if direc == 360 : direc = 0
            elif event.key == K_RIGHT and ecran == 2 and etat == 0 :
                direc -= 5
                if direc == -5 : direc = 355
            elif event.key == K_RETURN :
                if pause == 0 : pause = 1
                else : pause = 0

    if ecran in [2,3] : mouv()