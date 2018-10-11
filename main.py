# -*- coding: utf-8 -*-
import os
import sys
from random import randrange

import pygame
from vector_2d import Vector

from objects import Bola, Rect
from physical_object import Interaction, LineObject, RoundObject

if __name__ == "__main__":
    if sys.platform == 'win32' or sys.platform == 'win64':
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    reloj = pygame.time.Clock()

    resolution = (1050, 600)
    pygame.display.set_caption('Bolas')
    screen = pygame.display.set_mode(resolution, pygame.SRCALPHA, 32)

    done = False
    fps = 120
    count = 9999

    owned_bola = None

    bolas = [Bola(color=[randrange(20) for _ in range(3)],
                  pos=(randrange(resolution[0]), randrange(resolution[1])))
             for _ in range(20)]
    floor = LineObject((0, resolution[1]), resolution, static=True)
    # floor = LineObject((0, resolution[1]), (resolution[0], resolution[1]-50), static=True)
    ceiling = LineObject((resolution[0], 0), (0, 0), static=True)
    walls = (LineObject((0, 0), (0, resolution[1]), static=True),
             LineObject(resolution, (resolution[0], 0), static=True),
             )
    # platform = LineObject((100, resolution[1]-200), (350, resolution[1]-200), static=True)
    platform = Rect((50, 50, 5), (100, resolution[1] - 300, 500, 200))
    box = (floor, ceiling, platform) + walls
    mouse = RoundObject((0, 0))

    while not done:
        screen.fill((0, 0, 0, 255))
        time = reloj.get_time()

        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        # count += 1
        # Once a minute:
        # if count > fps * 20:
        #     count = 0

        if time:
            mouse.v = Vector(*pygame.mouse.get_rel()) / time
        mouse.pos = Vector(*pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[0] and owned_bola:
            owned_bola.v = mouse.v

        for event in events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bola in bolas:
                    if Interaction.is_clicked(bola, mouse):
                        owned_bola = bola
            if event.type == pygame.MOUSEBUTTONUP:
                owned_bola = None

            # if event.type == pygame.KEYDOWN and keys[pygame.K_c]:
            # if event.type == pygame.KEYDOWN and keys[pygame.K_s]:
            # if event.type == pygame.KEYDOWN and keys[pygame.K_t]:
            # if event.type == pygame.KEYDOWN and keys[pygame.K_TAB]:
        if keys[pygame.K_ESCAPE]:
            done = True

        for bola1 in bolas:
            bola1.draw(screen)
            bola1.actualize(time)
            for element in box:
                # FIXME si va demasiado rápido atraviesa
                Interaction.check_collision(bola1, element)
                try:
                    # FIXME todos debería tener metodo draw para no poner try
                    element.draw(screen)
                except AttributeError:
                    pass
            for bola2 in bolas:
                Interaction.check_collision(bola1, bola2)

        pygame.display.flip()
        reloj.tick(fps)

    # Cerramos la ventana y salimos.
    # Si te olvidas de esta ultima linea, el programa se 'colgara'
    # al salir si lo hemos estado ejecutando desde el IDLE.
    pygame.quit()
