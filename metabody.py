import pygame
from rigidBodies import *


# from collections import namedtuple


class Metabody(RigidBody):
    def __init__(self, pos, *args, **kwargs):
        self._bodies = args

        mass = sum([obj.mass for obj in self])
        gravity_center = sum([obj.pos * obj.mass for obj in self], Vector()) / mass
        self.points = [body.pos - gravity_center for body in self._bodies]
        self.dists = [abs(p) for p in self.points]
        self.pos = pos - gravity_center
        print(self.points)
        RigidBody.__init__(self, self.pos(), mass=mass)
        # TODO calc moment of inertia
        self.moi = 999999999

    def __iter__(self):
        return iter(self._bodies)

    def actualize(self, time):
        pass
        for i, obj in enumerate(self):
            self._forces += [(r + self.points[i], f) for r, f in obj._forces]
            obj._forces = []
        RigidBody.actualize(self, time)

        self.points = [point + point.normal(False) * self._omega * time for point in self.points]
        # self.points = [point.unit() * self.dists[i] for i, point in enumerate(self.points)]

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
        wheel_radius = 40
        # points = (Vector(width / 2, height / 2), Vector(0, height), Vector(width, height))
        self.frame = RectBody((0, 0, width, height))
        self.wheel = RoundBody(Vector(0, height), wheel_radius, affected_by_gravity=False)
        self.wheel2 = RoundBody(Vector(width, height), wheel_radius, affected_by_gravity=False)
        Metabody.__init__(self, Vector(*pos), self.frame, self.wheel, self.wheel2)

    def draw(self, screen):
        # frame
        pygame.draw.polygon(screen,
                            (10, 10, 10),
                            [list((p + self.frame.pos)()) for p in
                             self.frame.points], 0
                            )
        # wheels
        pygame.draw.circle(screen, (50, 0, 0), self.wheel.pos.int(), self.wheel.radio)
        pygame.draw.circle(screen, (0, 50, 0), self.wheel2.pos.int(), self.wheel2.radio)

        #
        pygame.draw.circle(screen, (0, 0, 255), (
                    sum([obj.pos * obj.mass for obj in self], Vector()) / sum([obj.mass for obj in self])).int(), 5)
        # pygame.draw.line(screen, (0, 255, 0), self.frame.pos(), self.pos())
