NP_PATH = np.array(PATH)
Enemy1_move = np.round((NP_PATH[1] - NP_PATH[0])/Enemy1_speed)
#
D = Dir[Enemy1_val]
    Enemy1_pos += np.int32((Enemy1_move*Enemy1_speed)/max(Enemy1_move))
    Enemy1_move -= D
    if sum(Enemy1_move) == 0:
        print('yay')
        Enemy1_val += 1
        Enemy1_move = np.round((NP_PATH[Enemy1_val] - NP_PATH[Enemy1_val])/Enemy1_speed)

        ####################################