# -*- coding: utf-8 -*-
from random import randrange
import pygame
from physical_object import PhysicalObject, Interaction


class Bola(PhysicalObject):
    def __init__(self, pos=None):
        PhysicalObject.__init__(self, pos, affected_by_gravity=True)
        self.color = [randrange(255) for _ in range(3)]
        self.radio = 15

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.int(), self.radio)

    def is_clicked(self, mouse):
        return Interaction.check_collision(self, mouse)
