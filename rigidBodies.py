# -*- coding: utf-8 -*-

from __future__ import division

from math import pi

from vector_2d import *


class RigidBody(object):
    def __init__(self, pos=(0, 0), affected_by_gravity=False, mass=10, static=False):
        self._pos = Vector(*pos)
        self.__v = Vector()
        self.__a = Vector()
        self._forces = []
        self._omega = 0
        self._alpha = 0
        self.mass = mass
        # Moment of inertia
        self.moi = 9e9
        self.affected_by_gravity = affected_by_gravity

    def __repr__(self):
        return type(self).__name__ + '{}'.format(self.pos())

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, value):
        assert isinstance(value, Vector), 'That value is not a Vector'
        self._pos = value

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
            self._forces.append((Vector(0, 0), Vector(0, 0.009)))
        force = sum((f[1] for f in self._forces), Vector())
        self.__a = force / self.mass
        self._alpha = sum(f[0] * f[1] for f in self._forces) / self.moi

        # KINETIC EQUATIONS
        self.__v += self.__a * t
        self._pos += self.__v * t
        self._omega += self._alpha * t

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
        self.list = [self.__p1, self.__p2]

    @property
    def points(self):
        return self.__p1, self.__p2

    def __getitem__(self, item):
        return self.list[item]

    def __iter__(self):
        return iter(self.list)


class RectBody(RigidBody):
    def __init__(self, rect, **kwargs):
        # TODO the rect objects could have round ones on corners to improve bounces
        self.points = [Vector(*rect[:2]), ]
        self.points.append(self.points[-1] + Vector(rect[2], 0))
        self.points.append(self.points[-1] + Vector(0, rect[3]))
        self.points.append(self.points[-1] - Vector(rect[2], 0))
        pos = (self.points[0] + self.points[2]) / 2.0
        self.lines = [LineObject(self.points[i - 1] + pos, self.points[i] + pos) for i in
                      range(len(self.points))]
        self._diagonal = abs(self.points[0] - pos)
        self.points = [point - pos for point in self.points]
        kwargs['mass'] = rect[2] * rect[3] * 20
        RigidBody.__init__(self, pos, **kwargs)

        self._omega = 0.00000
        self.moi = self.mass * (rect[2] ** 2 + rect[3] ** 2) / 12
        self.click_point_on_platform = None

    def append_force(self, r, f):
        assert isinstance(r, Vector) and isinstance(f, Vector), 'Esas fuerzas no son vectores'
        self._forces.append((r, f))

    def actualize(self, t):
        RigidBody.actualize(self, t)
        self.points = [point + point.normal(False) * self._omega * t for point in self.points]
        self.points = [point.unit() * self._diagonal for point in self.points]
        if self.click_point_on_platform:
            self.click_point_on_platform += (self._omega *
                                             (self.click_point_on_platform - self._pos).normal(False) + self.v) * t
        self.lines = [LineObject(self.points[i - 1] + self._pos, self.points[i] + self._pos) for i in
                      range(len(self.points))]
