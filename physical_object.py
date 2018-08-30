from random import randrange

from vector_2D.vector import Vector


class PhysicalObject(object):
    def __init__(self, screen_size):
        self.pos = Vector(randrange(screen_size[0]), randrange(screen_size[1]))
