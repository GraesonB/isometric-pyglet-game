# Import Libraries and Modules ------------------------------------------------#

from variables import *
from data import *
from engine import *
from assets import *
from forestdemon import *
import time



build_grid(mapdata)
graph = mapdata[1]
player = Player(player_temp, test_dict, player_hurtbox, 12, 2, 1, mapdata[1], speed = 2.1, accel = 1, fire_rate = 1/5, proj_speed = 4, hp = 10)
enemy = ForestDemon(enemy_temp, test2_dict, golem_hurtbox, 2, 12, 1, mapdata[1], hp = 1125, fire_rate = 110, proj_speed = 1, accel = 0.5, speed = 0.7)
# for enemy_spawn in range(2):
#     x_spawn = 4 + enemy_spawn * 2
#     y_spawn = 4 + enemy_spawn * 2
#     enemy = Enemy(enemy_temp, iron_golem_dict, enemy_hurtbox, x_spawn, 4, 1, mapdata[1], hp = 53, fire_rate = 6, proj_speed = 8, accel = 0.2, speed =0.5)
#     enemy2 = Enemy(enemy_temp, iron_golem_dict, enemy_hurtbox, 2, y_spawn, 1, mapdata[1], hp = 53, fire_rate = 6, proj_speed = 8, accel = 0.2, speed =0.5)
