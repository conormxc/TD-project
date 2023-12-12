from TD_functions import play
from read_functions import text_to_array
import numpy as np

file_path = 'Enemy_info2.txt'
money = 625
lives = 100

Enemy_info_old = np.int32(np.loadtxt(file_path, delimiter=','))

Enemy_info = text_to_array(file_path)

wave_num = play(Enemy_info,money,lives)
print(wave_num)
