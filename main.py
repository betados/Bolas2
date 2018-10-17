# -*- coding: utf-8 -*-
import os
import sys
from random import randrange

import pygame
from vector_2d import Vector

from objects import Bola, Rect
from rigidBodies import LineObject, RoundBody
from interaction import Interaction
from decimal import Decimal

if __name__ == "__main__":
    if sys.platform == 'win32' or sys.platform == 'win64':
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    reloj = pygame.time.Clock()

    resolution = (Decimal(1050), Decimal(600))
    Interaction.set_screen_height(resolution[1])
    pygame.display.set_caption('Bolas')
    screen = pygame.display.set_mode(resolution, pygame.SRCALPHA, 32)

    done = False
    fps = 120

    owned_bola = None
    owned_platform = None
    bolas_number = 5
    bolas = [
        Bola(
            color=[randrange(100) for _ in range(3)],
            pos=(randrange(resolution[0]), randrange(resolution[1])),
            radio=randrange(10, 30),
        ) for _ in range(bolas_number)
    ]
    floor = LineObject((0, resolution[1]), resolution)
    # floor = LineObject((0, resolution[1]), (resolution[0], resolution[1]-50), static=True)
    ceiling = LineObject((resolution[0], 0), (0, 0))
    walls = (LineObject((0, 0), (0, resolution[1])),
             LineObject(resolution, (resolution[0], 0)),
             )

    platform1 = Rect((100, 0, 0), (300, resolution[1] - 300, 600, 60))
    platform2 = Rect((0, 10, 0), (100, resolution[1] - 100, 600, 50))
    platforms = [
        platform1,
        # platform2,
    ]
    box = (floor, ceiling) + walls
    mouse = RoundBody((0, 0))

    while not done:
        screen.fill((0, 0, 0, 255))
        time = Decimal(reloj.get_time())

        events = pygame.event.get()
        keys = pygame.key.get_pressed()

        if time:
            mouse.v = Vector(*pygame.mouse.get_rel()) / time
        mouse.pos = Vector(*pygame.mouse.get_pos())
        if pygame.mouse.get_pressed()[0]:
            if owned_bola:
                owned_bola.v = mouse.v
            if owned_platform:
                owned_platform.append_force(owned_platform.click_point_on_platform - owned_platform.pos,
                                            mouse.pos - owned_platform.click_point_on_platform)
                p_list = [owned_platform.pos, owned_platform.click_point_on_platform, mouse.pos]
                pygame.draw.lines(screen, (0, 200, 0), False, [[p.x, p.y] for p in p_list])

        for event in events:
            if event.type == pygame.QUIT:
                done = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bola in bolas:
                    if Interaction.is_clicked(bola, mouse):
                        owned_bola = bola
                        break
                for platform in platforms:
                    if Interaction.is_clicked(platform, mouse):
                        owned_platform = platform
                        owned_platform.click_point_on_platform = mouse.pos
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                owned_bola = None
                owned_platform = None

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
            for platform in platforms:
                Interaction.check_collision(bola1, platform)
            for bola2 in bolas:
                # TODO recorrer solo la mitad de las bolas y en la interacción aplicar fuerzas a las dos
                Interaction.check_collision(bola1, bola2)

        for platform_i in platforms:
            for platform_j in platforms:
                # TODO recorrer solo la mitad de las plataformas y en la interacción aplicar fuerzas a las dos
                Interaction.check_collision(platform_i, platform_j)
            platform_i.actualize(time)
            platform_i.draw(screen)

        pygame.display.flip()
        reloj.tick(fps)

    # Cerramos la ventana y salimos.
    # Si te olvidas de esta ultima linea, el programa se 'colgara'
    # al salir si lo hemos estado ejecutando desde el IDLE.
    pygame.quit()
