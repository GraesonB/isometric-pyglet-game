# Import Libraries and Modules ------------------------------------------------#

from variables import *
from data import *
from engine import *
from assets import *
import blockbuilder




build_grid(mapdata)
player = Player(player_temp, player_hurtbox, 8, 8, 1, speed = 5, accel = 1, fire_rate = 1/6, proj_speed = 6, hp = 10)
enemy = Enemy(enemy_temp, enemy_hurtbox, 13, 14, 1, hp = 100, fire_rate = 1/10, proj_speed = 4, accel = 0.1, speed = 3)
enemy2 = Enemy(enemy_temp, enemy_hurtbox, 2, 13, 1, hp = 100, fire_rate = 1/20, proj_speed = 4, accel = 0.1, speed = 3)
enemy3 = Enemy(enemy_temp, enemy_hurtbox, 13, 7, 1, hp = 100, fire_rate = 1/20, proj_speed = 4, accel = 0.1, speed = 1)
enemy4 = Enemy(enemy_temp, enemy_hurtbox, 13, 2, 1, hp = 100, fire_rate = 1/20, proj_speed = 4, accel = 0.1, speed = 2)
#boss = Boss(enemy_temp, enemy_hurtbox, 7.5, 7.5, 1)
