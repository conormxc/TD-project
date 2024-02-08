
from read_functions import text_to_array
from game_loop import play
import numpy as np


file_path = 'Enemy_info.txt'
money = 200
lives = 20

Enemy_info_old = np.int32(np.loadtxt(file_path, delimiter=','))

Enemy_info = text_to_array(file_path)

wave_num = play(Enemy_info,money,lives)
print(wave_num)
