# -*- coding: utf-8 -*-
from random import randrange
import pygame
from physical_object import PhysicalObject


class Bola(PhysicalObject):
    def __init__(self, pos=None):
        PhysicalObject.__init__(self, pos)
        self.color = [randrange(255) for _ in range(3)]
        self.radio = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.int(), self.radio)

    def is_clicked(self, mouse):
        return abs(self.pos - mouse.pos) <= self.radio
