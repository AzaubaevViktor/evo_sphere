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
        pass

    def actions(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: yield Exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: yield Move(-1, 0)
                if event.key == pygame.K_RIGHT: yield Move(1, 0)
                if event.key == pygame.K_UP: yield Move(0, -1)
                if event.key == pygame.K_DOWN: yield Move(0, 1)
