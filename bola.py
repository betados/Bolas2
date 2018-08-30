# -*- coding: utf-8 -*-
from random import randrange
import pygame
from physical_object import PhysicalObject


class Bola(PhysicalObject):
    def __init__(self, res, pos=None):
        PhysicalObject.__init__(self, res, pos)
        self.color = [randrange(255) for _ in range(3)]
        self.radio = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self._pos.int(), self.radio)

    def is_clicked(self, mouse):
        return abs(self._pos - mouse) <= self.radio
