

from vector_2D.vector import Vector


class PhysicalObject(object):
    def __init__(self, pos, affected_by_gravity=False):
        self.__pos = Vector(*pos)
        self.__v = Vector()
        if affected_by_gravity:
            self.__a = Vector(0, 0.0000015)
        else:
            self.__a = Vector()

    @property
    def pos(self):
        return self.__pos

    @pos.setter
    def pos(self, value):
        assert isinstance(value, Vector), 'That value is not a Vector'
        self.__pos = value

    @property
    def v(self):
        return self.__v

    @v.setter
    def v(self, value):
        assert isinstance(value, Vector), 'That value is not a Vector'
        self.__v = value

    @property
    def a(self):
        return self.__a

    @a.setter
    def a(self, value):
        assert isinstance(value, Vector), 'That value is not a Vector'
        self.__a = value

    def actualize(self, t):
        self.__v += 0.5 * self.__a * t ** 2
        self.__pos += self.__v * t
