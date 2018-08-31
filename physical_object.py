# -*- coding: utf-8 -*-

from math import pi

from vector_2D.vector import Vector


class PhysicalObject(object):
    def __init__(self, pos=(0, 0), affected_by_gravity=False, mass=10):
        self.__pos = Vector(*pos)
        self.__v = Vector()
        self.__a = Vector()
        self.__forces = []
        self.mass = mass
        self.affected_by_gravity = affected_by_gravity

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
        if self.affected_by_gravity:
            self.__forces.append(Vector(0, 0.01))
        force = sum(self.__forces, Vector())
        self.__a = force / self.mass

        # KINETIC EQUATIONS
        self.__v += 0.5 * self.__a * t ** 2
        self.__pos += self.__v * t

        # WIPE FORCES
        self.__forces = []

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)

    def append_force(self, force):
        self.__forces.append(force)


# TODO implement children: round_object, rect_object

class RoundObject(PhysicalObject):
    def __init__(self, pos, radio=0, **kwargs):
        kwargs['mass'] = (4 / 3.0) * pi * radio ** 3
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

    @staticmethod
    def manage_collision(obj1, obj2):
        if Interaction.check_collision(obj1, obj2):
            obj1.append_force((obj1.pos - obj2.pos).unit() * ((obj1.radio + obj2.radio) - abs(obj1.pos - obj2.pos)))

    @staticmethod
    def is_clicked(obj, mouse):
        return Interaction.check_collision(obj, mouse)
