# Import Libraries and Modules ------------------------------------------------#
import pyglet as pg
import numpy as np
import threading
from pyglet.window import key, mouse

from variables import *
from assets import *

# Functions -------------------------------------------------------------------#

def build_grid(mapdata):
    for y,row in enumerate(mapdata):
        for x,tile in enumerate(row):
            if tile:
                tile = Tile(purple_cube, grid_tile, x, y, 1)

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

def iso_coords(x, y, z):
    coord_vec = np.array([[x],
                         [y]])
    grid_transform = np.array([[0.5 * asset_size * scale, -0.5 * asset_size * scale],
                            [0.25 * asset_size * scale, 0.25 * asset_size * scale]])
    xy_transform = np.dot(grid_transform,coord_vec)
    xyz_array = (np.append(xy_transform, -z))
    xyz_array[0] =  (xyz_array[0] - (asset_size / 2)) + (screen_width / 2)
    xyz_array[1] = screen_height - xyz_array[1]
    return xyz_array

def invert_iso(x,y):
    coord_vec = np.array([[x + (asset_size / 2) - (screen_width / 2)],
                          [screen_height - y]])
    grid_transform = np.linalg.inv(np.array([[0.5 * asset_size * scale, -0.5 * asset_size * scale],
                                       [0.25 * asset_size * scale, 0.25 * asset_size * scale]]))
    xy_transform = np.dot(grid_transform,coord_vec)
    xyz_array = (xy_transform).reshape(2)
    return xyz_array



# Classes ---------------------------------------------------------------------#

class Window(pg.window.Window):
    def __init__(self, width, height, loc, vsync = True):
        super().__init__(vsync)
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
        self.iso = iso_coords(x, y, z)
        # Variables
        self.z = z
        self.charge = 0
        self.proj_speed = proj_speed
        self.fire_rate = fire_rate
        self.speed = speed
        self.accel = accel
        self.hp = hp
        self.grid_x, self.grid_y = [(self.pos[0] * asset_size),
                                    (grid_screen_height - (self.pos[1] * asset_size))]
        # Sprite
        self.sprite = pg.sprite.Sprite(img = self.image, x = self.iso[0], y = self.iso[1] + self.iso[2], batch = batch)
        self.grid_sprite = pg.sprite.Sprite(img = self.grid_image, x = self.grid_x, y = self.grid_y, batch = grid_batch)
        self.sprite.update(scale = scale)
        # States
        self.dead = False
        self.proj_ready = True
        self.intangible = False
        self.charge_ready = False

        self.children = []

    def update(self, dt):
        self.vel[0] += self.acc[0]
        self.vel[1] += self.acc[0]
        self.pos[0] += self.vel[0] * dt
        self.pos[1] += self.vel[1] * dt
        #self.grid_sprite.x = self.pos[0] * asset_size
        #self.grid_sprite.y = grid_screen_height - (self.pos[1] * asset_size)
        self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + self.iso[2]

    def collides(self, other):
        if self.vel[0] > 0:
            x_entry = other.pos[0] - (self.pos[0] + self.image.width)
            x_exit = (other.pos[0] + other.image.width) - self.pos[0]
<<<<<<< Updated upstream
        else:
            x_entry = (other.pos[0] + other.image.width) - self.pos[0]
            x_exit = other.pos[0] - (self.pos[0] + self.image.width)
        if self.vel[1] > 0:
            y_entry = other.pos[1] - (self.pos[1] + self.image.height)
            y_exit = (other.pos[1] + other.image.height) - self.pos[1]
        else:
            y_entry = (other.pos[1] + other.image.height) - self.pos[1]
            y_exit = other.pos[1] - (self.pos[1] + self.image.height)

        if self.vel[0] == 0:
            near_x = 100000000
            far_x = -100000000
        else:
=======
        else:
            x_entry = (other.pos[0] + other.image.width) - self.pos[0]
            x_exit = other.pos[0] - (self.pos[0] + self.image.width)
        if self.vel[1] > 0:
            y_entry = other.pos[1] - (self.pos[1] + self.image.height)
            y_exit = (other.pos[1] + other.image.height) - self.pos[1]
        else:
            y_entry = (other.pos[1] + other.image.height) - self.pos[1]
            y_exit = other.pos[1] - (self.pos[1] + self.image.height)

        if self.vel[0] == 0:
            near_x = 100000000
            far_x = -100000000
        else:
