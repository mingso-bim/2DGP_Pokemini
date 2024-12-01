from pico2d import *
import game_framework
from map import Obstacle, game_width
import map
import gameWorld
import battle_mode
import pokemon, skill
import trainer
import skill

def init():
    global p
    global m

    p = gameWorld.p
    p.x, p.y = 300, 450

    gameWorld.addObject(p, 1)

    m = map.init_road()
    gameWorld.insertObject(m, 0)

    gameWorld.add_collision_pair('player:obstacle', p, None)
    gameWorld.add_collision_pair('player:portal', p, None)
    gameWorld.add_collision_pair('player:trainer', p, None)
    gameWorld.add_collision_pair('player:bush', p, None)

    debugMode()

def debugMode():
    p.setGender('male')
    p.addPokemon(pokemon.PACHIRISU)
    p.pokemons[0].addSkill(skill.FIRE_FANG)
    p.pokemons[0].addSkill(skill.THUNDER)
    p.pokemons[0].exp = 15

    t = trainer.Trainer()
    t.x, t.y = 300, 550
    t.pokemons.append(pokemon.PSYDUCK)
    gameWorld.add_collision_pair('player:trainer', None, t)
    gameWorld.addObject(t, 0)

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
        elif (SDL_KEYDOWN, SDLK_F2) == (e.type, e.key):
            gameWorld.get_player().scrolling = True
            print('scr')
        elif e.type == SDL_KEYDOWN or e.type == SDL_KEYUP:
            p.handle_events(e)
        elif e.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            gameWorld.get_map().handle_event(e)
            print('mouse clicked')
        elif (SDL_KEYDOWN, SDLK_SPACE) == (e.type, e.key):
            gameWorld.get_map().handle_event(e)


def pause(): pass
def resume(): pass