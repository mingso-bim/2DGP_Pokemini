from pico2d import *
import game_framework
from map import Obstacle
from player import Player
import map
import gameWorld

def init():
    global p

    map.initMap()
    p = gameWorld.p
    gameWorld.addObject(p, 1)

    gameWorld.add_collision_pair('player:obstacle', p, None)
    gameWorld.add_collision_pair('player:portal', p, None)

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
    global startX, startY
    global p
    events = get_events()
    for e in events:
        if (SDL_KEYDOWN, SDLK_ESCAPE) == (e.type, e.key):
            game_framework.quit()
        elif (SDL_KEYDOWN, SDLK_F1) == (e.type, e.key):
            map.saveMap()
            print('saved')
        elif (SDL_KEYDOWN, SDLK_F2) == (e.type, e.key):
            map.loadMap()
            print('loaded')
        elif e.type == SDL_KEYDOWN or e.type == SDL_KEYUP:
            p.handle_events(e)
        elif e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                startX = e.x
                startY = gameWorld.game_height - e.y
            if e.button == SDL_BUTTON_RIGHT:
                for o in map.map_house.obstacles:
                    if 20 > (o.right - o.left) * (o.top - o.bottom):
                        map.map_house.obstacles.remove(o)
                        gameWorld.remove_collision_object(o)
                    if o.left < e.x < o.right:
                        if o.bottom < gameWorld.game_height - e.y < o.top:
                            map.map_house.obstacles.remove(o)
                            gameWorld.remove_collision_object(o)
                            return
        elif e.type == SDL_MOUSEBUTTONUP:
            if e.button == SDL_BUTTON_RIGHT:
                return
            if startX > e.x:
                startX, e.x = e.x, startX
            if startY > gameWorld.game_height - e.y:
                startY, e.y = gameWorld.game_height - e.y, startY
            else:
                e.y = gameWorld.game_height - e.y

            o = Obstacle(startX, startY, e.x, e.y)
            map.map_house.obstacles.append(o)
            gameWorld.add_collision_pair('player:obstacle', None, o)

def pause(): pass
def resume(): pass