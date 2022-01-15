# Import Libraries and Modules ------------------------------------------------#
import pyglet as pg
import numpy as np
import threading
from pyglet.window import key, mouse

from variables import *
from assets import *
import blockbuilder

# Functions -------------------------------------------------------------------#

def build_grid(mapdata):
    for y,row in enumerate(mapdata):
        for x,tile in enumerate(row):
            if tile and x == 0 or y == 0:
                tile = Tile(purple_cube, grid_tile, x, y, 1, bat = back_batch)
                batched_wall_list.append(tile)
            elif tile and x == (len(mapdata) -1) or y == (len(mapdata) -1):
                tile = Tile(purple_cube, grid_tile, x, y, 1, bat = front_batch)
                batched_wall_list.append(tile)
            elif tile:
                tile = Tile(purple_cube, grid_tile, x, y, 1)
                wall_list.append(tile)


def player_lives(image, num_lives):
    player_lives = []
    for i in range(num_lives):
        x = (grid_screen_width - 80) - (20*i)
        y = (grid_screen_height - 40)
        new_sprite = pg.sprite.Sprite(img = image, x = x, y = y, batch = grid_batch)
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
    iso_y = screen_height - iso_y
    xyz = [iso_x, iso_y, -z]
    return xyz

def get_pos_dim_vel(entity):
    pos = entity.pos
    dim = [entity.width, entity.height]
    vel = entity.vel
    e_pos_dim_vel.append([pos, dim, vel])

def invert_iso(x,y):
    coord_vec = np.array([[x + (asset_size / 2) - (screen_width / 2)],
                          [screen_height - y]])
    grid_transform = np.linalg.inv(np.array([[0.5 * asset_size * scale, -0.5 * asset_size * scale],
                                       [0.25 * asset_size * scale, 0.25 * asset_size * scale]]))
    xy_transform = np.dot(grid_transform,coord_vec)
    xyz_array = (xy_transform).reshape(2)
    return xyz_array

def collision_time(dt, object, other):
    if object.vel[0] > 0:
        x_entry = other.pos[0] - (object.pos[0]  + object.width / asset_size)
        x_exit = (other.pos[0]  + other.width / asset_size) - object.pos[0]
    else:
        x_entry = (other.pos[0]  + other.width / asset_size) - object.pos[0]
        x_exit = other.pos[0] - (object.pos[0]  + object.width / asset_size)
    if object.vel[1] > 0:
        y_entry = other.pos[1] - (object.pos[1] + object.height / asset_size)
        y_exit = (other.pos[1]  + other.height / asset_size) - object.pos[1]
    else:
        y_entry = (other.pos[1] + other.height / asset_size) - object.pos[1]
        y_exit = other.pos[1]  - (object.pos[1] + object.height / asset_size)

    if object.vel[0] == 0:
        if ((object.pos[0] + object.width / asset_size) < other.pos[0]) or (object.pos[0] > (other.pos[0] + other.width / asset_size)):
            near_x = np.inf
            far_x = np.inf
        else:
            near_x = -np.inf
            far_x = np.inf
    else:
        near_x = x_entry / (object.vel[0] * dt)
        far_x = x_exit / (object.vel[0] * dt)

    if object.vel[1] == 0:
        if y_entry < 0 or y_exit > 0:
            near_y = np.inf
            far_y = np.inf
        else:
            near_y = -np.inf
            far_y = np.inf
    else:
        near_y = y_entry / (object.vel[1] * dt)
        far_y = y_exit / (object.vel[1] * dt)

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
        if ((object.pos[0] + object.width / asset_size) < wall_pt1[0]) or (object.pos[0] > wall_pt2[0]):
            near_x = np.inf
            far_x = np.inf
        else:
            near_x = -np.inf
            far_x = np.inf
    else:
        near_x = x_entry / (vector[0] * dt)
        far_x = x_exit / (vector[0] * dt)

    if vector[1] == 0:
        if y_entry < 0 or y_exit > 0:
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


