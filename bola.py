# -*- coding: utf-8 -*-
from random import randrange
import pygame
from physical_object import PhysicalObject


class Bola(PhysicalObject):
    def __init__(self, res):
        PhysicalObject.__init__(self, res)
        self.color = [randrange(255) for _ in range(3)]
        self.radio = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.int(), self.radio)

