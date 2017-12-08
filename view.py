import pygame

from model import Game


WHITE = (255, 255, 255)


class PyGameView:
    def __init__(self, game: Game):
        pygame.init()
        self.game = game
        self.screen = pygame.display.set_mode(game.size)
        self.font = pygame.font.SysFont('Courier New', 15)

        self.field = pygame.Surface(game.size, flags=pygame.SRCALPHA)

    def circle(self, pos, radius):
        pygame.draw.circle(self.field, WHITE, pos, radius, 1)

    def render(self):
        for coord in self.game.coord:
            self.circle((int(coord[0]), int(coord[1])), self.game.radius)

    def update(self):
        self.screen.blit(self.field, (0, 0))
        pygame.display.update()
        self.screen.fill((0, 0, 0))
        self.field.fill((0, 0, 0))

