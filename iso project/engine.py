# Import Libraries and Modules ------------------------------------------------#
import pyglet as pg
import numpy as np
from queue import PriorityQueue
from pyglet.window import key, mouse
import time

from data import *
from variables import *
from assets import *
import blockbuilder

# Functions -------------------------------------------------------------------#

def man_distance(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return (abs(x1-x2) + abs(y1-y2))

def build_grid(mapdata):
    if theme == 'nightmare':
        floor = nightmare_floor
        wall = nightmare_wall
    else:
        floor = floor_iso
        wall = wall_iso
    for z, layer  in enumerate(mapdata):
        for y,row in enumerate(layer):
            for x,tile in enumerate(row):

                if tile and z == 0:
                    tile = Tile(floor, None, void_tile, x, y, z, bat = back_batch, grp = floor_group, grid_grp = grid_floor_group)
                    batched_list.append(tile)
                elif tile and x == 0 or y == 0:
                    tile = Tile(wall, None, grid_tile, x, y, z, bat = back_batch, grp = back_wall_group)
                    batched_list.append(tile)
                elif tile and x == (len(mapdata[1]) -1) or y == (len(mapdata[1]) -1):
                    tile = Tile(wall, None, grid_tile, x, y, z, bat = front_batch)
                    batched_list.append(tile)
                elif tile:
                    tile = Tile(wall, None, grid_tile, x, y, z)
                    wall_list.append(tile)


def player_lives(image, num_lives):
    player_lives = []
    for i in range(num_lives):
        x = (screen_width - 40) - (20*i)
        y = (screen_height - 20)
        new_sprite = pg.sprite.Sprite(img = image, x = x, y = y, batch = front_batch)
        player_lives.append(new_sprite)
    return player_lives

def distance(point1 = [0,0], point2 = [0,0]):
    return (np.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2))

# def iso_coords(x, y, z):
#     coord_vec = np.array([[x],
#                          [y]])
#     grid_transform = np.array([[0.5 * asset_size * scale, -0.5 * asset_size * scale],
#                             [0.25 * asset_size * scale, 0.25 * asset_size * scale]])
#     xy_transform = np.dot(grid_transform,coord_vec)
#     xyz_array = (np.append(xy_transform, -z))
#     xyz_array[0] =  (xyz_array[0] - (asset_size / 2)) + (screen_width / 2)
#     xyz_array[1] = screen_height - xyz_array[1]
#     return xyz_array

def iso_coords(x, y, z):
    iso_x = (0.5 * asset_size * scale * x) + (-0.5 * asset_size * scale * y)
    iso_x = (iso_x - (asset_size / 2)) + (screen_width / 2)
    iso_y = (0.25 * asset_size * scale * x) + (0.25 * asset_size * scale * y)
    # below we take half the screen_height to center on player
    iso_y = (screen_height / 2) - iso_y  - asset_size * 2
    xyz = [iso_x, iso_y, z * asset_size * scale]
    return xyz

def invert_iso(x,y):
    coord_vec = np.array([[x + (asset_size / 2) - (screen_width / 2)],
                          [(screen_height / 2) - y + asset_size * 2]])
    grid_transform = np.linalg.inv(np.array([[0.5 * asset_size * scale, -0.5 * asset_size * scale],
                                       [0.25 * asset_size * scale, 0.25 * asset_size * scale]]))
    xy_transform = np.dot(grid_transform,coord_vec)
    xyz_array = (xy_transform).reshape(2)
    xyz_array[0] = xyz_array[0]
    xyz_array[1] = xyz_array[1]
    return xyz_array

