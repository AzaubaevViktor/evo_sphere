import pygame
import sys


class Action:
    def __call__(self, *args, **kwargs):
        pass


class Exit(Action):
    def __call__(self, *args, **kwargs):
        sys.exit()


class Move(Action):
    def __init__(self, dx, dy):
        self.dx, self.dy = (dx, dy)


class PyGameController:
    def __init__(self):
        pygame.key.set_repeat(10, 100)

    def actions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: yield Exit()

        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_LEFT]: yield Move(-0.0001, 0)
        if pressed[pygame.K_RIGHT]: yield Move(0.0001, 0)
        if pressed[pygame.K_UP]: yield Move(0, 0.01)
        if pressed[pygame.K_DOWN]: yield Move(0, -0.001)


