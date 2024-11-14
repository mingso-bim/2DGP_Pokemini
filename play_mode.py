from pico2d import *
import game_framework
from player import Player
from map import Map
import gameWorld

def init():
    global p

    p = gameWorld.p
    gameWorld.addObject(p, 1)

    map = Map()
    gameWorld.addObject(map, 0)

    gameWorld.add_collision_pair('player:obstacle', p, map.obstacles[0])

    debugMode()

def debugMode():
    p.setGender('male')

def finish():
    gameWorld.clear()

def update():
    gameWorld.update()
    gameWorld.handle_collisions()

def draw():
    clear_canvas()
    gameWorld.render()
    update_canvas()

def handle_events():
    global p
    events = get_events()
    for e in events:
        if (SDL_KEYDOWN, SDLK_ESCAPE) == (e.type, e.key):
            game_framework.quit()
        else:
            p.handle_events(e)

def pause(): pass
def resume(): pass