def collision_time2(dt, object, wall, vector):
    wall_pt1 = wall[0]
    wall_pt2 = wall[1]
    if vector[0] > 0:
        x_entry = wall_pt1[0] - (object.pos[0]  + object.width / asset_size)
        x_exit = wall_pt2[0] - object.pos[0]
    else:
        x_entry = wall_pt2[0] - object.pos[0]
        x_exit = wall_pt1[0] - (object.pos[0]  + object.width / asset_size)
    if vector[1] > 0:
        y_entry = wall_pt1[1] - (object.pos[1] + object.height / asset_size)
        y_exit = wall_pt2[1] - object.pos[1]
    else:
        y_entry = wall_pt2[1] - object.pos[1]
        y_exit = wall_pt1[1]  - (object.pos[1] + object.height / asset_size)

    if vector[0] == 0:
        if ((object.pos[0] + object.width / asset_size) <= wall_pt1[0]) or (object.pos[0] >= wall_pt2[0]):
            near_x = np.inf
            far_x = np.inf
        else:
            near_x = -np.inf
            far_x = np.inf
    else:
        near_x = x_entry / (vector[0] * dt)
        far_x = x_exit / (vector[0] * dt)

    if vector[1] == 0:
        if y_entry <= 0 or y_exit >= 0:
            near_y = np.inf
            far_y = np.inf
        else:
            near_y = -np.inf
            far_y = np.inf
    else:
        near_y = y_entry / (vector[1] * dt)
        far_y = y_exit / (vector[1] * dt)

    entry_time = max(near_x, near_y)
    exit_time = min(far_x, far_y)

    # no collision
    if entry_time > exit_time or (near_x < 0 and near_y < 0) or near_x > 1 or near_y > 1:
        return 1, 0, 0
    else:
        if near_x > near_y:
            if x_entry < 0:
                normalx = -1
                normaly = 0
            else:
                normalx = 1
                normaly = 0
        else:
            if y_entry < 0:
                normalx = 0
                normaly = -1
            else:
                normalx = 0
                normaly = 1
        return entry_time, normalx, normaly

# For animation direction
def get_direction(angle):
    if angle <= -112.5 and angle > -157.5:
        return 'northwest'
    elif angle <= -67.5 and angle > -112.5:
        return 'north'
    elif angle <= -22.5 and angle > -67.5:
        return 'northeast'
    # Returns false on angle 0
    # elif angle == 0:
    #     return False
    elif angle <= 22.5 and angle > -22.5:
        return 'east'
    elif angle <= 67.5 and angle > 22.5:
        return 'southeast'
    elif angle <= 112.5 and angle > 67.5:
        return 'south'
    elif angle <= 157.5 and angle > 112.5:
        return 'southwest'
    elif (angle <= -157.5 or angle > 157.5):
        return 'west'

# Needed for OpenGL functions
def rgb_to_float(r,g,b):
    r = r / 255
    g = g / 255
    b = b / 255
    return r,g,b
