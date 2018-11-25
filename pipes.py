import pygame

from numpy import random


class Pipe:

    def __init__(self, image, velocity=2, window_size=(380, 600), width=50, x=None, height=None):
        self.imagel = image
        self.imageu = image
        self.diff = 200
        if x is None:
            self.x = window_size[0]
        else:
            self.x = x
        self.v = velocity
        if height is None:
            self.height = random.randint(80, 360)
        else:
            self.height = height
        self.width = width
        self.imageu = pygame.transform.flip(self.imageu, False, True)
        self.imagel = pygame.transform.scale(self.imagel, (width, window_size[1] - self.height - self.diff))
        self.imageu =  pygame.transform.scale(self.imageu, (width, self.height))

    def draw(self, surface):
        self.x -= self.v
        if self.x + 50 > 0:
            surface.blit(self.imageu, (self.x, 0))
            surface.blit(self.imagel, (self.x, self.height + self.diff))

    def is_seen(self):
        return self.x + 50 > 0

    def is_touching(self, bird, bird_scale):
        if bird.x + bird_scale[0] < self.x or bird.x > self.x + self.width:
            return False

        if bird.y > self.height and bird.y + bird_scale[1] < self.height + self.diff:
            return False

        return True
