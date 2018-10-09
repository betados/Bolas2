# -*- coding: utf-8 -*-

import pygame
from physical_object import *


class Bola(RoundObject):
    def __init__(self, color, pos=None, radio=15):
        RoundObject.__init__(self, pos, radio, affected_by_gravity=True)
        self.color = color

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.int(), self.radio)


class Rect(RectObject):
    def __init__(self, color, rect):
        RectObject.__init__(self, rect)
        self.color = color

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
