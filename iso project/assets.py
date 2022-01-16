# Import Libraries ------------------------------------------------------------#
import pyglet as pg
from pyglet.gl import *

from variables import *

# art inspo https://www.deviantart.com/sky-burial/art/Insomnia-Blade-746441396

# Directories -----------------------------------------------------------------#

grid_dir = 'Assets/Grid Assets'
world_dir = 'Assets/World Assets'
character_dir = 'Assets/Character Assets'

# Function  -------------------------------------------------------------------#

def set_anchors_tl(image):
    image.anchor_y = image.height

def set_anchors_center(image):
    image.anchor_y = image.height / 2
    image.anchor_x = image.width / 2

def set_anchors_tm(image):
    image.anchor_y = image.height / 2
    image.anchor_x = image.width / 2

def set_anchors_tm_tall_body(image):
    image.anchor_y = image.width / 2
    image.anchor_x = image.width / 2

# Import Libraries ------------------------------------------------------------#
grid_tile = pg.resource.image(str(grid_dir) + '/grid tile.png')
void_tile = pg.resource.image(str(grid_dir) + '/void.png')

player_hurtbox = pg.resource.image(str(grid_dir) + '/player_hurtbox.png')
enemy_hurtbox = pg.resource.image(str(grid_dir) + '/enemy.png')
boss_hurtbox = pg.resource.image(str(grid_dir) + '/boss.png')

player_bullet = pg.resource.image(str(grid_dir) + '/player_bullet.png')
enemy_bullet = pg.resource.image(str(grid_dir) + '/enemy_bullet.png')
charge_bullet = pg.resource.image(str(grid_dir) + '/charge_bullet.png')

purple_cube = pg.resource.image(str(world_dir) + '/purple cube.png')
wall_iso = pg.resource.image(str(world_dir) + '/wall.png')
floor_iso = pg.resource.image(str(world_dir) + '/floor.png')

player_temp = pg.resource.image(str(character_dir) + '/player temp.png')
enemy_temp = pg.resource.image(str(character_dir) + '/enemy temp.png')

p_bullet_temp = pg.resource.image(str(character_dir) + '/player bullet temp.png')
e_bullet_temp = pg.resource.image(str(character_dir) + '/enemy bullet temp.png')

set_anchors_tl(player_hurtbox)
set_anchors_tl(grid_tile)
set_anchors_tl(void_tile)
set_anchors_tl(enemy_hurtbox)
set_anchors_tl(boss_hurtbox)

set_anchors_tl(player_bullet)
set_anchors_tl(enemy_bullet)
set_anchors_tl(charge_bullet)

set_anchors_tm(purple_cube)
set_anchors_tm(wall_iso)
set_anchors_tm(floor_iso)

set_anchors_tm_tall_body(player_temp)
set_anchors_tm_tall_body(enemy_temp)

set_anchors_tm_tall_body(e_bullet_temp)
set_anchors_tm_tall_body(p_bullet_temp)

# Text ------------------------------------------------------------------------#


glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
