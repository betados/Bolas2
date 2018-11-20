import pygame
from rigidBodies import *


# from collections import namedtuple


class Metabody(RigidBody):
    def __init__(self, pos, *args, **kwargs):
        self._bodies = args

        mass = sum([obj.mass for obj in self])
        cg = sum([obj.pos * obj.mass for obj in self], Vector()) / mass

        self.dists = [abs(p-cg) for p in self.points]
        self.pos = cg + pos
        RigidBody.__init__(self, pos(), mass=mass)
        # TODO calc moment of inertia
        self.moi = 999999999

    def __iter__(self):
        return iter(self._bodies)

    def actualize(self, time):
        for i, obj in enumerate(self):
            self._forces += [(r + self.points[i], f) for r, f in obj._forces]
            obj._forces = []
        RigidBody.actualize(self, time)

        self.points = [point + point.normal(False) * self._omega * time for point in self.points]
        self.points = [point.unit() * self.dists[i] for i, point in enumerate(self.points)]

        for i, obj in enumerate(self):
            obj.pos = self.points[i] + self.pos
            # rel_pos = obj.pos - self.pos
            # dist = abs(rel_pos)
            # obj.pos = self.pos + rel_pos + (rel_pos + rel_pos.normal(False)) * self._omega * time
            # obj.pos = self.pos + (obj.pos - self.pos).unit() * dist
            obj._omega = self._omega
            obj.actualize(time)


class Car(Metabody):
    def __init__(self, pos):
        height = 99
        width = 201
        wheel_radius = 50
        # points = (Vector(width / 2, height / 2), Vector(0, height), Vector(width, height))
        self.body = RectBody((0, 0, width, height))
        self.wheel = RoundBody(Vector(0, height), wheel_radius, affected_by_gravity=False)
        self.wheel2 = RoundBody(Vector(width, height), wheel_radius, affected_by_gravity=False)
        Metabody.__init__(self, Vector(*pos), self.body, self.wheel, self.wheel2)

    def draw(self, screen):
        # body
        pygame.draw.polygon(screen,
                            (0, 50, 0),
                            [list((p + self.body.pos)()) for p in
                             self.body.points], 0
                            )
        # wheels
        pygame.draw.circle(screen, (255, 20, 20), self.wheel.pos.int(), self.wheel.radio)
        pygame.draw.circle(screen, (20, 100, 20), self.wheel2.pos.int(), self.wheel2.radio)

        #
        pygame.draw.circle(screen, (20, 100, 255), self.pos.int(), 5)
        pygame.draw.line(screen, (0, 255, 0), self.body.pos(), self.pos())

