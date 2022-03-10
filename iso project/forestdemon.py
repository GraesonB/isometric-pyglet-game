from engine import *
from wolf import *

class ForestDemon(Enemy):
    def __init__(self, image, animation_dict, grid_image, x, y, z, map,
                 speed = 1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 100):
        super().__init__(image, animation_dict, grid_image, x, y, z, map, speed, accel, proj_speed, fire_rate, hp)
        self.attack_ready = False
        self.growth_active = False
        self.attack_cd = 6
        self.growth_life = 20
        self.rect_list = rect_list
        pg.clock.schedule_once(self.attack_cd_reset, 7)

    def update(self, dt):
        if self.attack_ready:
            self.acc = [0,0]
            self.vel = [0,0]
            self.casting = True
            if not self.growth_active:
                self.attack_ready = False
                self.growth_active = True
                pg.clock.schedule_once(self.growth, 100/60)
                pg.clock.schedule_once(self.attack_cd_reset, self.attack_cd)
                pg.clock.schedule_once(self.growth_deactivate, self.growth_life)
                pg.clock.schedule_once(self.not_casting, 178/60)
            else:
                random = np.random.uniform()
                if random < 0:
                    self.summon()
                    self.attack_ready = False
                    pg.clock.schedule_once(self.attack_cd_reset, self.attack_cd)
                    pg.clock.schedule_once(self.not_casting, 200/60)
                else:
                    self.fire(self.pos, 1, 20)
                    self.attack_ready = False
                    pg.clock.schedule_once(self.attack_cd_reset, self.attack_cd)
                    pg.clock.schedule_once(self.not_casting, 200/60)

        if not self.stunned and not self.casting:
            self.move_towards_target()
            # Acceleration
            self.vel[0] += self.acc[0]
            self.vel[1] += self.acc[1]
            # This should limit any vector into the length of self.speed
            if (self.vel[0] ** 2 + self.vel[1] ** 2) > self.speed ** 2:
                scale_down = self.speed / np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
                self.vel = [self.vel[0] * scale_down, self.vel[1] * scale_down]

    def get_state(self):
        self.angle = np.arctan2(self.vel[1],self.vel[0])
        self.direction = get_direction2(np.degrees(self.angle))
        if self.stunned:
            self.stand_state = False
            self.move_state = False
            self.animation('stunned',self.direction, 1/2)
        elif self.casting:
            self.stand_state = False
            self.move_state = False
            self.animation('cast1',self.direction, 1/2)
        elif self.vel == [0,0]:
            self.stand_state = True
            self.move_state = False
            self.animation('idle',self.direction, 1/2)
        else:
            self.stand_state = False
            self.move_state = True
            self.animation('walk',self.direction, 1/2)

    def growth(self, dt):
        center = [np.floor(self.pos[0]), np.floor(self.pos[1])]
        offset = [center[0] - 1, center[1] - 1]
        for y,row in enumerate(shrub_data):
            shrub_y = offset[1] + y
            for x,shrub in enumerate(row):
                shrub_x = offset[0] + x
                if shrub and shrub_x > 0 and shrub_y > 0:
                    pg.clock.schedule_once(self.plant, (np.random.randint(1,9) / 30), x = shrub_x, y = shrub_y)

    def plant(self, dt, x, y):
        shrub = Shrub(placeholder, plants_dict, grid_tile, x, y, 1, mapdata[1], self.growth_life)

    def bullet(self, dt, x, y, dx, dy):
        new_proj = Projectile(e_bullet_temp, bullet_dict['enemy_bullet'], enemy_bullet, x, y, self.z, self.map, self, vel = [dx, dy], accel = 0.04, lifespan = 10)
        self.children.append(new_proj)

    def summon(self):
        wolf = Wolf(enemy_temp, placeholder_dict, player_hurtbox, 2, 2, 1, mapdata[1])
        wolf = Wolf(enemy_temp, placeholder_dict, player_hurtbox, 2, 10, 1, mapdata[1])

    def fire(self, origin, speed_multiplier, blast_size):

        angle = np.arctan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])

        for i in range(blast_size):
            new_angle = angle + ((i-(blast_size/2))*0.05)

            proj_x = (origin[0]) + np.cos(new_angle) * 0.5
            proj_y = (origin[1]) + np.sin(new_angle) * 0.5

            proj_dx = np.cos(new_angle) * self.proj_speed * speed_multiplier
            proj_dy = np.sin(new_angle) * self.proj_speed * speed_multiplier
            pg.clock.schedule_once(self.bullet, (i/30), x = proj_x, y = proj_y, dx = proj_dx, dy = proj_dy)


    def attack_cd_reset(self, dt):
        self.attack_ready = True

    def not_casting(self, dt):
        self.casting = False

    def growth_deactivate(self,dt):
        self.growth_active = False

class Shrub(Entity):
    def __init__(self, image, animation_dict, grid_image, x, y, z, map, lifespan, hp = 6, bat = None, grp = None, grid_grp = grid_entity_group):
        super().__init__(image, animation_dict, grid_image, x, y, z, map)
        self.sprite = pg.sprite.Sprite(img = self.animation_dict['grow']['W'][0], x = self.iso[0], y = self.iso[1] + (self.iso[2] / 2),
                                       batch = bat, group = grp)
        self.sprite.update(scale = scale)
        pg.clock.schedule_once(self.set_ani_to_idle, 90/60)
        self.grid_sprite = pg.sprite.Sprite(img = self.grid_image, x = self.grid_pos[0], y = self.grid_pos[1],
                                            batch = grid_batch, group = grid_grp)
        self.rect_pt1 = self.pos
        self.rect_pt2 = [self.pos[0]+1, self.pos[1]+1]
        self.rect = [self.rect_pt1, self.rect_pt2]
        tile_update_list.append(self)
        barrier_list.append(self)
        to_add_rect_list.append(self.rect)
        pg.clock.schedule_once(self.die, lifespan)

    def update_pos(self, dt):
        self.iso = iso_coords(self.pos[0] - camera_movement[0], self.pos[1] - camera_movement[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + (self.iso[2] / 2)

    def set_ani_to_idle(self, dt):
        self.sprite.image = self.animation_dict['idle']['W'][0]

    def delete(self):
        self.sprite.delete()
        self.grid_sprite.delete()
        barrier_list.remove(self)
        tile_update_list.remove(self)
        to_remove_rect_list.append(self.rect)

    def die(self, dt):
        self.dead = True
