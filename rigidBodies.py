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
            self._forces.append((Vector(0, 0), Vector(0, 0.09)))
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


class RectBody(RigidBody):
    def __init__(self, rect, **kwargs):
        # TODO the rect objects could have round ones on corners to improve bounces
        self.points = [Vector(*rect[:2]), ]
        self.points.append(self.points[-1] + Vector(rect[2], 0))
        self.points.append(self.points[-1] + Vector(0, rect[3]))
        self.points.append(self.points[-1] - Vector(rect[2], 0))
        kwargs['mass'] = rect[2] * rect[3] * 20
        RigidBody.__init__(self, (0, 0), **kwargs)
        self.calc_pos_from_points()
        self._omega = 0.00
        self.moi = self.mass * (rect[2] ** 2 + rect[3] ** 2) / 12
        self.lines = [LineObject(self.points[i - 1], self.points[i]) for i in range(len(self.points))]
        self.click_point_on_platform = None

    def append_force(self, r, f):
        assert isinstance(r, Vector) and isinstance(f, Vector), 'Esas fuerzas no son vectores'
        self._forces.append((r, f))

    def calc_pos_from_points(self):
        self._pos = (self.points[0] + self.points[2]) / 2.0

    def actualize(self, t):
        RigidBody.actualize(self, t)
        # print self._omega
        self.points = [point + (self._omega * abs(point - self._pos) * (point - self._pos).normal() + self.v) * t for point in self.points]
        if self.click_point_on_platform:
            self.click_point_on_platform += (self._omega * abs(self.click_point_on_platform - self._pos) *
                                             (self.click_point_on_platform - self._pos).normal() + self.v) * t
        self.calc_pos_from_points()
        self.lines = [LineObject(self.points[i - 1], self.points[i]) for i in range(len(self.points))]


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
                        distance = obj1.pos - obj2.pos - normal * (obj1.radio - overlap)
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
        if isinstance(obj, RoundBody):
            return abs(obj.pos - mouse.pos) <= obj.radio

        if isinstance(obj, RectBody):
            return Interaction.is_inside_closed_lines(obj.lines, mouse.pos)

    @staticmethod
    def is_inside_rect(rect, pos):
        return rect[0] < pos.x < rect[0] + rect[2] and rect[1] < pos.y < rect[1] + rect[3]

    @staticmethod
    def is_inside_closed_lines(lines_list, pos):
        # FIXME no funciona perfecto todasl as veces
        times = 0
        # FIXME sería bueno saber el ancho de la pantalla para el range
        for i in range(999):
            for line in lines_list:
                if distance_point_segment(pos + Vector(i, 0), line) < 1:
                    times += 1
        # print times
        # I divide it cause each line crossing two points are at less than one of distance
        if (times/2) % 2 != 0:
            return True
        else:
            return False
