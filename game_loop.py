from TD_functions import *

def play(Enemy_raw_data,money,lives):

    Enemy_list = []
    Tower_list = []
    delayed_projectiles = []
    animations_list = []

    run = True
    Select = False
    check_rad = False
    tower_ind = False
    Wave = False
    Wave_num = 0
    Total_wave_num = Enemy_raw_data.shape[2]
    time = 0


    Play_button = pg.Rect(WIDTH - 2*BS,HEIGHT - 3*BS,BS,BS)

    while run:

            clock.tick(100)
            time += 1

            if not(Wave):
        

                All_enemies_deployed = False
                Enemy_num = 0

                for i in animations_list:
                    i[2] -= 1

                for i in delayed_projectiles:
                    animations_list = delay_hit(Enemy_list,i,animations_list)
                
                for i in Tower_list:
                    target_point, animations_list = i[0].shoot(Enemy_list,animations_list)
                    if any(target_point):
                        target = target_point.copy()
                        delayed_projectiles.append([target,i[0].delay,i[0].damage,i[0].bomb_range])
                
                delayed_projectiles = delete_bomb(delayed_projectiles)
                animations_list = delete_animations(animations_list)


                Money_text, Lives_text = display_text(money,lives)
                draw_window(time,Enemy_list,Select,Tower_list,tower_ind,animations_list,check_rad,Tower_locs,Money_text,Lives_text,Wave)
                pg.display.update()

                

                for event in pg.event.get():
                        if event.type == pg.QUIT:
                            run = False
                        if event.type == pg.MOUSEBUTTONDOWN:
                            check_rad = False
                            if Play_button.collidepoint(event.pos):
                                time = 0
                                Enemy_info = Enemy_raw_data[:,:,Wave_num] 
                                Wave = True
                                Wave_num += 1

                            elif Select == False:
                                Select, tower_type = Pick_tower(event,Tower_locs,money,Select)
                                check_rad, tower_ind = check_radius(event,Tower_list)
                            
                            elif Select == True:
                                Select, money = Place_tower(event,Select,money,Tower_list,tower_type)
                                Select = False

            else:

                
                if time == Enemy_info[Enemy_num,0]:
                    Enemy_list.append(enemy(Enemy_info[Enemy_num,1]))
                    Enemy_num += 1

                if Enemy_info[Enemy_num,0] == 0:
                    All_enemies_deployed = True
                
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
                    return Wave_num
                if not(len(Enemy_list)) and All_enemies_deployed:
                    Wave = False
                    if Wave_num == Total_wave_num:
                        return Wave_num + 1

                    
                
                Money_text, Lives_text = display_text(money,lives)    
                draw_window(time,Enemy_list,Select,Tower_list,tower_ind,animations_list,check_rad,Tower_locs,Money_text,Lives_text,Wave)

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
                    
                    
