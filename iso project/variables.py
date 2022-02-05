import pyglet as pg

# This will scale all assets
scale = 4

# Asset size is used for calculating spacing between grid tiles and iso rendering
asset_size = 32
theme = 'nightmare'

# Screen dims
screen_width = 900
screen_height = 900
screen_loc = (0,0)
grid_screen_width = 16 * asset_size
grid_screen_height = 16 * asset_size
grid_loc = (900,0)

# Initialize lists
p_list = []
e_list = []
ent_list = []
player_bullets = []
enemy_bullets = []
wall_list =[]
tile_update_list = []
sorting_list = []
batched_list = []
player_mouse_avg = [0,0]
camera_movement = [0,0]


# Set batches and ordered groups
grid_batch = pg.graphics.Batch()
grid_floor_group = pg.graphics.OrderedGroup(0)
grid_entity_group = pg.graphics.OrderedGroup(1)
batch = pg.graphics.Batch()

front_batch = pg.graphics.Batch()
back_batch = pg.graphics.Batch()
floor_group = pg.graphics.OrderedGroup(0)
back_wall_group = pg.graphics.OrderedGroup(1)
