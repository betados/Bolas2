# -*- coding: utf-8 -*-

import pygame

from rigidBodies import *


class Bola(RoundBody):
    def __init__(self, color, pos=None, radio=15):
        RoundBody.__init__(self, pos, radio, affected_by_gravity=False)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.int(), self.radio)


class Rect(RectBody):
    def __init__(self, color, rect):
        RectBody.__init__(self, rect)
        self.color = color

    def draw(self, screen):
        # print [[p.x, p.y] for p in self.points]
        pygame.draw.polygon(screen,
                            self.color,
                            [[p.x, p.y] for p in self.points],
                            )
        # for p in self.points:
        #     n = (p - self.pos).normal() * 30
        #     pygame.draw.line(screen, (0, 255, 0), p.get_comps(), (p+n).get_comps(),)

