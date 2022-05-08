from engine import *

class Death(Enemy):
    def __init__(self, image, animation_dict, grid_image, x, y, z, map,
                 speed = 1, accel = 1, proj_speed = 4, fire_rate = 1/6, hp = 100):
        super().__init__(image, animation_dict, grid_image, x, y, z, map, speed, accel, proj_speed, fire_rate, hp)

        self.body_particle_dict = animation_dict
        self.particle_sprite = pg.sprite.Sprite(img = self.animation_dict['walk']['E'][0], x = self.iso[0], y = self.iso[1] + (self.iso[2] / 2))
        self.particle_sprite.update(scale = scale)
        self.attack_ready = False
        self.holding_scythe = True
        self.attack_cd = 6
        self.rect_list = rect_list
        rand = np.random.randint(2,10)
        pg.clock.schedule_once(self.attack_cd_reset, rand)

    def update(self, dt):
        if self.attack_ready:
            self.acc = [0,0]
            self.vel = [0,0]
            self.casting = True
            if self.holding_scythe:
                random = np.random.uniform()
                if random >= 0:
                    self.throw_cast = True
                    self.attack_ready = False
                    self.holding_scythe = False
                    pg.clock.schedule_once(self.throw, 60/60)
                    pg.clock.schedule_once(self.attack_cd_reset, self.attack_cd)
                    pg.clock.schedule_once(self.not_casting, 158/60)
                else:
                    pass
                    # self.fire_cast = True
                    # self.attack_ready = False
                    # pg.clock.schedule_once(self.fire, 55/60)
                    # pg.clock.schedule_once(self.attack_cd_reset, self.attack_cd)
                    # pg.clock.schedule_once(self.not_casting, 138/60)
            else:
                self.throw_cast = True
                self.attack_ready = False
                self.holding_scythe = False
                pg.clock.schedule_once(self.fire, 60/60)
                pg.clock.schedule_once(self.attack_cd_reset, self.attack_cd)
                pg.clock.schedule_once(self.not_casting, 158/60)
        if not self.stunned and not self.casting:
            self.move_towards_target()
            # Acceleration
            self.vel[0] += self.acc[0]
            self.vel[1] += self.acc[1]
            # This should limit any vector into the length of self.speed
            if (self.vel[0] ** 2 + self.vel[1] ** 2) > self.speed ** 2:
                scale_down = self.speed / np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
                self.vel = [self.vel[0] * scale_down, self.vel[1] * scale_down]

    def state_handler(self):
        self.angle = np.arctan2(self.vel[1],self.vel[0])
        self.direction = get_direction2(np.degrees(self.angle))
        self.idle_angle = np.arctan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])
        self.idle_direction = get_direction2(np.degrees(self.idle_angle))
        if self.stunned:
            self.stand_state = False
            self.move_state = False
            self.animation('stunned',self.direction, 1/2)
        elif self.casting:
            self.stand_state = False
            self.move_state = False
            if self.throw_cast:
                self.animation('throw', self.idle_direction, 1/2)
        elif self.vel == [0,0]:
            self.stand_state = True
            self.move_state = False
            self.animation('walk',self.idle_direction, 1/2)
        else:
            self.stand_state = False
            self.move_state = True
            self.animation('walk',self.direction, 1/2)

    def bullet(self, dt, x, y, dx, dy):
        new_proj = Projectile(e_bullet_temp, bullet_dict['enemy_bullet'], enemy_bullet, x, y, self.z, self.map, self, vel = [dx, dy], accel = 0.04, lifespan = 10)
        self.children.append(new_proj)

    def throw(self, speed_multiplier = 1, blast_size = 4):
        angle = np.arctan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])

        proj_x = (self.pos[0]) + np.cos(angle) * 0.8
        proj_y = (self.pos[1]) + np.sin(angle) * 0.8

        proj_dx = np.cos(angle) * self.proj_speed * speed_multiplier
        proj_dy = np.sin(angle) * self.proj_speed * speed_multiplier
        new_proj = Scythe(e_bullet_temp, self.animation_dict['scythe_attack'], player_hurtbox,
            proj_x, proj_y, self.z, self.map, self, vel = [proj_dx, proj_dy])
        self.children.append(new_proj)

    def fire(self, speed_multiplier = 1, blast_size = 4):
        angle = np.arctan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])
        for i in range(blast_size):
            new_angle = angle + ((i-(blast_size/2))*0.1)
            proj_x = (self.pos[0]+0.5) + np.cos(new_angle) * 0.8
            proj_y = (self.pos[1]+0.5) + np.sin(new_angle) * 0.8
            rand = (np.random.uniform() - 0.5) / 10
            proj_dx = np.cos(new_angle + rand) * self.proj_speed * speed_multiplier
            proj_dy = np.sin(new_angle + rand) * self.proj_speed * speed_multiplier
            new_proj = Projectile(e_bullet_temp, bullet_dict['enemy_bullet'], enemy_bullet,
                proj_x, proj_y, self.z, self.map, self, vel = [proj_dx, proj_dy], accel = 0.04, lifespan = 10)
            self.children.append(new_proj)
            #pg.clock.schedule_once(self.bullet, (i/15), x = proj_x, y = proj_y, dx = proj_dx, dy = proj_dy)

    def handle_return_projectile(self):
        self.holding_scythe = True


    def post_wall_update(self, dt):
        self.check_wall_collisions(dt)
        self.resolve_wall_collisions(dt)
        self.state_handler()
        self.update_particles()
        self.finalize_update(dt)

    def finalize_update(self, dt):
        self.grid_pos[0] = self.pos[0] * grid_asset_size
        self.grid_pos[1] = self.pos[1] * grid_asset_size
        # Set entity position in grid
        self.grid_sprite.x = self.grid_pos[0]
        self.grid_sprite.y = grid_screen_height - (self.grid_pos[1])
        # set entity position in isometric space
        self.iso = iso_coords((self.pos[0] - camera_movement[0]), (self.pos[1] - camera_movement[1]), self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + (self.iso[2] / 2)

    def update_particles(self):
        self.particle_pos[0] += (self.pos[0] - self.particle_pos[0]) / 5
        self.particle_pos[1] += (self.pos[1] - self.particle_pos[1]) / 5
        self.particle_iso = iso_coords((self.particle_pos[0] - camera_movement[0]), (self.particle_pos[1] - camera_movement[1]), self.z)
        self.particle_sprite.image = self.animation_dict[self.current_animation + '_particles'][self.direction][self.ani_current_frame]
        self.particle_sprite.x = self.particle_iso[0]
        self.particle_sprite.y = self.particle_iso[1] + (self.iso[2] / 2)

    def attack_cd_reset(self, dt):
        self.attack_ready = True

    def not_casting(self, dt):
        self.casting = False
        # self.growth_cast = False
        # self.fire_cast = False
        # self.summon_cast = False

    def draw_sprites(self):
        self.particle_sprite.draw()
        self.sprite.draw()

class Scythe(Projectile):
    def __init__(self, image, animation_dict, grid_image, x, y, z, map, parent, speed = 2.5, accel = 0.1,
                 lifespan = 50, vel = [0, 0], damage = 1, coll_behaviour = 'bounce'):
        super().__init__(image, animation_dict, grid_image, x, y, z, map, parent, speed, accel, lifespan, vel, damage, coll_behaviour)
        self.dir_thrown_x = self.vel[0].copy()
        self.dir_thrown_y = self.vel[1].copy()
        self.target = parent.target
        self.return_timer = 5
        #return_projectile_list.append(self)
        pg.clock.schedule_once(self.return_to_parent, self.return_timer)

    def update(self, dt):
        try:
            self.angle = np.arctan2(self.target.pos[1] - self.pos[1], self.target.pos[0] - self.pos[0])
            self.acc[0] = np.cos(self.angle) * self.accel
            self.acc[1] = np.sin(self.angle) * self.accel

            self.vel[0] += self.acc[0]
            self.vel[1] += self.acc[1]

            self.vel = limit_velocity(self.vel, self.speed)
        except:
            self.dead = True

    def collides_parent(self, other):
        try:
            self.x1, self.y1 = self.pos
            self.x2, self.y2 = [(self.pos[0] + (self.grid_sprite.width / grid_asset_size)),
                                (self.pos[1] + (self.grid_sprite.height / grid_asset_size))]
            other.x1, other.y1 = other.pos
            other.x2, other.y2 = [(other.pos[0] + (other.grid_sprite.width / grid_asset_size)),
                                  (other.pos[1] + (other.grid_sprite.height / grid_asset_size))]
            if self.x2 <= other.x1 or self.x1 >= other.x2 or self.y2 <= other.y1 or self.y1 >= other.y2:
                return False
            else:
                return True
        except:
            self.dead = True

    def delete(self):
        super().delete()
        if type(self.parent) == Player:
            player_bullets.remove(self)
        if type(self.parent) == Enemy:
            enemy_bullets.remove(self)
        return_projectile_list.remove(self)

    def handle_parent_collision(self):
        self.dead = True

    def handle_collision(self, other):
            self.parent.charge += 1

    def return_to_parent(self, dt):
        return_projectile_list.append(self)
        self.target = self.parent
