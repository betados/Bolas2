# -*- coding: utf-8 -*-
import os
import sys
from random import randrange

import pygame
from vector_2d import Vector

from interaction import Interaction
from metabody import Car
from objects import Bola, Rect
from rigidBodies import LineObject, RoundBody


class Main(object):
    def __init__(self):
        if sys.platform == 'win32' or sys.platform == 'win64':
            os.environ['SDL_VIDEO_CENTERED'] = '1'

        pygame.init()
        self.reloj = pygame.time.Clock()

        resolution = (1050, 600)
        Interaction.set_screen_height(resolution[1])
        pygame.display.set_caption('Bolas')
        self.screen = pygame.display.set_mode(resolution, pygame.SRCALPHA, 32)

        self.done = False
        self.fps = 200
        self.fps_draw = 50
        self.acum_time = 0

        self.owned_bola = None
        self.owned_platform = None
        self.p_list = None
        bolas_number = 1
        self.bolas = [
            Bola(
                color=[randrange(100) for _ in range(3)],
                pos=(randrange(resolution[0]), randrange(resolution[1])),
                radio=randrange(10, 25),
            ) for _ in range(bolas_number)
        ]
        floor = LineObject((0, resolution[1]), resolution)
        # floor = LineObject((0, resolution[1]), (resolution[0], resolution[1]-50), static=True)
        ceiling = LineObject((resolution[0], 0), (0, 0))
        walls = (LineObject((0, 0), (0, resolution[1])),
                 LineObject(resolution, (resolution[0], 0)),
                 )

        platform1 = Rect((50, 0, 0), (100, 400, 500, 40))
        # platform2 = Rect((0, 10, 0), (100, resolution[1] - 100, 600, 50))
        self.platforms = [
            platform1,
            # platform2,
        ]
        self.car = Car((400, 200))
        self.box = (floor, ceiling) + walls
        self.mouse = RoundBody((0, 0))

    def loop(self):
        while not self.done:
            self.screen.fill((0, 0, 0, 255))
            time = self.reloj.get_time()

            self.acum_time += time
            if self.acum_time >= 1000 / self.fps_draw:
                self.draw(time)
                self.acum_time = 0

            events = pygame.event.get()
            keys = pygame.key.get_pressed()

            if time:
                self.mouse.v = Vector(*pygame.mouse.get_rel()) / time
                self.mouse.pos = Vector(*pygame.mouse.get_pos())
            if pygame.mouse.get_pressed()[0]:
                if self.owned_bola:
                    self.owned_bola.v = self.mouse.v
                if self.owned_platform:
                    self.owned_platform.append_force(
                        self.owned_platform.click_point_on_platform - self.owned_platform.pos,
                        self.mouse.pos - self.owned_platform.click_point_on_platform)
                    self.p_list = [self.owned_platform.pos, self.owned_platform.click_point_on_platform, self.mouse.pos]
                else:
                    self.p_list = None

            for event in events:
                if event.type == pygame.QUIT:
                    self.done = True
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for bola in self.bolas:
                        if Interaction.is_clicked(bola, self.mouse):
                            self.owned_bola = bola
                            break
                    for platform in self.platforms:
                        if Interaction.is_clicked(platform, self.mouse):
                            self.owned_platform = platform
                            self.owned_platform.click_point_on_platform = self.mouse.pos
                            break

                    if Interaction.is_clicked(self.car.frame, self.mouse):
                        self.owned_platform = self.car.frame
                        self.owned_platform.click_point_on_platform = self.mouse.pos

                if event.type == pygame.MOUSEBUTTONUP:
                    self.owned_bola = None
                    self.owned_platform = None

            if keys[pygame.K_ESCAPE]:
                self.done = True

            self.interaction(time)

            self.reloj.tick(self.fps)

    def draw(self, time):
        if self.owned_platform:
            try:
                pygame.draw.lines(self.screen, (0, 200, 0), False, [[p.x, p.y] for p in self.p_list])
            except TypeError:
                pass
        for bola1 in self.bolas:
            bola1.draw(self.screen)
        for platform_i in self.platforms:
            platform_i.draw(self.screen)
        self.car.draw(self.screen)
        self.car.actualize(time)
        pygame.display.flip()

    def interaction(self, time):
        for bola1 in self.bolas:
            bola1.actualize(time)
            for element in self.box:
                # FIXME si va demasiado rápido atraviesa
                Interaction.check_collision(bola1, element)
            for platform in self.platforms:
                Interaction.check_collision(bola1, platform)
            for bola2 in self.bolas:
                # TODO recorrer solo la mitad de las bolas y en la interacción aplicar fuerzas a las dos
                Interaction.check_collision(bola1, bola2)

            # TODO comprobarlo solo una vez y aplicar la fuerza en los dos
            Interaction.check_collision(bola1, self.car)
            Interaction.check_collision(self.car, bola1)

        for platform_i in self.platforms:
            # TODO comprobarlo solo una vez y aplicar la fuerza en los dos
            Interaction.check_collision(platform_i, self.car)
            Interaction.check_collision(self.car, platform_i)
            for platform_j in self.platforms:
                # TODO recorrer solo la mitad de las plataformas y en la interacción aplicar fuerzas a las dos
                Interaction.check_collision(platform_i, platform_j)
            platform_i.actualize(time)


if __name__ == "__main__":
    main = Main()
    main.loop()

    # Cerramos la ventana y salimos.
    # Si te olvidas de esta ultima linea, el programa se 'colgara'
    # al salir si lo hemos estado ejecutando desde el IDLE.
    pygame.quit()
