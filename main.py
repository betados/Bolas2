# -*- coding: utf-8 -*-
import os
import sys
from bola import Bola

import pygame

if __name__ == "__main__":
    if sys.platform == 'win32' or sys.platform == 'win64':
        os.environ['SDL_VIDEO_CENTERED'] = '1'

    pygame.init()
    reloj = pygame.time.Clock()

    resolution = (1050, 600)
    pygame.display.set_caption('Bolas')
    screen = pygame.display.set_mode(resolution, pygame.SRCALPHA, 32)

    done = False
    fps = 20
    count = 9999

    bolas = [Bola(resolution) for _ in range(5)]

    while not done:
        screen.fill((0, 0, 0, 255))

        for bola in bolas:
            bola.draw(screen)

        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        mouse = pygame.mouse.get_pressed()

        # count += 1
        # Once a minute:
        # if count > fps * 20:
        #     count = 0

        for event in events:
            if event.type == pygame.QUIT:
                done = True
            # if event.type == pygame.MOUSEBUTTONDOWN:
            # if event.type == pygame.KEYDOWN and keys[pygame.K_c]:
            # if event.type == pygame.KEYDOWN and keys[pygame.K_s]:
            # if event.type == pygame.KEYDOWN and keys[pygame.K_t]:
            # if event.type == pygame.KEYDOWN and keys[pygame.K_TAB]:
        if keys[pygame.K_ESCAPE]:
            done = True

        pygame.display.flip()
        reloj.tick(fps)

    # Cerramos la ventana y salimos.
    # Si te olvidas de esta ultima linea, el programa se 'colgara'
    # al salir si lo hemos estado ejecutando desde el IDLE.
    pygame.quit()
