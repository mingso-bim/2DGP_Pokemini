from pico2d import *
import Player
from map import *
from UI import *

def initialization():
    global running
    global gameStatus
    global world
    global player
    global moving

    running = True
    moving = False

    gameStatus = 0      # 0-main menu
    world = []

    player = Player.Player()
    world.append(player)


def update():
    for obj in world:
        obj.update()


def render():
    clear_canvas()

    if gameStatus == 0:
        for obj in mainMenuUI:
            obj.render()
            update_canvas()

    elif gameStatus == 1:
        for obj in world:
            obj.render()
            update_canvas()

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


initialization()

while running:
    update()
    render()
    Handle_event()

close_canvas()