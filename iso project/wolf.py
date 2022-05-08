from engine import *

class Wolf(Enemy):
    def __init__(self, image, animation_dict, grid_image, x, y, z, map,
                 speed = 2.1, accel = 1, proj_speed = 10, fire_rate = 1/6, hp = 10):
        super().__init__(image, animation_dict, grid_image, x, y, z, map, speed, accel, proj_speed, fire_rate, hp)

    def update(self,dt):
        if self.target != None:
            self.move_towards_target()
            # Acceleration
            self.vel[0] += self.acc[0]
            self.vel[1] += self.acc[1]
            # This should limit any vector into the length of self.speed
            if (self.vel[0] ** 2 + self.vel[1] ** 2) > self.speed ** 2:
                scale_down = self.speed / np.sqrt(self.vel[0] ** 2 + self.vel[1] ** 2)
                self.vel = [self.vel[0] * scale_down, self.vel[1] * scale_down]
    
