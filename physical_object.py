from random import randrange

from vector_2D.vector import Vector


class PhysicalObject(object):
    def __init__(self, screen_size, pos=None):
        if pos:
            self._pos = Vector(*pos)
        else:
            self._pos = Vector(randrange(screen_size[0]), randrange(screen_size[1]))
        self._v = Vector()
        self._a = Vector()

    def actualize(self, t):
        self._v += 0.5 * self._a * t ** 2
        self._pos += self._v * t
