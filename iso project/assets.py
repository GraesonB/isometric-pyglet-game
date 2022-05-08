# Import Libraries ------------------------------------------------------------#
import pyglet as pg
import os
from pyglet.gl import *

from variables import *

# Directories -----------------------------------------------------------------#

grid_dir = 'Assets/Grid Assets'
world_dir = 'Assets/World Assets'
character_dir = 'Assets/Character Assets'

# Function  -------------------------------------------------------------------#

# OpenGL stuff to remove antialiasing
def pixelate(image):
    texture = image.get_texture()
    glBindTexture(texture.target, texture.id)
    glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glBindTexture(texture.target, 0)

def set_anchors_tl(image):
    image.anchor_y = image.height
    pixelate(image)

def set_anchors_center(image):
    image.anchor_y = image.height / 2
    image.anchor_x = image.width / 2
    texture = image.get_texture()
    pixelate(image)

def set_anchors_tm(image):
    image.anchor_y = image.height
    image.anchor_x = image.width / 2
    texture = image.get_texture()
    pixelate(image)

def set_anchors_tm_tall_body(image, hurtbox):
    image.anchor_y = hurtbox.width * 4 / 2
    image.anchor_x = image.width / 2
    texture = image.get_texture()
    pixelate(image)

# # returns a dictionary of animations which are dictionaries of animation directions which are lists of images
# def img_to_animation2(hurtbox, directory, ani_duration = (2/60), anchors = 'tall body'):
#     animation_dictionary = {}
#     # for loop for each animation
#     for animation_name in os.listdir(directory):
#         if "." not in animation_name:
#             ani_directory = directory + "/" + animation_name
#             # create a dictionary for the directions
#             animation_directions = {}
#             for direction in os.listdir(ani_directory):
#                 if "." not in direction:
#                     direction_directory = ani_directory + "/" + direction
#                     animation_list = []
#                     for frame in sorted(os.listdir(direction_directory)):
#                         # make a list of every frame of the animation
#                         if frame.endswith('.png'):
#                             image = pg.resource.image(direction_directory + '/' + str(frame))
#                             if anchors == "tall body":
#                                 set_anchors_tm_tall_body(image, hurtbox)
#                             if anchors == 'center':
#                                 set_anchors_center(image)
#                             animation_list.append(image)
#                     # append the animation list to the dictionary of all directions
#                     ani = pg.image.Animation.from_image_sequence(animation_list, duration = ani_duration)
#                     animation_directions[direction] = ani
#                 # finally, build a dictionary of all animations
#             animation_dictionary[animation_name] = animation_directions
#     return animation_dictionary

def img_to_animation2(hurtbox, directory, ani_duration = (2/60), anchors = 'tall body'):
    animation_dictionary = {}
    # for loop for each animation
    for animation_name in os.listdir(directory):
        if "." not in animation_name:
            ani_directory = directory + "/" + animation_name
            # create a dictionary for the directions
            animation_directions = {}
            for direction in os.listdir(ani_directory):
                if "." not in direction:
                    direction_directory = ani_directory + "/" + direction
                    animation_list = []
                    for frame in sorted(os.listdir(direction_directory)):
                        # make a list of every frame of the animation
                        if frame.endswith('.png'):
                            image = pg.resource.image(direction_directory + '/' + str(frame))
                            if anchors == "tall body":
                                set_anchors_tm_tall_body(image, hurtbox)
                            if anchors == 'center':
                                set_anchors_center(image)
                            animation_list.append(image)
                    # append the animation list to the dictionary of all directions
                    animation_directions[direction] = animation_list
                # finally, build a dictionary of all animations
            animation_dictionary[animation_name] = animation_directions
    return animation_dictionary


