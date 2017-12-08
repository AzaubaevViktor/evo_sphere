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



