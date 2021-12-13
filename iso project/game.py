# Import Libraries and Modules ------------------------------------------------#
import pyglet as pg
import numpy as np
import threading
from pyglet import clock
from pyglet.gl import *

from variables import *
from engine import *
from instance import *

window2 = Window(screen_width, screen_height, screen_loc)
#window = Window(grid_screen_width, grid_screen_height, grid_loc)
#glClearColor(255, 255, 255, 1.0)

pg.clock.get_fps()


# Events  ---------------------------------------------------------------------#

# Allow Player class to handle key inputs

window2.push_handlers(player.keys)

# Function that handles all updates
def update_entities(dt):

    # Mouse stuff here because I don't know how to properly use mouse events
    player.mouse_pos = window2.mouse_pos
    player.mouse_left = window2.mouse_left
    player.mouse_right = window2.mouse_right

    # enemy.target = player
    # enemy2.target = player

    to_add_p = []
    for entity in p_list:
        entity.update(dt)
        to_add_p.extend(entity.children)
        entity.children = []
    player_bullets.extend(to_add_p)
    ent_list.extend(to_add_p)

    to_add_e = []
    for entity in e_list:
        entity.update(dt)
        to_add_e.extend(entity.children)
        entity.children = []
    enemy_bullets.extend(to_add_e)
    ent_list.extend(to_add_e)

    for entity in player_bullets:
        entity.update(dt)
    for entity in enemy_bullets:
        entity.update(dt)

    for entity in p_list:
        for bullet in enemy_bullets:
            if not entity.dead and not bullet.dead and not entity.intangible:
                if entity.collides(bullet):
                    entity.handle_collision(bullet)
                    bullet.handle_collision(entity)

    for entity in e_list:
        for bullet in player_bullets:
            if not entity.dead and not bullet.dead and not entity.intangible:
                if entity.collides(bullet):
                    entity.handle_collision(bullet, bullet.damage)
                    bullet.handle_collision(entity)

    for entity in ent_list:
        if entity.dead:
            entity.delete()

    if player.debug:
        for entity in e_list:
            #print(str(entity) + 'position: ' + str(entity.pos))
            print('FPS: ' + str(clock.get_fps()))
            print('Entity Count: ' + str(len(ent_list)))

# Draw everything
# @window.event
# def on_draw():
#     window.clear()
#     grid_batch.draw()

@window2.event
def on_draw():
    window2.clear()
    batch.invalidate()
    batch.draw()

# Debug Text ------------------------------------------------------------------#

#player_pos = pg.text.Label(text = ('Player pos: ' + str(player.pos)), x = 40, y = screen_height - 50)


# Scheduling the update function 60 times a second (60 FPS)
pg.clock.schedule_interval(update_entities, 1/60)

# Game Loop -------------------------------------------------------------------#
if __name__ == '__main__':

    pg.app.run()