# Classes ---------------------------------------------------------------------#
class Search:
    def __init__(self, entity, target, grid):
        self.start = (int(entity.path_point_y),int(entity.path_point_x))
        if target == None:
            self.target = (0,0)
        self.target = (int(target.pos[1]), int(target.pos[0]))
        self.grid = grid
        self.row_max = len(self.grid) - 2
        self.col_max = len(self.grid[0]) - 2

    def get_neighbors(self, cell):
        diag_cost = 1.41
        neighbors = []
        left_n = [(cell[0], cell[1] - 1), 1]
        right_n = [(cell[0], cell[1] + 1), 1]
        up_n = [(cell[0] - 1, cell[1]), 1]
        down_n = [(cell[0] + 1, cell[1]), 1]
        # diagonals
        lu_n =  [(cell[0] - 1, cell[1] - 1), diag_cost]
        ru_n = [(cell[0] - 1, cell[1] + 1), diag_cost]
        ld_n = [(cell[0] + 1, cell[1] - 1), diag_cost]
        rd_n = [(cell[0] + 1, cell[1] + 1), diag_cost]

        if cell[1] >= 1 and not self.grid[left_n[0][0]][left_n[0][1]]: # left
            neighbors.append(left_n)
        if cell[1] <= (self.col_max) and not self.grid[right_n[0][0]][right_n[0][1]]: # right
            neighbors.append(right_n)
        if cell[0] >= 1 and not self.grid[up_n[0][0]][up_n[0][1]]: # up
            neighbors.append(up_n)
        if cell[0] <= (self.row_max) and not self.grid[down_n[0][0]][down_n[0][1]]: # down
            neighbors.append(down_n)

        if cell[1] >= 1 and cell[0] >= 1 and not self.grid[lu_n[0][0]][lu_n[0][1]] and not self.grid[left_n[0][0]][left_n[0][1]] and not self.grid[up_n[0][0]][up_n[0][1]]: # left up
            neighbors.append(lu_n)
        if cell[1] <= (self.col_max) and cell[0] >= 1 and not self.grid[ru_n[0][0]][ru_n[0][1]] and not self.grid[right_n[0][0]][right_n[0][1]] and not self.grid[up_n[0][0]][up_n[0][1]]: # right up
            neighbors.append(ru_n)
        if cell[1] >= 1 and cell[0] <= (self.row_max) and not self.grid[ld_n[0][0]][ld_n[0][1]] and not self.grid[left_n[0][0]][left_n[0][1]] and not self.grid[down_n[0][0]][down_n[0][1]]: # left down
            neighbors.append(ld_n)
        if cell[1] <= (self.col_max) and cell[0] <= (self.row_max) and not self.grid[rd_n[0][0]][rd_n[0][1]] and not self.grid[right_n[0][0]][right_n[0][1]] and not self.grid[down_n[0][0]][down_n[0][1]]: # right down
            neighbors.append(rd_n)
        return neighbors

    def get_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        return path

    def algo(self):
        if self.start == None or self.target == None:
            return []
        count = 0
        open_set = PriorityQueue()
        open_set.put((0, count, self.start))
        came_from = {}
        g_score = {}
        f_score = {}
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                g_score[(r, c)] = float("inf")
                f_score[(r, c)] = float("inf")
        g_score[self.start] = 0
        f_score[self.start] = man_distance(self.start, self.target)

        open_set_hash = {self.start}
        while not open_set.empty():
            current = open_set.get()[2]
            if current == self.target:
                return self.get_path(came_from, current)

            for neighbor in self.get_neighbors(current):
                temp_g_score = g_score[current] + neighbor[1]

                if temp_g_score < g_score[neighbor[0]]:
                    came_from[neighbor[0]] = current
                    g_score[neighbor[0]] = temp_g_score
                    f_score[neighbor[0]] = temp_g_score + man_distance(neighbor[0], self.target)
                    if neighbor[0] not in open_set_hash:
                        count += 1
                        open_set.put((f_score[neighbor[0]], count, neighbor[0]))
                        open_set_hash.add(neighbor[0])
        print('Start: ' + str(self.start))
        print('End: ' + str(self.target))
        return False

    # Bidirectional A*, return path isn't working properly, but it's slower in this implementation anyways so I'm not gonna fix it
    def algo2(self):
        count_1 = 0
        count_2 = 0
        open_set_1 = PriorityQueue()
        open_set_2 = PriorityQueue()
        open_set_1.put((0, count_1, self.start))
        open_set_2.put((0, count_2, self.target))
        came_from_1 = {}
        came_from_2 = {}
        g_score = {}
        f_score = {}
        for r,row in enumerate(self.grid):
            for c,col in enumerate(row):
                g_score[(r, c)] = float("inf")
                f_score[(r, c)] = float("inf")
        g_score[self.start] = 0
        f_score[self.start] = man_distance(self.start, self.target)
        g_score[self.target] = 0
        f_score[self.target] = man_distance(self.start, self.target)

        visited_nodes_1 = [self.start]
        visited_nodes_2 = [self.target]

        while not open_set_1.empty() and not open_set_2.empty():
            current_1 = open_set_1.get()[2]
            current_2 = open_set_2.get()[2]




            if current_1 in visited_nodes_2:
                path_1 = self.get_path(came_from_1, current_1)
                path_2 = self.get_path(came_from_2, current_1)
                del path_2[0]
                path_2.reverse()
                return path_2 + path_1

            if current_2 in visited_nodes_1:
                path_1 = self.get_path(came_from_2, current_1)
                path_2 = self.get_path(came_from_1, current_1)
                del path_2[0]
                path_2.reverse()
                return path_2 + path_1


            for neighbor in self.get_neighbors(current_1):
                temp_g_score = g_score[current_1] + neighbor[1]

                if temp_g_score < g_score[neighbor[0]]:
                    came_from_1[neighbor[0]] = current_1
                    g_score[neighbor[0]] = temp_g_score
                    f_score[neighbor[0]] = temp_g_score + man_distance(neighbor[0], self.target)
                    if neighbor[0] not in visited_nodes_1:
                        count_1 += 1
                        open_set_1.put((f_score[neighbor[0]], count_1, neighbor[0]))
                        visited_nodes_1.append(neighbor[0])
                        #print(neighbor[0])
            for neighbor in self.get_neighbors(current_2):
                temp_g_score = g_score[current_2] + neighbor[1]
                if temp_g_score < g_score[neighbor[0]]:
                    came_from_2[neighbor[0]] = current_2
                    g_score[neighbor[0]] = temp_g_score
                    f_score[neighbor[0]] = temp_g_score + man_distance(neighbor[0], self.start)
                    if neighbor[0] not in visited_nodes_2:
                        count_2 += 1
                        open_set_2.put((f_score[neighbor[0]], count_2, neighbor[0]))
                        visited_nodes_2.append(neighbor[0])

        return False


