import pygame as pg
from pygame.locals import NOFRAME
import numpy as np
import os
import math




pg.init()
clock = pg.time.Clock()

WIDTH , HEIGHT = 700 , 700
X, Y = 150 , 0
FPS = 30
BS = 50 #Block Size
MAP = [[BS,BS],[WIDTH-BS,BS],[WIDTH-BS,HEIGHT-2*BS],[BS,HEIGHT-2*BS]]
OVERLAY = [[BS,BS],[WIDTH-BS,BS],[WIDTH-BS,HEIGHT-2*BS],[BS,HEIGHT-2*BS],[BS,HEIGHT],[0,HEIGHT],[0,0],[HEIGHT,0],[HEIGHT,HEIGHT],[BS,HEIGHT]]

PATH = [[X,Y+50],[150,300],[250,300],[250,150],[550,150],[550,250],[500,250],[500,450],[250,450],[250,600],['end','end']]
SUPP_PATH = []
DIR = []  

pg.font.init() 
my_font = pg.font.SysFont('Comic Sans MS', 20)

Tower_locs = []
for i in range(1,4):
    Tower_locs.append((i*2*BS,HEIGHT-2*BS))

AL1 = 5
AL2 = 10
AL3 = 5
Flame1 = pg.transform.scale(pg.image.load(os.path.join('Images','Flame1.png')),(BS,BS))
Flame2 = pg.transform.scale(pg.image.load(os.path.join('Images','Flame22.png')),(BS,BS))
Flame3 = pg.transform.scale(pg.image.load(os.path.join('Images','Flame3.png')),(BS,BS))
Flame4 = pg.transform.scale(pg.image.load(os.path.join('Images','Flame4.png')),(BS,BS))
Shot = pg.transform.scale(pg.image.load(os.path.join('Images','Shot.png')),(BS,BS))


class enemy(object):
    def __init__(self,type):
        if type == 1:
            self.speed = 2
            self.health = 100
            self.spr = 'Enemy1.png'
            self.money = 5
        if type == 2:
            self.speed = 4
            self.health = 200
            self.spr = 'Enemy2.png'
            self.money = 10
        if type == 3:
            self.speed = 3
            self.health = 500
            self.spr = 'Enemy3.png'
            self.money = 20
        if type == 4:
            self.speed = 1
            self.health = 2000
            self.spr = 'Enemy44.png'
            self.money = 50
        self.pos = np.array([X,Y])
        self.val = 0
        self.sprite = pg.transform.scale(pg.image.load(os.path.join('Images',self.spr)),(BS,BS))
        self.distance = 0

    def move(self,l):
        
        d = DIR[self.val]
        self.pos += d*self.speed
        self.distance += self.speed

        if sum(d) > 0 and (sum(d*self.pos) - sum(PATH[self.val+1]*d)) >= 0:
            self.val +=1
            self.pos = PATH[self.val]
            if self.val >= len(DIR):
                self.health = 0
                self.money = 0
                l -= 1
        elif sum(d) < 0 and (sum(d*self.pos) - sum(PATH[self.val+1]*d)) >= 0:
            self.val +=1
            self.pos = PATH[self.val]
            if self.val >= len(DIR):
                self.health = 0
                self.money = 0
                l -= 1
        
        return l
    
    def check_alive(self):
        
        if self.health <= 0:
            return False
        return True

class tower(object):
    def __init__(self,type,pos):

        self.basic_hit = False
        self.bomb_hit = False
        self.radial_hit = False
        if type == 1:
            self.basic_hit = True
            self.fire_period = 25
            self.spr = 'Sniper.png'
            self.cost = 100
            self.range = 125
            self.damage = 25
        if type == 2:
            self.bomb_hit = True
            self.delay = 25
            self.bomb_range = 50
            self.fire_period = 75
            self.spr = 'Rocket.png'
            self.cost = 500
            self.range = 200
            self.damage = 250
        if type == 3:
            self.radial_hit = True
            self.fire_period = 25
            self.spr = 'Gun.png'
            self.cost = 300
            self.range = 75
            self.damage = 50
        self.pos = pos
        self.sprite = pg.transform.scale(pg.image.load(os.path.join('Images',self.spr)),(BS,BS))
        self.fire_time = self.fire_period

    def shoot(self,E_list,animations):

        target_point = []
        self.fire_time -= 1
        if self.fire_time <= 0:
            if self.basic_hit:
                animations = self.basic_shoot(E_list,animations)
            if self.bomb_hit:
                target_point, animations = self.mortar_shoot(E_list,animations)
            if self.radial_hit:
                animations = self.radial_shoot(E_list,animations)
        
        return target_point, animations

    def basic_shoot(self,E_list,animations):

        target_dist = 0
        target = 0
        for j in E_list:
            dist = np.array(j.pos) - np.array(self.pos)
            magnitude = (dist[0]**2+dist[1]**2)**(1/2)
            if magnitude <= self.range and j.distance >= target_dist:
                target_dist = j.distance
                target = j
        if target:
            target.health -= self.damage
            self.fire_time = self.fire_period
            animations.append([0,target.pos,AL2])
            animations.append([4,self.pos,AL1])
        return animations

            
    def mortar_shoot(self,E_list,animations):

        target_dist = 0
        target = []
        for j in E_list:
            dist = np.array(j.pos) - np.array(self.pos)
            magnitude = (dist[0]**2+dist[1]**2)**(1/2)
            if magnitude <= self.range and j.distance >= target_dist:
                target_dist = j.distance
                target = j.pos
                self.fire_time = self.fire_period
        if any(target):
            animations.append([5,self.pos,AL1])
        return target, animations
    
    def radial_shoot(self,E_list,animations):
        counter = 0
        for j in E_list:
            dist = np.array(j.pos) - np.array(self.pos)
            magnitude = (dist[0]**2+dist[1]**2)**(1/2)
            if magnitude <= self.range:
               j.health -= self.damage
               counter += 1
        if counter > 0:
               pos = np.array(self.pos) + np.array([BS/2,BS/2])
               animations.append([3,pos,AL3])
               self.fire_time = self.fire_period
        return animations

    

    

        

            

        


                

        
    

    

