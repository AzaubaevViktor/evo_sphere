from typing import Tuple

import numpy as np


class Game:
    def __init__(self,
                 count,
                 size=(640, 480),
                 radius=11,
                 friction=0.01,
                 bullet_speed=5
                 ):
        """
        Класс игры
        :param count: Количество существ
        :param size: Размеры экрана (x, y)
        :param radius: Размер создания
        :param friction: Коэффициент трения для передвижения
        :param bullet_speed: Скорость пули за шаг времени
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

        # Cooldown на выстрел
        self.cooldowns = np.zeros((count, 1))
        self.cooldown = 10

        # Пули
        self._bullet_speed = bullet_speed
        self.bullets_speed = np.zeros((0, 2))
        self.bullets = np.zeros((0, 2))
        self.bullets_angle = np.zeros((0, 1))

    def add_bullet(self, _id):
        if self.cooldowns[_id] == 0:
            center = self.coord[_id]
            angle = self.angle[_id]
            vec = np.array((np.cos(angle), np.sin(angle))).flatten(0)
            vec_p = vec[::-1].flatten(0)
            vec_p[0] = - vec_p[0]
            bullets = [
                center + (vec_p + vec) * self.radius,
                center + (-vec_p + vec) * self.radius
            ]

            for bullet in bullets:
                self.bullets = np.vstack((self.bullets, bullet))
                self.bullets_angle = np.vstack((self.bullets_angle, [angle]))

            self.cooldowns[_id] = self.cooldown

    def _walls(self, d_time: float):
        # Отражение от левой стены
        self.dist = self.coord - np.full_like(self.coord, self.radius)
        self.dist *= self.dist < 0
        self.accel += np.abs(self.dist) * d_time / self.radius ** 2

        # Отражение от правой стены
        wall = np.full_like(self.coord, self.size[0])
        wall[:, 1] = self.size[1]

        self.dist = wall - self.radius - self.coord
        self.dist *= self.dist < 0
        self.accel -= np.abs(self.dist) * d_time / self.radius ** 2

    def _move(self, d_time: float):
        # Apply
        self.speed *= (1 - self.friction * d_time)
        self.speed += self.accel * d_time
        self.coord += self.speed * d_time

        self.angle_speed *= (1 - self.friction * d_time)
        self.angle_speed += self.angle_accel * d_time
        self.angle += self.angle_speed * d_time

    def _bullets(self, d_time: float):
        # Bullets
        self.bullets_speed = np.zeros_like(self.bullets)
        self.bullets_speed[:, 0] = np.cos(self.bullets_angle).flatten()
        self.bullets_speed[:, 1] = np.sin(self.bullets_angle).flatten()

        self.bullets += self.bullets_speed * d_time * self._bullet_speed

        droped = (self.bullets[:, 0] < 0) + (self.bullets[:, 1] < 0) + \
                 (self.bullets[:, 0] > self.size[0]) + (
                         self.bullets[:, 1] > self.size[1])
        droped = droped.reshape((len(droped), 1))
        droped = droped.nonzero()[0]

        self.bullets = np.delete(self.bullets, droped, 0)
        self.bullets_angle = np.delete(self.bullets_angle, droped, 0)

        # Cooldowns
        self.cooldowns -= d_time
        self.cooldowns *= self.cooldowns > 0

    def _drop_accel(self, d_time: float):
        # Drop
        self.accel.fill(0)
        self.angle_accel.fill(0)

    def step(self, d_time: float):
        """
        Шаг симуляции
        :param d_time: Шаг времени
        :return:
        """
        self._walls(d_time)
        self._move(d_time)
        self._bullets(d_time)

        self._drop_accel(d_time)