class Window(pg.window.Window):
    def __init__(self, width, height, loc, vsync = True):
        super().__init__(vsync)
        self.sorting_list = []
        self.label = pg.text.Label('game')
        self.set_size(width, height)
        self.set_location(loc[0], loc[1])
        #self.set_fullscreen(True)
        self.mouse_pos = [0,0]
        self.mouse_left = False
        self.mouse_right = False

    def on_mouse_motion(self,x,y,dx,dy):
        #self.mouse_pos = [x / asset_size, (grid_screen_height - y - 1) / asset_size]
        self.mouse_pos = invert_iso(x,y)
    def on_mouse_press(self, x, y, button, modifiers):
        if button == 1:
            self.mouse_left = True
        if button == 4:
            self.mouse_right = True

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & mouse.LEFT:
            #self.mouse_pos = [x / asset_size, (grid_screen_height - y - 1) / asset_size]
            self.mouse_pos = invert_iso(x,y)
            self.mouse_left = True
        if buttons & mouse.RIGHT:
            #self.mouse_pos = [x / asset_size, (grid_screen_height - y - 1) / asset_size]
            self.mouse_pos = invert_iso(x,y)
            self.mouse_right = True
    def on_mouse_release(self, x, y, button, modifiers):
        if button == 1:
            self.mouse_left = False
        if button == 4:
            self.mouse_right = False



