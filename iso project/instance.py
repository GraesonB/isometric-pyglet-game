# Import Libraries and Modules ------------------------------------------------#

from variables import *
from data import *
from engine import *
from assets import *
import blockbuilder




build_grid(mapdata)
player = Player(goat, goat_dict, player_hurtbox, 16, 16, 1, speed = 5, accel = 0.5, fire_rate = 1/30, proj_speed = 10, hp = 10)


for enemy_spawn in range(4):
    x_spawn = 4 + enemy_spawn * 2
    y_spawn = 4 + enemy_spawn * 2
    enemy = Enemy(enemy_temp, None, enemy_hurtbox, x_spawn, 4, 1, hp = 3, fire_rate = 5, proj_speed = 4, accel = 0.1, speed = 3)
    enemy2 = Enemy(enemy_temp, None, enemy_hurtbox, 4, y_spawn, 1, hp = 3, fire_rate = 5, proj_speed = 4, accel = 0.1, speed = 3)
    #enemy2 = Enemy(enemy_temp, None, enemy_hurtbox, x_spawn, y_spawn, 1, hp = 3, fire_rate = 3, proj_speed = 4, accel = 0.1, speed = 3)
