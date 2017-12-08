import pygame

from controller import PyGameController, Move, Action
from model import Game
from view import PyGameView

model = Game(2)

view = PyGameView(model)

controller = PyGameController()


while True:
    model.step(1)
    view.render()
    view.update()

    for action in controller.actions():
        if isinstance(action, Move):
            model.accel[0, 0] = action.dx
            model.accel[0, 1] = action.dy
        elif isinstance(action, Action):
            action()

