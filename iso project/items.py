from engine import *


class Items(Entity):
    def __init__(self, image, animation_dict, grid_image, x, y, z,
                 speed = 1):
        super().__init__(image, animation_dict, grid_image, x, y, z, speed)

    def update_pos(self, dt):
        self.iso = iso_coords(self.pos[0] - camera_movement[0], self.pos[1] - camera_movement[1], self.z)
        self.sprite.x = self.iso[0]
        self.sprite.y = self.iso[1] + (self.iso[2] / 2)

    def on_pickup(self):
        pass
