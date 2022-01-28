# Import Libraries ------------------------------------------------------------#
import pyglet as pg
import os
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

# in aseprite, save files as "entity_name-{tag}-{tagframe00}.png"
def images_to_animation(directory, idle_duration = (5/60), run_duration = (5/60)):
    idle_dict = {}
    run_dict = {}
    for file in os.listdir(directory):
        if file.endswith('.png'):
            if 'base' in str(file):
                base_image = pg.resource.image(directory + '/' + str(file))
                base_image.anchor_x = base_image.width / 2
            if 'idle' in str(file):
                image = pg.resource.image(directory + '/' + str(file))
                set_anchors_tm_tall_body(image)
                idle_dict.update( {str(file) : image})
            if 'run' in str(file):
                image = pg.resource.image(directory + '/' + str(file))
                run_dict.update( {str(file) : image})
    idle_list = []
    run_list = []
    for key in sorted(idle_dict.keys()):
        idle_list.append(idle_dict[key])
    idle_animation = pg.image.Animation.from_image_sequence(idle_list, duration = idle_duration)
    # for key in sorted(run_dict.keys()):
    #     run_list.append(idle_dict[key])
    #
    # run_animation = pg.image.Animation.from_image_sequence(run_list, duration = run_duration)

    return [idle_animation]

# Assets  ---------------------------------------------------------------------#
grid_tile = pg.resource.image(str(grid_dir) + '/grid tile.png')
void_tile = pg.resource.image(str(grid_dir) + '/void.png')

player_hurtbox = pg.resource.image(str(grid_dir) + '/player_hurtbox.png')
enemy_hurtbox = pg.resource.image(str(grid_dir) + '/enemy.png')
boss_hurtbox = pg.resource.image(str(grid_dir) + '/boss.png')

player_bullet = pg.resource.image(str(grid_dir) + '/player_bullet.png')
enemy_bullet = pg.resource.image(str(grid_dir) + '/enemy_bullet.png')
charge_bullet = pg.resource.image(str(grid_dir) + '/charge_bullet.png')

nightmare_floor = pg.resource.image(str(world_dir) + '/nightmare_floor.png')
nightmare_wall = pg.resource.image(str(world_dir) + '/nightmare_wall.png')
wall_iso = pg.resource.image(str(world_dir) + '/wall.png')
floor_iso = pg.resource.image(str(world_dir) + '/floor.png')

player_temp = pg.resource.image(str(character_dir) + '/player temp.png')
goat = pg.resource.image(str(character_dir) + '/goat.png')
enemy_temp = pg.resource.image(str(character_dir) + '/enemy temp.png')

p_bullet_temp = pg.resource.image(str(character_dir) + '/player bullet temp.png')
p_bullet_temp2 = pg.resource.image(str(character_dir) + '/player bullet temp2.png')
p_charge_bullet = pg.resource.image(str(character_dir) + '/player charge bullet.png')
e_bullet_temp = pg.resource.image(str(character_dir) + '/enemy bullet temp.png')

set_anchors_tl(player_hurtbox)
set_anchors_tl(grid_tile)
set_anchors_tl(void_tile)
set_anchors_tl(enemy_hurtbox)
set_anchors_tl(boss_hurtbox)

set_anchors_tl(player_bullet)
set_anchors_tl(enemy_bullet)
set_anchors_tl(charge_bullet)

set_anchors_tm(nightmare_wall)
set_anchors_tm(nightmare_floor)
set_anchors_tm(wall_iso)
set_anchors_tm(floor_iso)

set_anchors_tm_tall_body(player_temp)
set_anchors_tm_tall_body(goat)
set_anchors_tm_tall_body(enemy_temp)

set_anchors_tm_tall_body(e_bullet_temp)
set_anchors_tm_tall_body(p_bullet_temp)
set_anchors_tm_tall_body(p_bullet_temp2)
set_anchors_tm_tall_body(p_charge_bullet)


# Build Animations ------------------------------------------------------------#

# baby goat
goat_east_dir = 'Assets/Character Assets/goat/east'
goat_east = images_to_animation(goat_east_dir, idle_duration = 8/60)



# Entity Dictionaries ---------------------------------------------------------#

goat_dict = {
'idle_east' : goat_east[0]
}

# Text ------------------------------------------------------------------------#


glEnable(GL_TEXTURE_2D)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
