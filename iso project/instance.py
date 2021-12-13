# Import Libraries and Modules ------------------------------------------------#

from variables import *
from data import *
from engine import *
from assets import *





player = Player(player_temp, player_hurtbox, 5, 5, 1, speed = 4, accel = 2, fire_rate = 1/4, proj_speed = 16)
# enemy = Enemy(enemy_temp, enemy_hurtbox, 13, 13, 1, hp = 100, fire_rate = 1/2, proj_speed = 5, accel = 0.01, speed = 1)
# enemy2 = Enemy(enemy_temp, enemy_hurtbox, 2, 13, 1, hp = 100, fire_rate = 1/6, proj_speed = 5, accel = 0.01, speed = 1)
build_grid(mapdata)
#enemy2 = Enemy(enemy_hurtbox, 13, 7, fire_rate = 1/10, proj_speed = 5)
#enemy3 = Enemy(enemy_hurtbox, 13, 2, fire_rate = 1/10, proj_speed = 5)
#enemy4 = Enemy(enemy_hurtbox, 13, 13, fire_rate = 1/10, proj_speed = 5)
boss = Boss(enemy_temp, boss_hurtbox, 8, 6, 1)