# Classes ---------------------------------------------------------------------#

class Window(pg.window.Window):
    def __init__(self, width, height, loc, vsync = True):
        super().__init__(vsync)
        self.sorting_list = []
        self.label = pg.text.Label('game')
        self.set_size(width, height)
        self.set_location(loc[0], loc[1])
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
    def __init__(self, image, grid_image, x, y, z, speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 6):
        self.image = image
        self.grid_image = grid_image
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
        self.parent = None
        self.z = z
        self.charge = 0
        self.proj_speed = proj_speed
        self.fire_rate = fire_rate
        self.speed = speed
        self.accel = accel
        self.hp = hp
        self.dash_mult = 1
        # Sprite
        self.sprite = pg.sprite.Sprite(img = self.image, x = self.iso[0], y = self.iso[1] + self.iso[2], batch = batch)
        self.grid_sprite = pg.sprite.Sprite(img = self.grid_image, x = self.grid_pos[0], y = self.grid_pos[1], batch = grid_batch)
        self.sprite.update(scale = scale)
        self.width = int(self.grid_sprite.width)
        self.height = int(self.grid_sprite.height)
        # States
        self.dead = False
        self.proj_ready = True
        self.intangible = False
        self.charge_ready = False

        self.children = []
        self.collisions_list = []

    def update(self, dt):
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[0]
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + self.iso[2]

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
        self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + self.iso[2]

    def post_wall_update(self, dt):
        self.check_wall_collisions(dt)
        self.resolve_wall_collisions(dt)
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

    # def handle_wall_collision_y(self, wall):
    #     if self.y1 < wall.y2 and (self.vel[1] < 0 or self.dash_vector[1] < 0):
    #         self.pos[1] = wall.y2
    #     elif self.y2 > wall.y1 and (self.vel[1] > 0 or self.dash_vector[1] > 0):
    #         self.pos[1] = wall.y1 - (self.grid_image.height / asset_size)
    #
    # def handle_wall_collision_x(self, wall):
    #     if self.x1 < wall.x2 and (self.vel[0] < 0 or self.dash_vector[0] < 0):
    #         self.pos[0] = wall.x2
    #     elif self.x2 > wall.x1 and (self.vel[0] > 0 or self.dash_vector[0] > 0):
    #         self.pos[0] = wall.x1 - (self.grid_image.height / asset_size)

    def delete(self):
        self.sprite.delete()
        self.grid_sprite.delete()
        ent_list.remove(self)

    def proj_prep(self, dt):
        self.proj_ready = True



