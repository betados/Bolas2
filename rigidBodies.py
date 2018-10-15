# -*- coding: utf-8 -*-

from __future__ import division

from math import pi

from vector_2d import *


class RigidBody(object):
    def __init__(self, pos=(0, 0), affected_by_gravity=False, mass=10, static=False):
        self.__pos = Vector(*pos)
        self.__v = Vector()
        self.__a = Vector()
        self._forces = []
        self._omega = 0.009
        self.__alpha = 0
        self.mass = mass
        # Moment of inertia
        self.moi = 9e9
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
        # FORCES
        if self.affected_by_gravity:
            self._forces.append((Vector(0, 0), Vector(0, 0.09)))
        force = sum((f[1] for f in self._forces), Vector())
        self.__a = force / self.mass
        self.__alpha = sum(f[0] * f[1] for f in self._forces) / self.moi

        # KINETIC EQUATIONS
        self.__v += self.__a * t
        self.__pos += self.__v * t
        self._omega += self.__alpha * t

        # WIPE FORCES
        self._forces = []

    def __eq__(self, other):
        return id(self) == id(other)

    def __ne__(self, other):
        return id(self) != id(other)


class RoundBody(RigidBody):
    def __init__(self, pos, radio=0, **kwargs):
        kwargs['mass'] = (4 / 3.0) * pi * radio ** 3
        RigidBody.__init__(self, pos, **kwargs)
        self.radio = radio
        self.k = 9

    def append_force(self, force):
        self._forces.append((Vector(), force))


class LineObject(object):
    def __init__(self, p1, p2):
        self.__p1 = Vector(*p1)
        self.__p2 = Vector(*p2)

    @property
    def points(self):
        return self.__p1, self.__p2


class RectBody(RigidBody):
    def __init__(self, rect, **kwargs):
        # TODO the rect objects could have round ones on corners to improve bounces
        self.points = [Vector(*rect[:2]), ]
        self.points.append(self.points[-1] + Vector(rect[2], 0))
        self.points.append(self.points[-1] + Vector(0, rect[3]))
        self.points.append(self.points[-1] - Vector(rect[2], 0))
        self.pos = (self.points[0] + self.points[2]) / 2.0
        RigidBody.__init__(self, self.pos, **kwargs)

        # self._rect = rect
        self.moi = 1000000 * self.mass * (rect[2] ** 2 + rect[3] ** 2) / 12
        self.lines = [LineObject(self.points[i - 1], self.points[i]) for i in range(len(self.points))]

    def append_force(self, r, f):
        self._forces.append((r, f))

    @property
    def rect(self):
        rect = list(self.points[0].get_comps())
        rect.append(abs(self.points[0] - self.points[1]))
        rect.append(abs(self.points[1] - self.points[2]))
        print rect
        return rect

    def actualize(self, t):
        RigidBody.actualize(self, t)
        self.points = [point + self._omega * (point - self.pos).normal() * t for point in self.points]

        print self.points


class Interaction(object):
    @staticmethod
    def check_collision(obj1, obj2):
        if id(obj1) != id(obj2):
            if isinstance(obj1, RoundBody) and isinstance(obj2, LineObject):
                Interaction.manage_round_line_collision(obj1, obj2)
                return

            if isinstance(obj1, RoundBody) and isinstance(obj2, RoundBody):
                overlap = ((obj1.radio + obj2.radio) - abs(obj1.pos - obj2.pos))
                if overlap > 0:
                    obj1.append_force((obj1.pos - obj2.pos).unit() * overlap * obj1.k)
                return

            if isinstance(obj1, RoundBody) and isinstance(obj2, RectBody):
                for line in obj2.lines:
                    overlap, normal = Interaction.manage_round_line_collision(obj1, line)
                    if overlap and overlap > 0:
                        distance = obj1.pos - obj2.pos - normal * obj1.radio
                        obj2.append_force(distance, -normal * overlap * obj1.k)

    @staticmethod
    def manage_round_line_collision(round_obj, obj2):
        overlap = round_obj.radio - distance_point_segment(round_obj.pos, obj2.points)
        if overlap > 0:
            normal = (obj2.points[0] - obj2.points[1]).normal()
            round_obj.append_force(
                # FIXME solo una cara es rebotante y esa dependa de orden de los puntos al crear
                normal * overlap * round_obj.k)
            return overlap, normal
        return None, None

    @staticmethod
    def is_clicked(obj, mouse):
        return abs(obj.pos - mouse.pos) <= obj.radio
