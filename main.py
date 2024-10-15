from pico2d import *
from Player import Player

def Initialization():
    global world
    global player

    world = []

    player = Player()
    world.append(player)


def Update():
    for obj in world:
        obj.update()


def Render():
    for obj in world:
        obj.render()


def Handle_event():
    pass



Initialization()
open_canvas()

while True:
    Update()
    Render()

close_canvas()