# in aseprite, save files as "entity_name-{innertag}-{outertag}-{innertagframe00}.png"
def images_to_animation(hurtbox, directory, ani_duration = (5/60)):
    image_dict = {}
    directions = ['-N-','-NW-','-W-','-SW-','-S-','-SE-','-E-','-NE-']
    for file in os.listdir(directory):
        if file.endswith('.png'):
            image = pg.resource.image(directory + '/' + str(file))
            texture = image.get_texture()
            glEnable(texture.target)
            glTexParameteri(texture.target, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            set_anchors_tm_tall_body(image, hurtbox)
            image_dict.update({str(file) : image})

    animation_dict = {}
    base = [[],[],[],[],[],[],[],[]]
    idle = [[],[],[],[],[],[],[],[]]
    walk = [[],[],[],[],[],[],[],[]]
    run = [[],[],[],[],[],[],[],[]]
    direction_val = 0
    for direction in directions:
        for key in sorted(image_dict.keys()):
            if direction in key:
                if 'base' in key:
                    base[direction_val].append(image_dict[key])
                if 'idle' in key:
                    idle[direction_val].append(image_dict[key])
                if 'walk' in key:
                    walk[direction_val].append(image_dict[key])
                if 'run' in key:
                    run[direction_val].append(image_dict[key])
        direction_val += 1
    directions = ['north','northwest','west','southwest','south','southeast','east','northeast']
    type = ['base','idle', 'walk', 'run']
    animation_types = [base, idle, walk, run]
    for t,animation_type in enumerate(animation_types):
        for dir,animation in enumerate(animation_type):
            if animation:
                key = type[t]+'_'+directions[dir]
                ani = pg.image.Animation.from_image_sequence(animation, duration = ani_duration)
                animation_dict[key] = ani

    return animation_dict


# Assets  ---------------------------------------------------------------------#
grid_tile = pg.resource.image(str(grid_dir) + '/grid tile.png')
void_tile = pg.resource.image(str(grid_dir) + '/void.png')

player_hurtbox = pg.resource.image(str(grid_dir) + '/player_hurtbox.png')
enemy_hurtbox = pg.resource.image(str(grid_dir) + '/enemy.png')
golem_hurtbox = pg.resource.image(str(grid_dir) + '/golem_hurtbox.png')
boss_hurtbox = pg.resource.image(str(grid_dir) + '/boss.png')

player_bullet = pg.resource.image(str(grid_dir) + '/player_bullet.png')
enemy_bullet = pg.resource.image(str(grid_dir) + '/enemy_bullet.png')
charge_bullet = pg.resource.image(str(grid_dir) + '/charge_bullet.png')

nightmare_floor = pg.resource.image(str(world_dir) + '/nightmare_floor.png')
nightmare_wall = pg.resource.image(str(world_dir) + '/nightmare_wall.png')
placeholder = pg.resource.image(str(world_dir) + '/placeholder.png')
wall_iso = pg.resource.image(str(world_dir) + '/wall.png')
floor_iso = pg.resource.image(str(world_dir) + '/floor.png')
stone_floor = pg.resource.image(str(world_dir) + '/stone floor 512.png')

player_temp = pg.resource.image(str(character_dir) + '/player temp.png')
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
set_anchors_tl(golem_hurtbox)

set_anchors_center(player_bullet)
set_anchors_tl(enemy_bullet)
set_anchors_tl(charge_bullet)

set_anchors_center(nightmare_wall)
set_anchors_center(placeholder)
set_anchors_tm(stone_floor)
set_anchors_tm(nightmare_floor)
set_anchors_tm(wall_iso)
set_anchors_tm(floor_iso)

set_anchors_tm_tall_body(player_temp, player_hurtbox)
set_anchors_tm_tall_body(enemy_temp, enemy_hurtbox)

set_anchors_tm_tall_body(e_bullet_temp, enemy_bullet)
set_anchors_tm_tall_body(p_bullet_temp, player_bullet)
set_anchors_tm_tall_body(p_bullet_temp2, player_bullet)
set_anchors_tm_tall_body(p_charge_bullet, charge_bullet)

# Build Animations ------------------------------------------------------------#

test_dir = 'Assets/Character Assets/TEST'
test_dict = img_to_animation2(player_hurtbox, test_dir)
test2_dir = 'Assets/Character Assets/test_2'
test2_dict = img_to_animation2(golem_hurtbox, test2_dir)
placeholder_dir = 'Assets/Character Assets/placeholder'
placeholder_dict = img_to_animation2(player_hurtbox, placeholder_dir)
bullet_dir = 'Assets/Character Assets/bullets'
bullet_dict = img_to_animation2(player_hurtbox, bullet_dir)
death_dir = 'Assets/Character Assets/death'
death_dict = img_to_animation2(golem_hurtbox, death_dir)
# Add wither animation
plants_dir = 'Assets/Character Assets/plants'
plants_dict = img_to_animation2(player_hurtbox, plants_dir, anchors = "center")
wither = plants_dict['grow']['W'].copy()
wither = (list(reversed(wither[0:8])))
plants_dict['wither'] = {'W' : wither}


# Entity Dictionaries ---------------------------------------------------------#



# Text ------------------------------------------------------------------------#


# glEnable(GL_TEXTURE_2D)
# glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