>>>>>>> Stashed changes
            near_x = x_entry / self.vel[0]
            far_x = x_exit / self.vel[0]
        if self.vel[1] == 0:
            near_y = 100000000
            far_y = -1000000000
        else:
            near_y = y_entry / self.vel[1]
            far_y = y_exit / self.vel[1]

        if near_x > far_y or near_y > far_x:
            return False

<<<<<<< Updated upstream
<<<<<<< Updated upstream

=======
        t_hit_near = max(near_x, near_y)
        t_hit_far = min(far_x, far_y)

=======
        t_hit_near = max(near_x, near_y)
        t_hit_far = min(far_x, far_y)

>>>>>>> Stashed changes
        if t_hit_far < 0:
            return False
        else:
            print('Near x: ' + str(near_x))
            print('Near y: ' + str(near_x))



    # def collides(self, other):
    #     self.x1, self.y1 = self.pos
    #     self.x2, self.y2 = [(self.pos[0] + (self.grid_sprite.width / asset_size)),
    #                         (self.pos[1] + (self.grid_sprite.height / asset_size))]
    #     other.x1, other.y1 = other.pos
    #     other.x2, other.y2 = [(other.pos[0] + (other.grid_sprite.width / asset_size)),
    #                           (other.pos[1] + (other.grid_sprite.height / asset_size))]
    #     if self.x2 <= other.x1 or self.x1 >= other.x2 or self.y2 <= other.y1 or self.y1 >= other.y2:
    #         return False
    #     else:
    #         return True
<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

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
                self.action_state = False
                self.dash_vector = [self.vel[0], self.vel[1]]

                self.invincible(dt)
                # These lines set the dash to last 5 frames
                self.dash(dt, multiplier = 3)
                pg.clock.schedule_once(self.dash, 1/60, multiplier = 3)
                pg.clock.schedule_once(self.dash, 2/60, multiplier = 2)
                pg.clock.schedule_once(self.dash, 3/60, multiplier = 2)
                pg.clock.schedule_once(self.dash, 4/60, multiplier = 2)
                pg.clock.schedule_once(self.dash, 5/60, multiplier = 2)
                pg.clock.schedule_once(self.dash, 6/60, multiplier = 1)
                pg.clock.schedule_once(self.dash, 7/60, multiplier = 1)
                pg.clock.schedule_once(self.dash, 8/60, multiplier = 1)
                pg.clock.schedule_once(self.dash, 9/60, multiplier = 1)
                pg.clock.schedule_once(self.dash, 10/60, multiplier = 0.5)
                pg.clock.schedule_once(self.dash, 11/60, multiplier = 0.5)

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


        if self.keys[key.W] and self.action_state:
            self.acc[1] = -self.accel
        elif self.keys[key.S] and self.action_state:
            self.acc[1] = self.accel
        else:
            self.acc[1] = 0
            self.vel[1] = 0

        if self.keys[key.A] and self.action_state:
            self.acc[0] = -self.accel
        elif self.keys[key.D] and self.action_state:
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

        # Adjusting player's position, handling x and y wall collisions seperately
        self.pos[0] += self.vel[0] * dt
<<<<<<< Updated upstream
<<<<<<< Updated upstream
        # for wall in wall_list:
        #     if self.collides(wall):
        #         self.handle_wall_collision_x(wall)
        #         self.vel[0] = 0
        #         self.dash_vector[0] = 0
        self.pos[1] += self.vel[1] * dt
        # for wall in wall_list:
        #     if self.collides(wall):
        #         self.handle_wall_collision_y(wall)
        #         self.vel[1] = 0
        #         self.dash_vector[1] = 0
=======
        self.pos[1] += self.vel[1] * dt
=======
        self.pos[1] += self.vel[1] * dt
>>>>>>> Stashed changes





