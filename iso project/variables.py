import pyglet as pg
# Variables -------------------------------------------------------------------#
scale = 2
#asset size is used for calculating spacing between grid tiles and iso rendering
asset_size = 32


# Screen dims
screen_width = 640
screen_height = 400
screen_loc = (0,0)

grid_screen_width = 16 * asset_size
grid_screen_height = 16 * asset_size
grid_loc = (800,0)

p_list = []
e_list = []
ent_list = []
player_bullets = []
enemy_bullets = []
wall_list =[]

grid_batch = pg.graphics.Batch()
batch = pg.graphics.Batch()
