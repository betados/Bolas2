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
        pygame.draw.polygon(screen,
                            self.color,
                            [[p.x + self._pos.x, p.y + self._pos.y] for p in self.points], 0
                            )
        # TODO check witch is faster
        # for line in self.lines:
        #     pygame.draw.line(screen, (20, 0, 0), line[0].get_comps(), line[1].get_comps(),)

