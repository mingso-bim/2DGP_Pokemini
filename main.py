from pico2d import *
import Player
import mainMenu
from map import *
import intro

def initialization():
    global running
    global gameStatus
    global world
    global player
    global moving
    global intro
    global mainMenuUI

    running = True
    moving = False

    world = []

    player = Player.Player()
    world.append(player)

    intro = intro.Intro(player)
    mainMenuUI = mainMenu.MainMenu(intro)

def update():
    if intro.enable:
        intro.update()
    elif mainMenuUI.enable:
        mainMenuUI.update()
    else:
        for obj in world:
            obj.update()


def render():
    clear_canvas()

    if intro.enable:
        intro.render()
        update_canvas()

    elif mainMenuUI.enable:
        for obj in mainMenuUI.objs:
            obj.render()
        update_canvas()

    else:
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
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F1:
            gameStatus = 0
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F2:
            gameStatus = 1
        elif event.type == SDL_KEYDOWN and event.key == SDLK_F3:
            gameStatus = 2
        else:
            if mainMenuUI.enable:
                mainMenuUI.handle_event(event)
            elif intro.enable:
                intro.handle_event(event)
            else:
                if event.type in (SDL_KEYDOWN, SDL_KEYUP):
                    player.handle_event(event)


initialization()

while running:
    update()
    render()
    Handle_event()

close_canvas()