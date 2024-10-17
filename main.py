from idlelib.run import handle_tk_events

from pico2d import *
import Player
from map import *

def Initialization():
    open_canvas(600, 700)
    global running
    global gameStatus
    global world
    global player
    global moving

    running = True
    moving = False
    # 0-main menu
    gameStatus = 0
    world = []

    player = Player.Player()
    world.append(player)


def Update():
    for obj in world:
        obj.update()


def Render():
    clear_canvas()

    if gameStatus == 0:
        RenderMainMenu()

    elif gameStatus == 1:
        for obj in world:
            obj.render()

def Handle_event():
    global running, gameStatus
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_RSHIFT:
            gameStatus = 1
        else:
            player.handle_event(event)


Initialization()

while running:
    Update()
    Render()
    Handle_event()

close_canvas()