class Entity:
    def __init__(self, image, animation, grid_image, x, y, z, map, speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 6):
        self.image = image
        self.animation = animation
        self.grid_image = grid_image
        self.map = map
        # Vectors
        self.pos = [x, y]
        self.cen = [x + self.image.width / 2, y - self.image.height / 2]
        self.spawn = [x, y]
        self.vel = [0, 0]
        self.acc = [0, 0]
        self.dash_vector = [0, 0]
        self.grid_pos = [(self.pos[0] * asset_size),
                                    (grid_screen_height - (self.pos[1] * asset_size))]
        self.iso = iso_coords(x, y, z)
        # Variables
        self.flower_val = 0
        self.flower_adj = 0.10
        self.parent = None
        self.z = z
        self.angle = 0
        self.charge = 0
        self.proj_speed = proj_speed
        self.fire_rate = fire_rate
        self.speed = speed
        self.accel = accel
        self.hp = hp
        self.dash_mult = 1
        # Sprite
        self.sprite = pg.sprite.Sprite(img = self.image, x = self.iso[0], y = self.iso[1] + (self.iso[2] / 2))
        self.grid_sprite = pg.sprite.Sprite(img = self.grid_image, x = self.grid_pos[0], y = self.grid_pos[1],
                                            batch = grid_batch, group = back_wall_group)
        self.sprite.update(scale = scale)
        self.width = int(self.grid_sprite.width)
        self.height = int(self.grid_sprite.height)
        # States
        self.dead = False
        self.proj_ready = True
        self.intangible = False
        self.charge_ready = False
        self.walk_state = False
        self.stand_state = False

        self.children = []
        self.collisions_list = []

    def check_wall_collisions(self, dt):
        self.collisions_list = []
        for wall in blockbuilder.rect_list:
            time, normx, normy = collision_time2(dt, self, wall, self.vel)
            dot = 1
            if time < 1:
                remaining_time = 1 - time
                dot = (self.vel[0] * normy + self.vel[1] * normx) * remaining_time
                vel = [dot * normy, dot * normx]
                self.collisions_list.append([time, normx, normy, vel, wall])
        return self.collisions_list

    def resolve_wall_collisions(self, dt):
        if len(self.collisions_list) == 0:
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
        elif len(self.collisions_list) == 1:
            self.pos[0] += self.vel[0] * dt * self.collisions_list[0][0]
            self.pos[1] += self.vel[1] * dt * self.collisions_list[0][0]
            self.vel = self.collisions_list[0][3]
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
        else:
            # this block is for dealing with the scenario of the velocity intersecting with two walls.
            # This happens sometimes when they are in line with eachother and thats a no no.
            sorted_collisions = sorted(self.collisions_list, key = lambda x: x[0])
            if (self.vel[0] < 0 and self.vel[1] < 0) or (self.vel[0] < 0 and self.vel[1] > 0):
                # this next if statement is a bit of a mess, but its checking if the wall's pt 2 x's are the same
                if sorted_collisions[0][4][1][0] == sorted_collisions[1][4][1][0]:
                    self.pos[0] += self.vel[0] * dt * sorted_collisions[0][0]
                    self.pos[1] += self.vel[1] * dt * sorted_collisions[0][0]
                    self.vel = sorted_collisions[0][3]
                    self.pos[0] += self.vel[0] * dt
                    self.pos[1] += self.vel[1] * dt
                else:
                    pass

            if (self.vel[0] > 0 and self.vel[1] < 0) or (self.vel[0] > 0 and self.vel[1] > 0):
                # checks if the wall's pt 1 x's are the same
                if sorted_collisions[0][4][0][0] == sorted_collisions[1][4][0][0]:
                    self.pos[0] += self.vel[0] * dt * sorted_collisions[0][0]
                    self.pos[1] += self.vel[1] * dt * sorted_collisions[0][0]
                    self.vel = sorted_collisions[0][3]
                    self.pos[0] += self.vel[0] * dt
                    self.pos[1] += self.vel[1] * dt
                else:
                    pass


    def finalize_update(self, dt):

        self.grid_pos[0] = self.pos[0] * asset_size
        self.grid_pos[1] = self.pos[1] * asset_size

        # Set entity position in grid
        self.grid_sprite.x = self.grid_pos[0]
        self.grid_sprite.y = grid_screen_height - (self.grid_pos[1])

        # set entity position in isometric space
        self.iso = iso_coords((self.pos[0] - camera_movement[0]), (self.pos[1] - camera_movement[1]), self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + (self.iso[2] / 2)

    def post_wall_update(self, dt):
        self.check_wall_collisions(dt)
        self.resolve_wall_collisions(dt)
        self.get_state()
        self.set_animation()
        self.finalize_update(dt)

    def collides(self, other):
        if type(other) == type(self) or type(other) == type(self.parent):
            return False
        else:
            self.x1, self.y1 = self.pos
            self.x2, self.y2 = [(self.pos[0] + (self.grid_sprite.width / asset_size)),
                                (self.pos[1] + (self.grid_sprite.height / asset_size))]
            other.x1, other.y1 = other.pos
            other.x2, other.y2 = [(other.pos[0] + (other.grid_sprite.width / asset_size)),
                                  (other.pos[1] + (other.grid_sprite.height / asset_size))]
            if self.x2 <= other.x1 or self.x1 >= other.x2 or self.y2 <= other.y1 or self.y1 >= other.y2:
                return False
            else:
                return True

    def fire_flower(self,img, angle, speed, offset):
        angle = angle
        proj_x = (self.pos[0]) + np.cos(angle) * offset
        proj_y = (self.pos[1]) + np.sin(angle) * offset
        proj_dx = np.cos(angle) * speed * 5
        proj_dy = np.sin(angle) * speed * 5

        new_proj = Projectile(img, None, enemy_bullet, proj_x, proj_y, self.z,
                              self.map, self, vel = [proj_dx, proj_dy])
        self.children.append(new_proj)

    def flower(self, bullet_img):
        if self.proj_ready:
            for bullet_angle in range(0,4):
                angle = bullet_angle * 1.5707
                self.fire_flower(bullet_img, angle + (self.flower_val), 0.1, 1.5)
                self.fire_flower(bullet_img, angle + (self.flower_val), 0.5, 3)

            self.flower_val += self.flower_adj
            self.proj_ready = False
            pg.clock.schedule_once(self.proj_prep, self.fire_rate)

    def delete(self):
        self.sprite.delete()
        self.grid_sprite.delete()
        ent_list.remove(self)

    def proj_prep(self, dt):
        self.proj_ready = True

    def get_state(self):
        if self.vel == [0,0]:
            self.stand_state = True
            self.walk_state = False
        else:
            self.stand_state = False
            self.walk_state = True
            self.angle = np.arctan2(self.vel[1],self.vel[0])

    def set_animation(self):
        self.direction = get_direction(np.degrees(self.angle))
        if self.walk_state:
            if self.sprite.image != self.animation['walk_'+self.direction]:
                self.sprite.image = self.animation['walk_'+self.direction]
        elif self.stand_state:
            if self.sprite.image != self.animation['base_'+self.direction]:
                self.sprite.image = self.animation['base_'+self.direction]



class Player(Entity):
    def __init__(self, image, animation, grid_image, x, y, z, map,
                 speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 6):
        super().__init__(image, animation, grid_image, x, y, z, map, speed, accel, proj_speed, fire_rate, hp)
        self.keys = key.KeyStateHandler()
        # Vectors
        self.mouse_pos = [0,0]
        self.dash_vector = [0,0]
        # Variables
        self.hp = hp
        self.life_display = player_lives(self.grid_image, self.hp)
        self.sprite = pg.sprite.Sprite(img = self.animation['base_east'], x = self.iso[0], y = self.iso[1] + (self.iso[2] / 2))
        self.sprite.update(scale = scale)
        # States
        self.mvmt_ready = True
        self.action_state = True
        self.debug = False
        # Cooldowns
        self.mvmt_cd = 1/2
        p_list.append(self)
        ent_list.append(self)

    def update(self, dt):

        # Player inputs
        if self.keys[key.SPACE]:
            if self.mvmt_ready:
                self.mvmt_ready = False
                #self.action_state = False
                self.dash_vector = [self.vel[0], self.vel[1]]

                self.invincible(dt)
                # These lines set the dash to last 5 frames
                self.dash(dt, multiplier = 4)
                pg.clock.schedule_once(self.dash, 1/60, multiplier = 3)
                pg.clock.schedule_once(self.dash, 2/60, multiplier = 3)
                pg.clock.schedule_once(self.dash, 3/60, multiplier = 2)
                pg.clock.schedule_once(self.dash, 4/60, multiplier = 2)
                pg.clock.schedule_once(self.dash, 5/60, multiplier = 1)
                pg.clock.schedule_once(self.dash, 6/60, multiplier = 1)




                # Schedule resets
                pg.clock.schedule_once(self.mvmt_cd_reset, self.mvmt_cd)
                pg.clock.schedule_once(self.action_state_reset, 16/60)
                pg.clock.schedule_once(self.intangible_reset, 16/60)
                pg.clock.schedule_once(self.dash_vec_reset, 16/60)


        if self.mouse_left and self.action_state:
            if self.proj_ready:
                #self.flower(p_bullet_temp2)
                self.fire(p_bullet_temp2, player_bullet, self.pos, 1, dam = 1)
                self.proj_ready = False
                pg.clock.schedule_once(self.proj_prep, self.fire_rate)
            else:
                pass

        if self.mouse_right and self.action_state:
            if self.charge >= 5:
                self.fire(p_charge_bullet, charge_bullet, self.pos, 0.5, dam = 10)
                self.charge = 0
                pg.clock.schedule_once(self.proj_prep, self.fire_rate)

        if self.keys[key.Y] and self.action_state:
            self.debug = True
        else:
            self.debug = False

        if self.keys[key.W] and not self.keys[key.S] and self.action_state:
            self.acc[1] = -self.accel
        elif self.keys[key.S] and not self.keys[key.W]and self.action_state:
            self.acc[1] = self.accel
        else:
            self.acc[1] = 0
            self.vel[1] = 0

        if self.keys[key.A] and not self.keys[key.D] and self.action_state:
            self.acc[0] = -self.accel
        elif self.keys[key.D]and not self.keys[key.A] and self.action_state:
            self.acc[0] = self.accel
        else:
            self.acc[0] = 0
            self.vel[0] = 0

        # Acceleration
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]

        # This should limit any vector into the length of self.speed
        if (self.vel[0] ** 2 + self.vel[1] ** 2) > self.speed ** 2:
            scale_down = self.speed / np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
            self.vel = [self.vel[0] * scale_down, self.vel[1] * scale_down]

        self.vel[0] = self.vel[0] * self.dash_mult
        self.vel[1] = self.vel[1] * self.dash_mult

    def fire(self, image, hitbox, origin, speed_multiplier, dam = 10):
        angle = np.arctan2(self.mouse_pos[1] - self.pos[1], self.mouse_pos[0] - self.pos[0])
        proj_x = (origin[0]) + np.cos(self.angle) * 0.5
        proj_y = (origin[1]) + np.sin(self.angle) * 0.5

        proj_dx = np.cos(angle) * self.proj_speed * speed_multiplier
        proj_dy = np.sin(angle) * self.proj_speed * speed_multiplier


        new_proj = Projectile(image, None, hitbox, proj_x, proj_y, self.z, self.map, self, vel = [proj_dx, proj_dy], damage = dam, accel = 0.04)
        self.children.append(new_proj)

    def dash(self, dt, multiplier):
        self.dash_mult = multiplier

    def handle_collision(self, dt):
        if self.hp > 1:
            self.hp -= 1
            self.life_display = player_lives(self.grid_image, self.hp)
            self.invincible(dt)
            pg.clock.schedule_once(self.intangible_reset, 1)
        else:
            self.hp -= 1
            self.life_display = player_lives(self.grid_image, self.hp)
            self.dead = True


    def invincible(self, dt):
        self.intangible = True
        self.grid_sprite.opacity = 155
        self.sprite.opacity = 155

    def delete(self):
        super().delete()
        p_list.remove(self)

    # Reset methods

    def mvmt_cd_reset(self, dt):
        self.mvmt_ready = True
    def action_state_reset(self, dt):
        self.action_state = True
    def intangible_reset(self, dt):
        self.intangible = False
        self.grid_sprite.opacity = 255
        self.sprite.opacity = 255
    def dash_vec_reset(self, dt):
        self.dash_vector = [0,0]

