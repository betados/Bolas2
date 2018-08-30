# -*- coding: utf-8 -*-
from random import randrange
import pygame
from vector_2D.vector import Vector


class Bola(object):
    def __init__(self, res):
        self.pos = Vector(randrange(res[0]), randrange(res[1]))
        self.color = [randrange(255) for _ in range(3)]
        self.radio = 10

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos.int(), self.radio)

