# Import Libraries and Modules ------------------------------------------------#
import pyglet as pg
import numpy as np
from pyglet import clock
from pyglet.gl import *

from variables import *
from engine import *
from data import *
from forestdemon import *
from death import *
from assets import *

window2 = Window(screen_width, screen_height, screen_loc)
#window = Window(grid_screen_width, grid_screen_height, grid_loc)

# Instance --------------------------------------------------------------------#


build_grid(mapdata)
graph = mapdata[1]
player = Player(player_temp, test_dict, player_hurtbox, 4, 12, 1, mapdata[1], speed = 2.5, accel = 1, fire_rate = 1/7, proj_speed = 4, hp = 20)
#enemy = ForestDemon(enemy_temp, test2_dict, golem_hurtbox, 3, 5, 1, mapdata[1], hp = 75, accel = 0.5, speed = 0.5)
#enemy = Death(enemy_temp, death_dict, golem_hurtbox, 8, 8, 1, mapdata[1], hp = 75, accel = 0.5, speed = 0.75)

bg_r, bg_g, bg_b = rgb_to_float(10,10,15)
glClearColor(bg_r, bg_g, bg_b, 1.0)

pg.clock.get_fps()

# Events  ---------------------------------------------------------------------#

# Allow Player class to handle key inputs
window2.push_handlers(player.keys)

# Function that handles all updates
def update_entities(dt):

    player_mouse_avg[0] =  (player.pos[0] + ((player.pos[0] + ((player.pos[0] + player.mouse_pos[0]) / 2)) / 2)) / 2
    player_mouse_avg[1] =  (player.pos[1] + ((player.pos[1] + ((player.pos[1] + player.mouse_pos[1]) / 2)) / 2)) / 2
    camera_movement[0] += (player_mouse_avg[0] - camera_movement[0]) / 10
    camera_movement[1] += (player_mouse_avg[1] - camera_movement[1]) / 10
    player.mouse_pos[0] = window2.mouse_pos[0] + camera_movement[0] - 1
    player.mouse_pos[1] = window2.mouse_pos[1] + camera_movement[1] - 1

    player.mouse_left = window2.mouse_left
    player.mouse_right = window2.mouse_right

    update_gridgraph(graph)
    update_rect_list()

    # For all players, establish velocity vectors, and add children to list
    to_add_p = []
    for entity in p_list:
        entity.update(dt)
        to_add_p.extend(entity.children)
        entity.children = []
    player_bullets.extend(to_add_p)
    ent_list.extend(to_add_p)

    # For all enemies, establishs velocity vectors, and add children to list
    to_add_e = []
    for entity in e_list:
        entity.target = player
        entity.update(dt)
        to_add_e.extend(entity.children)
        entity.children = []
    enemy_bullets.extend(to_add_e)
    ent_list.extend(to_add_e)

    # Establish velocity vectors for bullets
    for entity in player_bullets:
        entity.update(dt)
    for entity in enemy_bullets:
        entity.update(dt)

    for entity in ent_list:
        entity.post_wall_update(dt)

    for wall in tile_update_list:
        wall.update_pos(dt)


    for entity in p_list:
        for bullet in enemy_bullets:
            if not entity.dead and not bullet.dead and not entity.intangible:
                if entity.collides(bullet):
                    entity.handle_collision(bullet)
                    bullet.handle_collision(entity)

    for entity in barrier_list:
        for bullet in player_bullets:
            if not entity.dead and not bullet.dead:
                if entity.collides(bullet):
                    if entity.collides(bullet):
                        entity.handle_collision(bullet, bullet.damage)
                        bullet.handle_collision(entity)

    for entity in e_list:
        for bullet in player_bullets:
            if not entity.dead and not bullet.dead and not entity.intangible:
                if entity.collides(bullet):
                    entity.handle_collision(bullet, bullet.damage)
                    bullet.handle_collision(entity)

    for projectile in return_projectile_list:
        if projectile.collides_parent(projectile.parent):
            projectile.handle_parent_collision()
            projectile.parent.handle_return_projectile()

    for entity in ent_list:
        if entity.dead:
            entity.delete()
    for entity in barrier_list:
        if entity.dead:
            entity.delete()
    if player.debug:
        print(player.pos)

    # Sorting list for ordering sprite depth, not perfect sorting but it's good enough
    window2.sorting_list = ent_list + wall_list + barrier_list
    window2.sorting_list.sort(key = lambda e: ((np.floor(e.pos[0]) + np.floor(e.pos[1])), (e.pos[0]) + (e.pos[1])))

# Draw everything
# @window.event
# def on_draw():
#     window.clear()
#     grid_batch.draw()

@window2.event
def on_draw():
    window2.clear()
    back_batch.draw()
    for entity in window2.sorting_list:
        entity.draw_sprites()
    front_batch.draw()

# Debug Text ------------------------------------------------------------------#

#player_pos = pg.text.Label(text = ('Player pos: ' + str(player.pos)), x = 40, y = screen_height - 50)
# Scheduling the update function 60 times a second (60 FPS)
pg.clock.schedule_interval(update_entities, 1/120)

# Game Loop -------------------------------------------------------------------#
if __name__ == '__main__':

    pg.app.run()