class Enemy(Entity):
    def __init__(self, image, animation, grid_image, x, y, z, map,
                 speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 100):
        super().__init__(image, animation, grid_image, x, y, z, map, speed, accel, proj_speed, fire_rate, hp)
        self.target = None
        self.path_point_x = self.pos[0]
        self.path_point_y = self.pos[1]

        e_list.append(self)
        ent_list.append(self)

    def delete(self):
        super().delete()
        e_list.remove(self)

    def fire(self):
        angle = np.arctan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])
        proj_x = (self.pos[0])+ np.cos(angle) * 0.5
        proj_y = (self.pos[1])+ np.sin(angle) * 0.5

        proj_dx = np.cos(angle) * self.proj_speed
        proj_dy = np.sin(angle) * self.proj_speed


        new_proj = Projectile(e_bullet_temp, None, enemy_bullet, proj_x, proj_y, self.z, self.map, self, vel = [proj_dx, proj_dy])

        self.children.append(new_proj)

    def update(self, dt):
        if self.proj_ready and self.target != None:
            self.vel = [0,0]
            self.fire()
            self.proj_ready = False
            pg.clock.schedule_once(self.proj_prep, self.fire_rate)

        if self.target != None and distance(self.pos, self.target.pos) >= -5:
            self.move_towards_target()


            # Acceleration
            self.vel[0] += self.acc[0]
            self.vel[1] += self.acc[1]

            # This should limit any vector into the length of self.speed
            if (self.vel[0] ** 2 + self.vel[1] ** 2) > self.speed ** 2:
                scale_down = self.speed / np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
                self.vel = [self.vel[0] * scale_down, self.vel[1] * scale_down]



    def move_towards_target(self):
        # Fire up A*
        self.search = Search(self, self.target, self.map)
        path = self.search.algo()
        print(path)
        self.angle = np.arctan2(path[-2][0] - path[-1][0], path[-2][1] - path[-1][1])
        self.acc[0] = np.cos(self.angle) * self.speed
        self.acc[1] = np.sin(self.angle) * self.speed

        # This sets the input for the next time A* is called, based on the direction of the last move determines what point on the entity is important to pass in
        if self.acc[0] < 0:
            self.path_point_x = self.pos[0] + self.grid_sprite.width / asset_size
        else:
            self.path_point_x = self.pos[0]
        if self.acc[1] < 0:
            self.path_point_y = self.pos[1] + self.grid_sprite.height / asset_size
        else:
            self.path_point_y = self.pos[1]
        self.angle = np.degrees(self.angle)


    def handle_collision(self, dt, damage):
        if self.hp > 1:
            self.hp -= damage
            if self.hp < 1:
                self.dead = True
        else:
            self.dead = True


