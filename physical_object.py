# -*- coding: utf-8 -*-

from vector_2D.vector import Vector


class PhysicalObject(object):
    def __init__(self, pos=(0, 0), affected_by_gravity=False):
        self.__pos = Vector(*pos)
        self.__v = Vector()
        if affected_by_gravity:
            # self.__a = Vector(0, 0.0000015)
            self.__a = Vector(0, 0.0000001)
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
        # KINETIC EQUATIONS
        self.__v += 0.5 * self.__a * t ** 2
        self.__pos += self.__v * t

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)

    def is_clicked(self, mouse):
        return Interaction.check_collision(self, mouse)


# TODO implement children: round_object, rect_object

class RoundObject(PhysicalObject):
    def __init__(self, pos, radio=0, **kwargs):
        PhysicalObject.__init__(self, pos, **kwargs)
        self.radio = radio


class RectObject(PhysicalObject):
    def __init__(self, rect, **kwargs):
        PhysicalObject.__init__(self, rect[:2], **kwargs)
        self.rect = rect


class Interaction(object):
    @staticmethod
    def check_collision(obj1, obj2):
        if isinstance(obj1, RoundObject) and isinstance(obj2, RoundObject):
            return abs(obj1.pos - obj2.pos) <= (obj1.radio + obj2.radio)