class Player(Entity):
    def __init__(self, image, grid_image, x, y, z,
                 speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 6):
        super().__init__(image, grid_image, x, y, z, speed, accel, proj_speed, fire_rate, hp)
        self.keys = key.KeyStateHandler()
        # Vectors
        self.mouse_pos = [0,0]
        self.dash_vector = [0,0]
        # Variables
        self.hp = hp
        self.life_display = player_lives(self.grid_image, self.hp)
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
                self.fire(p_bullet_temp, player_bullet, self.pos, 1, dam = 1)
                self.proj_ready = False
                pg.clock.schedule_once(self.proj_prep, self.fire_rate)

        if self.mouse_right and self.action_state:
            if self.charge >= 5:
                self.fire(p_bullet_temp, charge_bullet, self.pos, 0.5, dam = 100)
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



        # Checking for collisions with swept

        # self.grid_pos[0] = self.pos[0] * asset_size
        # self.grid_pos[1] = self.pos[1] * asset_size
        #
        # # Set entity position in grid
        # self.grid_sprite.x = self.grid_pos[0]
        # self.grid_sprite.y = grid_screen_height - (self.grid_pos[1])
        #
        # # set entity position in isometric space
        # self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
        # self.sprite.x = self.iso[0]
        # self.sprite.y = self.iso[1] + self.iso[2]


    def fire(self, image, hitbox, origin, speed_multiplier, dam = 1):
        angle = np.arctan2(self.mouse_pos[1] - self.pos[1], self.mouse_pos[0] - self.pos[0])
        proj_x = (origin[0]) + np.cos(angle) * 0.5
        proj_y = (origin[1])+ np.sin(angle) * 0.5

        proj_dx = np.cos(angle) * self.proj_speed * speed_multiplier
        proj_dy = np.sin(angle) * self.proj_speed * speed_multiplier


        new_proj = Projectile(image, hitbox, proj_x, proj_y, self.z, self, vel = [proj_dx, proj_dy], damage = dam)
        self.children.append(new_proj)

    def dash(self, dt, multiplier):
        self.dash_mult = multiplier
        # dash_vec = [(self.vel[0] * multiplier / asset_size),
        #             (self.vel[1] * multiplier / asset_size)]
        # self.pos[0] += dash_vec[0]
        # self.pos[1] += dash_vec[1]


        #
        #
        # self.pos = [self.pos[0] + (self.vel[0] * multiplier / asset_size),
        #             self.pos[1] + (self.vel[1] * multiplier / asset_size)]

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
    def __init__(self, image, grid_image, x, y, z,
                 speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 100):
        super().__init__(image, grid_image, x, y, z, speed, accel, proj_speed, fire_rate, hp)
        self.target = None
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


        new_proj = Projectile(enemy_bullet, enemy_bullet, proj_x, proj_y, self.z, self, vel = [proj_dx, proj_dy])
        self.children.append(new_proj)

    def update(self, dt):
        if self.proj_ready and self.target != None:
            self.fire()
            self.proj_ready = False
            pg.clock.schedule_once(self.proj_prep, self.fire_rate)

        if self.target != None and distance(self.pos, self.target.pos) >= -1:
            self.move_towards_target()

            # Acceleration
            self.vel[0] += self.acc[0]
            self.vel[1] += self.acc[1]

            # This should limit any vector into the length of self.speed
            if (self.vel[0] ** 2 + self.vel[1] ** 2) > self.speed ** 2:
                scale_down = self.speed / np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
                self.vel = [self.vel[0] * scale_down, self.vel[1] * scale_down]

            # Adjusting unit's position, handling x and y wall collisions seperately
            # self.pos[0] += self.vel[0] * dt
            # # for wall in wall_list:
            # #     if self.collides(wall):
            # #         self.handle_wall_collision_x(wall)
            # #         self.vel[0] = 0
            # #         self.dash_vector[0] = 0
            # self.pos[1] += self.vel[1] * dt
            # # for wall in wall_list:
            # #     if self.collides(wall):
            # #         self.handle_wall_collision_y(wall)
            # #         self.vel[1] = 0
            # #         self.dash_vector[1] = 0
            #
            # # Set entity position in grid
            # self.grid_sprite.x = self.pos[0] * asset_size
            # self.grid_sprite.y = grid_screen_height - (self.pos[1] * asset_size)
            #
            # # set entity position in isometric space
            # self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
            # self.sprite.x = self.iso[0]
            # self.sprite.y = self.iso[1] + self.iso[2]


    def move_towards_target(self):
        angle = np.arctan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])
        self.acc[0] = np.cos(angle) * self.accel
        self.acc[1] = np.sin(angle) * self.accel


    def handle_collision(self, dt, damage):
        if self.hp > 1:
            self.hp -= damage
            if self.hp < 1:
                self.dead = True
        else:
            self.dead = True


class Tile(Entity):
    def __init__(self, image, grid_image, x, y, z, speed = 1, bat = None):
        super().__init__(image, grid_image, x, y, z, speed)
        self.sprite = pg.sprite.Sprite(img = self.image, x = self.iso[0], y = self.iso[1] + self.iso[2], batch = bat)
        self.sprite.update(scale = scale)
        self.grid_sprite = pg.sprite.Sprite(img = self.grid_image, x = self.grid_pos[0], y = self.grid_pos[1], batch = grid_batch)