def Pick_tower(event,Tower_locs,money,Select):
    
    tower_type = 0
    for j in range(len(Tower_locs)):
        i = Tower_locs[j]
        if (event.pos[0] > i[0] and event.pos[0] < i[0]+50) and (event.pos[1] > i[1] and event.pos[1] < i[1]+50) and (money-tower(j+1,[200,200]).cost >= 0):
            Select = True
            tower_type = j+1
    
    return Select, tower_type

def Place_tower(event,Select,money,Tower_list,tower_type):

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

def check_radius(event,Tower_list):
    if len(Tower_list) >= 0:
        for i in range(len(Tower_list)):
            if Tower_list[i][1].collidepoint(event.pos):
                return True,i
        return False,0

def round_down(numbers):
    return [math.floor(num / BS) * BS for num in numbers]

def delete_enemy(E_list,money):
    c = 0
    for j in range(len(E_list)):
        i = E_list[j-c]
        if not(i.check_alive()):
            money += i.money
            del(E_list[j-c])
            c += 1

    return E_list, money

def delay_hit(E_list,i, animations):
    i[1] -= 1
    if i[1] <= 0:
        animations.append([1,i[0],AL2])
        for j in E_list:
            dist = np.array(j.pos) - np.array(i[0])
            magnitude = (dist[0]**2+dist[1]**2)**(1/2)
            if magnitude <= i[3]:
                j.health -= i[2]
    return animations

def delete_bomb(Bomb_list):
    c = 0
    for j in range(len(Bomb_list)):
        i = Bomb_list[j-c]
        if i[1] <= 0:
            del(Bomb_list[j-c])
            c += 1
    return Bomb_list

def delete_animations(animations):
    c = 0
    for j in range(len(animations)):
        i = animations[j-c]
        if i[2] <= 0:
            del(animations[j-c])
            c += 1
    return animations

def draw_animations(animation):
    if animation[0] == 0:
        screen.blit(Flame1,animation[1])
    if animation[0] == 1:
        screen.blit(Flame2,animation[1])
    if animation[0] == 3:
        a = (tower(3,[0,0])).range
        pg.draw.circle(screen, [255,255,0], animation[1], (a/AL3)*(AL3-animation[2]), width=5)
    if animation[0] == 4:
        pos = np.array([animation[1]]) - np.array([0,20])
        screen.blit(Shot,pos[0])
    if animation[0] == 5:
        screen.blit(Flame4,animation[1])
    

    



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

def draw_window(time,E_list,Select,T_list,t_ind,animations,check_rad,Tower_locs,Money_text,Lives_text):
   
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
    for i in animations:
        draw_animations(i)
    pg.draw.polygon(screen, [0,0,255], OVERLAY)
    for j in range(len(Tower_locs)):
        i = Tower_locs[j]
        screen.blit(pg.transform.scale(pg.image.load(os.path.join('Images',tower(j+1,[200,200]).spr)),(BS,BS)),i)
    screen.blit(Money_text, (BS+10,HEIGHT-3*BS))
    screen.blit(Lives_text, (BS+10,HEIGHT-4*BS))
    pg.display.update()




def play(Enemy_info,money,lives):

    Enemy_list = []
    Tower_list = []
    delayed_projectiles = []
    animations_list = []
    Enemy_num = 0

    time = 0
    run = True
    Select = False
    check_rad = False
    tower_ind = False

    while run:
        clock.tick(25)
        time += 1
        
        if time == Enemy_info[Enemy_num,0]:
            Enemy_list.append(enemy(Enemy_info[Enemy_num,1]))
            Enemy_num += 1
        
        for i in Enemy_list:
            lives = i.move(lives) 

        for i in animations_list:
            i[2] -= 1

        for i in delayed_projectiles:
            animations_list = delay_hit(Enemy_list,i,animations_list)
        
        for i in Tower_list:
            target_point, animations_list = i[0].shoot(Enemy_list,animations_list)
            if any(target_point):
                target = target_point.copy()
                delayed_projectiles.append([target,i[0].delay,i[0].damage,i[0].bomb_range])
                


        Enemy_list, money = delete_enemy(Enemy_list, money)
        delayed_projectiles = delete_bomb(delayed_projectiles)
        animations_list = delete_animations(animations_list)

        if lives <= 0:
            run = False
        
        n_coins = str(money) + ' Coins'
        n_lives = str(lives) + ' Lives'
        Money_text = my_font.render(n_coins, False, (0, 0, 0))
        Lives_text = my_font.render(n_lives, False, (0, 0, 0))
            
        draw_window(time,Enemy_list,Select,Tower_list,tower_ind,animations_list,check_rad,Tower_locs,Money_text,Lives_text)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False

            if event.type == pg.MOUSEBUTTONDOWN:
                check_rad = False
                if Select == False:
                    Select, tower_type = Pick_tower(event,Tower_locs,money,Select)
                    check_rad, tower_ind = check_radius(event,Tower_list)
                
                elif Select == True:
                    Select, money = Place_tower(event,Select,money,Tower_list,tower_type)
                    Select = False
            
                




                        
                
                
        
        

