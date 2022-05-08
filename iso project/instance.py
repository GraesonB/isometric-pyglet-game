# Import Libraries and Modules ------------------------------------------------#

from variables import *
from data import *
from engine import *
from assets import *
from forestdemon import *
import time



build_grid(mapdata)
graph = mapdata[1]
player = Player(player_temp, test_dict, player_hurtbox, 12, 2, 1, mapdata[1], speed = 2.1, accel = 1, fire_rate = 1/7, proj_speed = 4, hp = 10)
enemy = ForestDemon(enemy_temp, test2_dict, golem_hurtbox, 2, 12, 1, mapdata[1], hp = 125, accel = 0.5, speed = 0.7)
enemy = ForestDemon(enemy_temp, test2_dict, golem_hurtbox, 2, 2, 1, mapdata[1], hp = 125, accel = 0.5, speed = 0.7)
# for enemy_spawn in range(4):
#     x_spawn = 4 + enemy_spawn * 2
#     y_spawn = 4 + enemy_spawn * 2
#     enemy = ForestDemon(enemy_temp, test2_dict, enemy_hurtbox, x_spawn, 4, 1, mapdata[1], hp = 153, accel = 0.2, speed =0.5)
