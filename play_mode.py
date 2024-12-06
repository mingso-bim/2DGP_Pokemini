from pico2d import *
import game_framework
import map
import gameWorld
import pokemon, skill
import skill
import effect

def init():
    global p
    global m

    p = gameWorld.p
    gameWorld.addObject(p, 1)

    m = map.init_house()
    gameWorld.insertObject(m, 0)

    gameWorld.add_collision_pair('player:trainer', p, None)
    gameWorld.add_collision_pair('player:obstacle', p, None)
    gameWorld.add_collision_pair('player:portal', p, None)
    gameWorld.add_collision_pair('player:bush', p, None)

    effect.b_fade_in()
    debugMode()

def debugMode():
    p.setGender('female')
    p.addPokemon(pokemon.PIPLUP)
    p.pokemons[0].level = 9
    p.pokemons[0].exp = 5

def finish():
    effect.b_fade_out()
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
            debugMode()
        elif e.type == SDL_KEYDOWN or e.type == SDL_KEYUP:
            p.handle_events(e)
        elif e.type in (SDL_MOUSEBUTTONDOWN, SDL_MOUSEBUTTONUP):
            gameWorld.get_map().handle_event(e)
            print(f'   click{gameWorld.get_player().x}, {gameWorld.get_player().y}')


def pause(): pass
def resume(): pass