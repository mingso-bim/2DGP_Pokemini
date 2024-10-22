from pico2d import *
import Player
from map import *
from mainMenu import *

def initialization():
    global running
    global gameStatus
    global world
    global player
    global moving
    global intro

    running = True
    moving = False

    gameStatus = 2      # 0-main menu
    world = []

    player = Player.Player()
    world.append(player)


def update():
    for obj in world:
        obj.update()


def render():
    clear_canvas()

    if gameStatus == 0:             # main menu
        for obj in mainMenuUI:
            obj.render()
        update_canvas()

    elif gameStatus == 1:           # in game world
        for obj in world:
            obj.render()
        update_canvas()

    elif gameStatus == 2:
        for obj in introUI:
            obj.render()
        update_canvas()

    print(gameStatus)

def Handle_event():
    global running, gameStatus
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            gameStatus = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F2:
            gameStatus = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F3:
            gameStatus = 2
        else:
            player.handle_event(event)


initialization()

while running:
    update()
    render()
    Handle_event()

close_canvas()