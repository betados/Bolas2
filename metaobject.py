import pygame
from rigidBodies import *


# from collections import namedtuple


class Metaobject(RigidBody):
    def __init__(self, pos, *args, **kwargs):
        self._list = args
        self.points = kwargs['points']
        self.dists = [abs(p) for p in self.points]
        mass = sum([obj.mass for obj in self])
        pos = pos + sum([obj._pos * obj.mass for obj in self], Vector()) / mass
        RigidBody.__init__(self, pos(), mass=mass)
        # TODO calc moment of inertia
        self.moi = 9999999

    def __iter__(self):
        return iter(self._list)

    def actualize(self, time):
        for obj in self:
            self._forces += [(r + (obj.pos - self.pos), f) for r, f in obj._forces]
            obj._forces = []
        RigidBody.actualize(self, time)

        self.points = [point + point.normal(False) * self._omega * time for point in self.points]
        self.points = [point.unit() * self.dists[i] for i, point in enumerate(self.points)]

        for i, obj in enumerate(self):
            obj.pos = self.points[i]
            # rel_pos = obj.pos - self.pos
            # dist = abs(rel_pos)
            # obj.pos = self.pos + rel_pos + (rel_pos + rel_pos.normal(False)) * self._omega * time
            # obj.pos = self.pos + (obj.pos - self.pos).unit() * dist
            obj._omega = self._omega
            obj.actualize(time)


class Car(Metaobject):
    def __init__(self, pos):
        height = 20
        width = 40
        wheel_radius = 10
        # TODO que sean named tuples donde se guarde la posicion relativa
        points = (Vector(), Vector(0, height), Vector(width, height))
        self.body = RectBody((*points[0](), width, height))
        self.wheel = RoundBody(points[1], wheel_radius, affected_by_gravity=False)
        self.wheel2 = RoundBody(points[2], wheel_radius, affected_by_gravity=False)
        Metaobject.__init__(self, Vector(*pos), self.body, self.wheel, self.wheel2, points=points)

    def draw(self, screen):
        # body
        pygame.draw.polygon(screen,
                            (0, 50, 0),
                            [list((p + self.body.pos + self.pos)())for p in
                             self.body.points], 0
                            )
        # wheels
        pygame.draw.circle(screen, (255, 20, 20), (self.pos + self.wheel.pos).int(), self.wheel.radio)
        pygame.draw.circle(screen, (20, 20, 20),  (self.pos + self.wheel2.pos).int(), self.wheel2.radio)
        pygame.draw.line(screen, (0, 255, 0),  (self.pos + self.body.pos).int(), self.pos())
