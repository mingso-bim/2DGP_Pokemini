from pico2d import *
import game_framework
from map import Obstacle, game_width
import map
import gameWorld
import battle_mode
import pokemon, skill
import trainer
import skill
import effect

def init():
    global p
    global m

    p = gameWorld.p
    p.x, p.y = 300, 450
    p.x, p.y = 527, 127
    p.scrolling = True

    gameWorld.addObject(p, 1)

    m = map.init_road()
    gameWorld.insertObject(m, 0)

    gameWorld.add_collision_pair('player:trainer', p, None)
    gameWorld.add_collision_pair('player:obstacle', p, None)
    gameWorld.add_collision_pair('player:portal', p, None)
    gameWorld.add_collision_pair('player:bush', p, None)

    debugMode()

def debugMode():
    p.setGender('male')
    p.addPokemon(pokemon.TURTWIG)
    p.pokemons[0].addSkill(skill.FIRE_FANG)
    p.pokemons[0].addSkill(skill.THUNDER)
    p.pokemons[0].exp = 15
    #p.pokemons[0].cur_hp = 0

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
            gameWorld.get_map().save_map()
            print('saved')
        elif e.type == SDL_KEYDOWN or e.type == SDL_KEYUP:
            p.handle_events(e)
        elif e.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            gameWorld.get_map().handle_event(e)
            print(f'   click{gameWorld.get_player().x}, {gameWorld.get_player().y}')


def pause(): pass
def resume(): pass