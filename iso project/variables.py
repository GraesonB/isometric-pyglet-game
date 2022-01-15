import pyglet as pg
# Variables -------------------------------------------------------------------#
scale = 2
#asset size is used for calculating spacing between grid tiles and iso rendering
asset_size = 32


# Screen dims
screen_width = 900
screen_height = 600
screen_loc = (0,0)

grid_screen_width = 16 * asset_size
grid_screen_height = 16 * asset_size
grid_loc = (900,0)

p_list = []
e_list = []
ent_list = []
player_bullets = []
enemy_bullets = []
wall_list =[]
sorting_list = []
batched_wall_list = []
# A list of every entity's position, dimension, and velocity
e_pos_dim_vel = []

grid_batch = pg.graphics.Batch()
batch = pg.graphics.Batch()
front_batch = pg.graphics.Batch()
back_batch = pg.graphics.Batch()
