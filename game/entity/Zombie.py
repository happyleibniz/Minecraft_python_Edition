from game.entity.Entity import Entity


class Zombie(Entity):
    def __init__(self, gl):
        super().__init__(gl)
        head_width = 1
        head_height = 1
        head_d = 1
        head_x = -1
        head_y = 3
        head_z = 0.25
        self.model.addCube(head_x, head_y, head_z, head_width, head_height, head_d, gl.zombie_head_texture)
        self.model.addCube(head_x, 1.5, 0.5, head_width, head_height*2, head_d/2, gl.zombie_clothes_texture)
        self.model.addCube(-0.5, 0, 0.5, head_width / 2, head_height*2, head_d / 2, gl.zombie_leg_texture)  # left
        # leg(?)
        self.model.addCube(-1, 0, 0.5, head_width / 2.3, head_height*1.92, head_d / 2, gl.zombie_leg_texture)  #
        # right leg(?,UP)
        self.model.addCube(-1.5, 1.5, 0.5, head_width/2, head_height*2, head_d/2, gl.zombie_hand_texture)  # right hand
        self.model.addCube(0, 1.5, 0.5, head_width / 2, head_height * 2, head_d / 2,
                           gl.zombie_hand_texture)  # right hand
