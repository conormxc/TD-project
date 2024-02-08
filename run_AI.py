from read_functions import text_to_array
from game_loop import play
from game_loop_AI import play_AI
from genetic_algorithm import create_models
import numpy as np



file_path = 'Enemy_info.txt'
money = 200
lives = 10

models = create_models(10)

Enemy_info_old = np.int32(np.loadtxt(file_path, delimiter=','))
Enemy_info = text_to_array(file_path)

wave_num = play_AI(Enemy_info,money,lives,models[0])
print(wave_num)
