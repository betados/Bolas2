import pygame
from rigidBodies import *


class Metaobject(RigidBody):
    def __init__(self, *args):
        self._list = args
        mass = sum([obj.mass for obj in self]) * 10
        pos = sum([obj._pos * obj.mass for obj in self], Vector()) / mass
        # TODO calc moment of inertia
        RigidBody.__init__(self, pos(), mass=mass)

    def __iter__(self):
        return iter(self._list)


class Car(Metaobject):
    def __init__(self, pos):
        
        self.body = RectBody((*pos, 20, 10))
        self.wheel = RoundBody(Vector(*pos) + Vector(0, 10), 2, affected_by_gravity=False)
        self.wheel2 = RoundBody(Vector(*pos) + Vector(20, 10), 2, affected_by_gravity=False)
        Metaobject.__init__(self, self.body, self.wheel, self.wheel2)

    def draw(self, screen):
        # body
        pygame.draw.polygon(screen,
                            (0, 50, 0),
                            [[p.x + self.body._pos.x, p.y + self.body._pos.y] for p in
                             self.body.points], 0
                            )
        # wheels
        pygame.draw.circle(screen, (255, 20, 20), self.wheel.pos.int(), self.wheel.radio)
        pygame.draw.circle(screen, (20, 20, 20), self.wheel2.pos.int(), self.wheel2.radio)
        # print self.wheel._forces

    def actualize(self, time):
        pos_ant = self._pos
        for obj in self:
            self._forces += obj._forces
            obj._forces = []
        RigidBody.actualize(self, time)
        dif = self._pos - pos_ant
        for obj in self:
            obj._pos += dif
