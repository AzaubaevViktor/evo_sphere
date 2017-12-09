import numpy as np


class Game:
    def __init__(self,
                 count,
                 size=(640, 480),
                 radius=11,
                 friction=0.01
                 ):
        """
        Класс игры
        :param count: Количество существ
        :param size: Размеры экрана (x, y)
        :param radius: Размер создания
        :param friction: Коэффициент трения
        """
        self.radius = radius
        self.size = size
        self.count = count
        self.friction = friction

        # Положение
        self.coord = np.zeros((count, 2))
        self.speed = np.zeros((count, 2))
        self.accel = np.zeros((count, 2))

        # Угол
        self.angle = np.zeros((count, 1))
        self.angle_speed = np.zeros((count, 1))
        self.angle_accel = np.zeros((count, 1))

    def step(self, d_time: float):
        """
        Шаг симуляции
        :param d_time: Шаг времени
        :return:
        """
        # Отражение от левой стены
        self.dist = self.coord - np.full_like(self.coord, self.radius)
        self.dist *= self.dist < 0
        self.accel += np.abs(self.dist) / self.radius ** 2

        # Отражение от правой стены
        wall = np.full_like(self.coord, self.size[0])
        wall[:, 1] = self.size[1]

        self.dist = wall - self.radius - self.coord
        self.dist *= self.dist < 0
        self.accel -= np.abs(self.dist) / self.radius ** 2

        # Apply
        self.speed *= (1 - self.friction * d_time)
        self.speed += self.accel * d_time
        self.coord += self.speed * d_time

        self.angle_speed *= (1 - self.friction * d_time)
        self.angle_speed += self.angle_accel * d_time
        self.angle += self.angle_speed * d_time

        # Drop
        self.accel.fill(0)
        self.angle_accel.fill(0)