class Boss(Entity):
    def __init__(self, image, grid_image, x, y, z, speed = 1, accel = 1, proj_speed = 20, fire_rate = 1/10):
        super().__init__(image, grid_image, x, y, z, speed, accel)
        self.proj_speed = proj_speed
        self.proj_ready = True
        self.fire_rate = fire_rate
        self.mouse_pos = [0,0]
        self.bullet_colour = 0
        self.phase_1_val = 0
        self.phase_1_adj = 0.05
        e_list.append(self)

    def update(self, dt):
        super().update(dt)
        self.phase_1()


    def fire(self, angle, speed, colour):
        angle = angle
        proj_x = (self.pos[0]) + np.cos(angle) * 1.6
        proj_y = (self.pos[1]) + np.sin(angle) * 1.6
        proj_dx = np.cos(angle) * speed
        proj_dy = np.sin(angle) * speed

        new_proj = Projectile(enemy_bullet, enemy_bullet, proj_x, proj_y, self.z, self, vel = [proj_dx, proj_dy])
        self.children.append(new_proj)

    def phase_1(self):
        if self.proj_ready:
            self.fire(0 + self.phase_1_val, 4, 0)
            self.fire(1.5707 + self.phase_1_val, 4, 1)
            self.fire(3.1416 + self.phase_1_val, 4, 2)
            self.fire(4.7124 + self.phase_1_val, 4, 3)
            self.fire(0 - self.phase_1_val, 4, 0)
            self.fire(1.5707 - self.phase_1_val, 4, 1)
            self.fire(3.1416 - self.phase_1_val, 4, 2)
            self.fire(4.7124 - self.phase_1_val, 4, 3)

            self.fire(0 + self.phase_1_val, 2, 0)
            self.fire(1.5707 + self.phase_1_val, 2, 1)
            self.fire(3.1416 + self.phase_1_val, 2, 2)
            self.fire(4.7124 + self.phase_1_val, 2, 3)
            self.fire(0 - self.phase_1_val, 2, 0)
            self.fire(1.5707 - self.phase_1_val, 2, 1)
            self.fire(3.1416 - self.phase_1_val, 2, 2)
            self.fire(4.7124 - self.phase_1_val, 2, 3)


            if self.bullet_colour < 3:
                self.bullet_colour += 1
            else:
                self.bullet_colour = 0
            self.phase_1_val += self.phase_1_adj
            self.proj_ready = False
            pg.clock.schedule_once(self.proj_prep, self.fire_rate)



class Projectile(Entity):
    def __init__(self, image, grid_image, x, y, z, parent, speed = 1, accel = 1,
                 lifespan = 3, vel = [0, 0], damage = 1, coll_behaviour = 'bounce'):
        super().__init__(image, grid_image, x, y, z, speed, accel)
        self.vel = vel
        self.lifespan = lifespan
        self.parent = parent
        self.damage = damage
        self.sprite.update(scale = 1)
        pg.clock.schedule_once(self.die, self.lifespan)
        self.coll_behaviour = coll_behaviour

    def die(self, dt):
        self.dead = True

    def delete(self):
        super().delete()
        if type(self.parent) == Player:
            player_bullets.remove(self)
        if type(self.parent) == Enemy or type(self.parent) == Boss:
            enemy_bullets.remove(self)

    def update(self, dt):
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[0]

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

    def post_wall_update(self, dt):
        self.check_wall_collisions(dt)
        if self.coll_behaviour == 'bounce':
            self.resolve_wall_collisions_bounce(dt)
        elif self.coll_behaviour == 'slide':
            self.resolve_wall_collisions_slide(dt)
        self.finalize_update(dt)


    def handle_collision(self, other):
            self.parent.charge += 1
            self.dead = True
