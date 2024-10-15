from pico2d import *
from Player import Player
from map import *

def Initialization():
    global gameStatus
    global world
    global player

    # 0-main menu
    gameStatus = 0
    world = []

    player = Player()
    world.append(player)


def Update():
    for obj in world:
        obj.update()


def Render():
    if gameStatus == 0:
        RenderMainMenu()


def Handle_event():
    pass


Initialization()
open_canvas(500, 600)

while True:
    Update()
    Render()

close_canvas()