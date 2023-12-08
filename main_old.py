import pygame as pg
import numpy as np
import os

pg.init()
clock = pg.time.Clock()

WIDTH , HEIGHT = 600 , 600
X, Y = 250 , 0
FPS = 30
BS = 50 #Block Size
MAP = [[BS,BS],[WIDTH-BS,BS],[WIDTH-BS,HEIGHT-2*BS],[BS,HEIGHT-2*BS]]
OVERLAY = [[BS,BS],[WIDTH-BS,BS],[WIDTH-BS,HEIGHT-2*BS],[BS,HEIGHT-2*BS],[BS,HEIGHT],[0,HEIGHT],[0,0],[HEIGHT,0],[HEIGHT,HEIGHT],[BS,HEIGHT]]

PATH = [[250,50],[250,300],[350,300],[350,400],[100,400],[100,200],[150,200],[150,0],['end','end']]
SUPP_PATH = []
DIR = []  

class enemy(object):
    def __init__(self,type):
        if type == 1:
            self.speed = 1
            self.health = 100
            self.spr = 'Enemy1.png'
        if type == 2:
            self.speed = 7
            self.health = 200
            self.spr = 'Enemy2.png'
        self.pos = np.array([X,Y])
        self.val = 0
        self.sprite = pg.transform.scale(pg.image.load(os.path.join('Images',self.spr)),(BS,BS))

    def move(self):
        run = True
        d = DIR[self.val]
        self.pos += d*self.speed

        if sum(d) > 0 and (sum(d*self.pos) - sum(PATH[self.val+1]*d)) >= 0:
            self.val +=1
            self.pos = PATH[self.val]
            if self.val >= len(DIR):
                run = False
        elif sum(d) < 0 and (sum(d*self.pos) - sum(PATH[self.val+1]*d)) >= 0:
            self.val +=1
            self.pos = PATH[self.val]
            if self.val >= len(DIR):
                run = False
        
        return run


for i in range(len(PATH)-2):
    a1 = PATH[i]
    a2 = PATH[i+1]
    if a1[1] < a2[1]:
        a3 = [a1[0]+BS,a1[1]]
        a4 = [a2[0]+BS,a2[1]]
        SUPP_PATH.append([a1,a2,a4,a3])
        DIR.append(np.array([0,1]))
    elif a1[0] < a2[0]:
        a3 = [a1[0],a1[1]+BS]
        a4 = [a2[0],a2[1]+BS]
        SUPP_PATH.append([a1,a2,a4,a3])
        DIR.append(np.array([1,0]))
    if a1[1] > a2[1]:
        a1 = [a1[0],a1[1]+BS]
        a3 = [a1[0]+BS,a1[1]]
        a4 = [a2[0]+BS,a2[1]]
        SUPP_PATH.append([a1,a2,a4,a3])
        DIR.append(np.array([0,-1]))
    elif a1[0] > a2[0]:
        a1 = [a1[0]+BS,a1[1]]
        a3 = [a1[0],a1[1]+BS]
        a4 = [a2[0],a2[1]+BS]
        SUPP_PATH.append([a1,a2,a4,a3])
        DIR.append(np.array([-1,0]))

screen = pg.display.set_mode((WIDTH,HEIGHT))

def draw_window(time):
   
    pg.draw.polygon(screen, (50,150,50), MAP)
    for i in range(len(SUPP_PATH)):
        polygon_points = SUPP_PATH[i]
        pg.draw.polygon(screen, [255,0,0], polygon_points)
    screen.blit(Enemy1.sprite,Enemy1.pos)
    screen.blit(Enemy2.sprite,Enemy2.pos)
    pg.draw.polygon(screen, [0,0,255], OVERLAY)
    pg.display.update()


Enemy_list = []
    
time = 0
run = True
while run:

    clock.tick(50)
    time += 1
    if time == 1:
        Enemy1 = enemy(1)
        Enemy2 = enemy(2)
    

    

    
    run = Enemy1.move()   
    run = Enemy2.move()   

        
    draw_window(time)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
        
        