class Tile(Entity):
    def __init__(self, image, animation, grid_image, x, y, z,
                 speed = 1, bat = None, grp = None, grid_grp = grid_entity_group):
        super().__init__(image, animation, grid_image, x, y, z, speed)
        self.sprite = pg.sprite.Sprite(img = self.image, x = self.iso[0], y = self.iso[1] + (self.iso[2] / 2),
                                       batch = bat, group = grp)
        self.sprite.update(scale = scale)
        self.grid_sprite = pg.sprite.Sprite(img = self.grid_image, x = self.grid_pos[0], y = self.grid_pos[1],
                                            batch = grid_batch, group = grid_grp)
        tile_update_list.append(self)

    def update_pos(self, dt):
        self.iso = iso_coords(self.pos[0] - camera_movement[0], self.pos[1] - camera_movement[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + (self.iso[2] / 2)


class Projectile(Entity):
    def __init__(self, image, animation, grid_image, x, y, z, map, parent, speed = 1, accel = 1,
                 lifespan = 3, vel = [0, 0], damage = 1, coll_behaviour = 'die', decel = False):
        super().__init__(image, animation, grid_image, x, y, z, map, speed, accel)
        self.vel = vel
        self.lifespan = lifespan
        self.parent = parent
        self.damage = damage
        self.sprite.update(scale = scale / 2)
        pg.clock.schedule_once(self.die, self.lifespan)
        self.coll_behaviour = coll_behaviour
        self.decel = decel

    def die(self, dt):
        self.dead = True

    def delete(self):
        super().delete()
        if type(self.parent) == Player:
            player_bullets.remove(self)
        if type(self.parent) == Enemy:
            enemy_bullets.remove(self)



    def update(self, dt):
        if self.decel:
            if self.vel[0] > 0:
                self.acc[0] = -self.accel * self.vel[0]
            elif self.vel[0] < 0:
                self.acc[0] = self.accel * -self.vel[0]
            else:
                self.acc[0] = 0

            if self.vel[1] > 0:
                self.acc[1] = -self.accel * self.vel[1]
            elif self.vel[1] < 0:
                self.acc[1] = self.accel * -self.vel[1]
            else:
                self.acc[1] = 0
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[1]

    def resolve_wall_collisions_slide(self, dt):
        if len(self.collisions_list) == 0:
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
        elif len(self.collisions_list) == 1:
            self.pos[0] += self.vel[0] * dt * self.collisions_list[0][0]
            self.pos[1] += self.vel[1] * dt * self.collisions_list[0][0]
            self.vel = self.collisions_list[0][3]
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
        else:
            # this block is for dealing with the scenario of the velocity intersecting with two walls.
            # This happens sometimes when they are in line with eachother and thats a no no.
            sorted_collisions = sorted(self.collisions_list, key = lambda x: x[0])
            if (self.vel[0] < 0 and self.vel[1] < 0) or (self.vel[0] < 0 and self.vel[1] > 0):
                # this next if statement is a bit of a mess, but its checking if the wall's pt 2 x's are the same
                if sorted_collisions[0][4][1][0] == sorted_collisions[1][4][1][0]:
                    self.pos[0] += self.vel[0] * dt * sorted_collisions[0][0]
                    self.pos[1] += self.vel[1] * dt * sorted_collisions[0][0]
                    self.vel = sorted_collisions[0][3]
                    self.pos[0] += self.vel[0] * dt
                    self.pos[1] += self.vel[1] * dt
                else:
                    pass

            if (self.vel[0] > 0 and self.vel[1] < 0) or (self.vel[0] > 0 and self.vel[1] > 0):
                # checks if the wall's pt 1 x's are the same
                if sorted_collisions[0][4][0][0] == sorted_collisions[1][4][0][0]:
                    self.pos[0] += self.vel[0] * dt * sorted_collisions[0][0]
                    self.pos[1] += self.vel[1] * dt * sorted_collisions[0][0]
                    self.vel = sorted_collisions[0][3]
                    self.pos[0] += self.vel[0] * dt
                    self.pos[1] += self.vel[1] * dt
                else:
                    pass

    def resolve_wall_collisions_bounce(self, dt):
        if len(self.collisions_list) == 0:
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
        elif len(self.collisions_list) == 1:
            self.pos[0] += self.vel[0] * dt * self.collisions_list[0][0]
            self.pos[1] += self.vel[1] * dt * self.collisions_list[0][0]
            if abs(self.collisions_list[0][1]) > 0:
                self.vel[0] = -self.vel[0]
            if abs(self.collisions_list[0][2]) > 0:
                self.vel[1] = -self.vel[1]
        else:
            # this block is for dealing with the scenario of the velocity intersecting with two walls.
            # This happens sometimes when they are in line with eachother and thats a no no.
            sorted_collisions = sorted(self.collisions_list, key = lambda x: x[0])
            if abs(sorted_collisions[0][1]) > 0:
                self.vel[0] = -self.vel[0]
            if abs(sorted_collisions[0][2]) > 0:
                self.vel[1] = -self.vel[1]

    def resolve_wall_collisions_die(self, dt):
        if len(self.collisions_list) == 0:
            self.pos[0] += self.vel[0] * dt
            self.pos[1] += self.vel[1] * dt
        elif len(self.collisions_list) > 0:
            self.dead = True

    def post_wall_update(self, dt):
        self.check_wall_collisions(dt)
        if self.coll_behaviour == 'bounce':
            self.resolve_wall_collisions_bounce(dt)
        elif self.coll_behaviour == 'slide':
            self.resolve_wall_collisions_slide(dt)
        elif self.coll_behaviour == 'die':
            self.resolve_wall_collisions_die(dt)
        self.finalize_update(dt)


    def handle_collision(self, other):
            self.parent.charge += 1
            self.dead = True
