

class Bird:

    def __init__(self, image, velocity=0, gravity=0.3, jump_speed=7.4, window_size=(800, 600), y=None):
        self.image = image
        self.frame_no = 0
        self.cycle = True
        self.v = velocity
        self.g = gravity
        self.y = window_size[1]/2 if y is None else window_size[1]/2 + y
        self.x = 40
        self.jump_speed = jump_speed

    def draw(self, surface, start=True):
        if start:
            self.y += self.v
            self.v += self.g
        if self.frame_no < 0:
            self.cycle = True
            self.frame_no = 1
        elif self.frame_no > 30:
            self.cycle = False
            self.frame_no = 29

        surface.blit(self.image[int(self.frame_no/10)], (self.x, self.y))

        if self.cycle:
            self.frame_no += 1
        else:
            self.frame_no -= 1

    def jump(self):
        self.v = -self.jump_speed