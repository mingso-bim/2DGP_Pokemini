from pico2d import *
import player
import mainMenu
import map
import intro
import gameWorld


def initialization():
    global running
    global gameStatus
    global intro, mainMenuUI

    running = True

    p = player.Player()
    gameWorld.addObject(player, 1)

    intro = intro.Intro(p)
    mainMenuUI = mainMenu.MainMenu(intro)

    m = map.Map()
    gameWorld.addObject(map, 0)

    pad = map.TouchPad()
    gameWorld.addObject(pad, 0)

def update():
    if intro.enable:
        intro.update()
    elif mainMenuUI.enable:
        mainMenuUI.update()
    else:
        gameWorld.update()

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
        gameWorld.render()
        update_canvas()


def Handle_event():
    global running, gameStatus
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
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