<<<<<<< Updated upstream
>>>>>>> Stashed changes
=======
>>>>>>> Stashed changes

        # Set entity position in grid
        self.grid_sprite.x = self.pos[0] * asset_size
        self.grid_sprite.y = grid_screen_height - (self.pos[1] * asset_size)

        # set entity position in isometric space
        self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + self.iso[2]

    def fire(self, image, hitbox, origin, speed_multiplier, dam = 1):
        angle = np.arctan2(self.mouse_pos[1] - self.pos[1], self.mouse_pos[0] - self.pos[0])
        proj_x = (origin[0]) + np.cos(angle) * 0.5
        proj_y = (origin[1])+ np.sin(angle) * 0.5

        proj_dx = np.cos(angle) * self.proj_speed * speed_multiplier
        proj_dy = np.sin(angle) * self.proj_speed * speed_multiplier


        new_proj = Projectile(image, hitbox, proj_x, proj_y, self.z, self, vel = [proj_dx, proj_dy], damage = dam)
        self.children.append(new_proj)

    def dash(self, dt, multiplier):
        self.pos = [self.pos[0] + (self.dash_vector[0] * multiplier / asset_size),
                    self.pos[1] + (self.dash_vector[1] * multiplier / asset_size)]

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
            self.pos[0] += self.vel[0] * dt
            # for wall in wall_list:
            #     if self.collides(wall):
            #         self.handle_wall_collision_x(wall)
            #         self.vel[0] = 0
            #         self.dash_vector[0] = 0
            self.pos[1] += self.vel[1] * dt
            # for wall in wall_list:
            #     if self.collides(wall):
            #         self.handle_wall_collision_y(wall)
            #         self.vel[1] = 0
            #         self.dash_vector[1] = 0

            # Set entity position in grid
            self.grid_sprite.x = self.pos[0] * asset_size
            self.grid_sprite.y = grid_screen_height - (self.pos[1] * asset_size)

            # set entity position in isometric space
            self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
            self.sprite.x = self.iso[0]
            self.sprite.y = self.iso[1] + self.iso[2]


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
    def __init__(self, image, grid_image, x, y, z, speed = 1):
        super().__init__(image, grid_image, x, y, z, speed)
        wall_list.append(self)


class Boss(Entity):
    def __init__(self, image, grid_image, x, y, z, speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/20):
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
            self.fire(0 + self.phase_1_val, 1, 0)
            self.fire(1.5707 + self.phase_1_val, 1, 1)
            self.fire(3.1416 + self.phase_1_val, 1, 2)
            self.fire(4.7124 + self.phase_1_val, 1, 3)
            self.fire(0 - self.phase_1_val, 1, 0)
            self.fire(1.5707 - self.phase_1_val, 1, 1)
            self.fire(3.1416 - self.phase_1_val, 1, 2)
            self.fire(4.7124 - self.phase_1_val, 1, 3)

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
    def __init__(self, image, grid_image, x, y, z, parent, speed = 1, accel = 1, lifespan = 10, vel = [0, 0], damage = 1):
        super().__init__(image, grid_image, x, y, z, speed, accel)
        self.vel = vel
        self.lifespan = lifespan
        self.parent = parent
        self.damage = damage
        self.sprite.update(scale = 1)
        pg.clock.schedule_once(self.die, self.lifespan)

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

        self.pos[0] += self.vel[0] * dt
        # for wall in wall_list:
        #     if self.collides(wall):
        #         self.handle_wall_collision_x(wall)
        #         self.vel[0] = 0
        #         self.die(dt)
        self.pos[1] += self.vel[1] * dt
        # for wall in wall_list:
        #     if self.collides(wall):
        #         self.handle_wall_collision_y(wall)
        #         self.vel[1] = 0
        #         self.die(dt)
        if self.pos[0] < 0.75 or self.pos[1] < 1:
            self.die(dt)

        # Set entity position in grid
        self.grid_sprite.x = self.pos[0] * asset_size
        self.grid_sprite.y = grid_screen_height - (self.pos[1] * asset_size)

        # set entity position in isometric space
        self.iso = iso_coords(self.pos[0], self.pos[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + self.iso[2]


    def handle_collision(self, other):
            self.parent.charge += 1
            self.dead = True
