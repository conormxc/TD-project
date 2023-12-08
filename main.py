import pygame as pg
from pygame.locals import NOFRAME
import numpy as np
import os
import math



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

    def move(self,r):
        
        d = DIR[self.val]
        self.pos += d*self.speed

        if sum(d) > 0 and (sum(d*self.pos) - sum(PATH[self.val+1]*d)) >= 0:
            self.val +=1
            self.pos = PATH[self.val]
            if self.val >= len(DIR):
                r = False
        elif sum(d) < 0 and (sum(d*self.pos) - sum(PATH[self.val+1]*d)) >= 0:
            self.val +=1
            self.pos = PATH[self.val]
            if self.val >= len(DIR):
                r = False
        
        return r

class tower(object):
    def __init__(self,type,pos):
        self.basic_hit = False
        self.bomb_hit = False
        self.radial_hit = False
        if type == 1:
            self.basic_hit = True
            self.fire_period = 10
            self.spr = 'Sniper.png'
            self.cost = 100
            self.range = 125
        if type == 2:
            self.bomb_hit = True
            self.fire_period = 10
            self.spr = 'Rocket.png'
            self.cost = 300
            self.range = 200
        if type == 3:
            self.radial_hit = True
            self.fire_period = 10
            self.spr = 'Gun.png'
            self.cost = 500
            self.range = 75
        self.pos = pos
        self.sprite = pg.transform.scale(pg.image.load(os.path.join('Images',self.spr)),(BS,BS))

    

def Pick_tower(event,Tower_locs,money,Select):
    
    tower_type = 0
    for j in range(len(Tower_locs)):
        i = Tower_locs[j]
        if (event.pos[0] > i[0] and event.pos[0] < i[0]+50) and (event.pos[1] > i[1] and event.pos[1] < i[1]+50) and (money-tower(j+1,[200,200]).cost >= 0):
            Select = True
            tower_type = j+1
    
    return Select, tower_type

def Place_tower(event,Select,money):

    if (event.pos[0] > BS and event.pos[0] < WIDTH-BS) and (event.pos[1] > BS and event.pos[1] < HEIGHT - 2*BS):
        Select = False
        pos_in_path = False
        for i in path_rects:
            if i.collidepoint(event.pos):
                pos_in_path = True
        if pos_in_path == False:
            point = round_down(event.pos)
            Tower_list.append([tower(tower_type,point),pg.Rect(point[0],point[1],BS,BS)])
            money -= Tower_list[-1][0].cost
            path_rects.append(pg.Rect(point[0],point[1],BS,BS))
    
    return Select, money


def draw_grid():
    
    for x in range(0, WIDTH, BS):
        for y in range(0, HEIGHT, BS):
            rect = pg.Rect(x, y, BS, BS)
            pg.draw.rect(screen, [255,255,255], rect, 1)

def rect_from_points(points):
    
    point1, point2, point3, point4 = points

    min_x = min(point1[0], point2[0], point3[0], point4[0])
    min_y = min(point1[1], point2[1], point3[1], point4[1])
    width = max(point1[0], point2[0], point3[0], point4[0]) - min_x
    height = max(point1[1], point2[1], point3[1], point4[1]) - min_y

    return pg.Rect(min_x, min_y, width, height)

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

def check_radius(event):
    if len(Tower_list) >= 0:
        for i in range(len(Tower_list)):
            if Tower_list[i][1].collidepoint(event.pos):
                print('yahoo')
                return True,i
        return False,0


def round_down(numbers):
    return [math.floor(num / BS) * BS for num in numbers]



path_rects = []

for i in range(len(PATH)-2):             # Turns the points from PATH into the desired path
    a1 = PATH[i]
    a2 = PATH[i+1]
    if a1[1] < a2[1]:
        a3 = [a1[0]+BS,a1[1]]
        a4 = [a2[0]+BS,a2[1]]
        DIR.append(np.array([0,1]))
    elif a1[0] < a2[0]:
        a3 = [a1[0],a1[1]+BS]
        a4 = [a2[0],a2[1]+BS]
        DIR.append(np.array([1,0]))
    elif a1[1] > a2[1]:
        a1 = [a1[0],a1[1]+BS]
        a3 = [a1[0]+BS,a1[1]]
        a4 = [a2[0]+BS,a2[1]]
        DIR.append(np.array([0,-1]))
    elif a1[0] > a2[0]:
        a1 = [a1[0]+BS,a1[1]]
        a3 = [a1[0],a1[1]+BS]
        a4 = [a2[0],a2[1]+BS]
        DIR.append(np.array([-1,0]))
        
    SUPP_PATH.append([a1,a2,a4,a3])
    path_rects.append(rect_from_points([a1,a2,a4,a3]))

screen = pg.display.set_mode((WIDTH,HEIGHT))
#pg.display.set_mode((1, 1), NOFRAME)

def draw_window(time,E_list,Select,T_list,t_ind):
   
    pg.draw.polygon(screen, (50,150,50), MAP)
    for i in range(len(SUPP_PATH)):
        polygon_points = SUPP_PATH[i]
        pg.draw.polygon(screen, [255,0,0], polygon_points)
    for i in E_list:
        screen.blit(i.sprite,i.pos)
    if len(T_list) > 0:
        for i in T_list:
            i = i[0]
            screen.blit(i.sprite,i.pos)
    if Select == True:
        draw_grid()
    if check_rad == True:
        centre = T_list[t_ind][0].pos
        draw_circle_alpha(screen, [200,200,200,100], [centre[0]+BS/2,centre[1]+BS/2], T_list[t_ind][0].range)
    pg.draw.polygon(screen, [0,0,255], OVERLAY)
    for j in range(len(Tower_locs)):
        i = Tower_locs[j]
        screen.blit(pg.transform.scale(pg.image.load(os.path.join('Images',tower(j+1,[200,200]).spr)),(BS,BS)),i)
    pg.display.update()








Tower_locs = []
for i in range(1,4):
    Tower_locs.append((i*2*BS,HEIGHT-2*BS))

Enemy_list = []
Tower_list = []
file_path = 'Enemy_info.txt'
Enemy_info = np.int32(np.loadtxt(file_path, delimiter=','))
Enemy_num = 0

time = 0
run = True
Select = False
check_rad = False
tower_ind = False
money = 1000

while run:

    clock.tick(50)
    time += 1
    
    if time == Enemy_info[Enemy_num,0]:
        Enemy_list.append(enemy(Enemy_info[Enemy_num,1]))
        Enemy_num += 1
    
    for i in Enemy_list:
        run = i.move(run)  

        
    draw_window(time,Enemy_list,Select,Tower_list,tower_ind)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            check_rad = False
            if Select == False:
                Select, tower_type = Pick_tower(event,Tower_locs,money,Select)
                check_rad, tower_ind = check_radius(event)
            
            elif Select == True:
                Select, money = Place_tower(event,Select,money)
                Select = False
            
                




                        
                
                
        
        

