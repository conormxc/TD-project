from TD_functions import play
from read_functions import text_to_array
import numpy as np

file_path = 'Enemy_info.txt'
money = 200
lives = 10

Enemy_info = np.int32(np.loadtxt(file_path, delimiter=','))

#Enemy_info = text_to_array(file_path)

play(Enemy_info,money,lives)

