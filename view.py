import numpy as np
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
        pygame.draw.circle(self.field, WHITE, (int(pos[0]), int(pos[1])), int(radius), 1)

    def line(self, a, b):
        pygame.draw.line(self.field, WHITE,
                         (int(a[0]), int(a[1])),
                         (int(b[0]), int(b[1])), 1)

    def render(self):
        # Создание
        for coord, speed_vec in zip(self.game.coord, self.game.angle):
            # Тельце
            coord.reshape(2)
            self.circle(coord, self.game.radius)

            # Ручки
            rad = np.array((
                np.cos(speed_vec[0]) * self.game.radius,
                np.sin(speed_vec[0]) * self.game.radius
            ))
            rad_p = rad[::-1].flatten()
            rad_p[0] = -rad_p[0]

            self.line(coord + rad_p,
                      coord + rad_p + rad)
            self.line(coord - rad_p,
                      coord - rad_p + rad)

        # Пули
        for coord, speed_vec in zip(self.game.bullets, self.game.bullets_speed):
            self.line(coord, coord + speed_vec * 5)



    def update(self):
        self.screen.blit(self.field, (0, 0))
        pygame.display.update()
        self.screen.fill((0, 0, 0))
        self.field.fill((0, 0, 0))

