# Import Libraries and Modules ------------------------------------------------#

from variables import *
from data import *
from engine import *
from assets import *
import blockbuilder



build_grid(mapdata)
player = Player(goat, goat_dict, player_hurtbox, 8, 12, 1, mapdata[1], speed = 3, accel = 0.5, fire_rate = 1/6, proj_speed = 8, hp = 10)
enemy = Enemy(enemy_temp, goat_dict, enemy_hurtbox, 2, 2, 1, mapdata[1], hp = 25, fire_rate = 5, proj_speed = 4, accel = 0.5, speed = 2)


# for enemy_spawn in range(2):
#     x_spawn = 4 + enemy_spawn * 4
#     y_spawn = 4 + enemy_spawn * 4
#     enemy = Enemy(enemy_temp, goat_dict, enemy_hurtbox, x_spawn, 4, 1, hp = 3, fire_rate = 1/2, proj_speed = 8, accel = 0.1, speed =1)
#     enemy2 = Enemy(enemy_temp, goat_dict, enemy_hurtbox, 2, y_spawn, 1, hp = 3, fire_rate = 1/2, proj_speed = 8, accel = 0.1, speed =1)
