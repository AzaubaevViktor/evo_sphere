import numpy as np
import time

from controller import PyGameController, Move, Action, Shot
from model import Game
from view import PyGameView

model = Game(2)

view = PyGameView(model)

controller = PyGameController()

start = time.time()
count = 0

while True:
    model.step(1)
    view.render()
    view.update()

    for action in controller.actions():
        if isinstance(action, Move):
            model.accel[0, 0] += action.dy * np.cos(model.angle[0])
            model.accel[0, 1] += action.dy * np.sin(model.angle[0])

            model.angle_accel[0] += action.dx
        if isinstance(action, Shot):
            model.add_bullet(0)
        elif isinstance(action, Action):
            action()

    count += 1

    if time.time() - start > 1:
        print("{:.1f} FPS".format(count / (time.time() - start)))
        count = 0
        start = time.time()

