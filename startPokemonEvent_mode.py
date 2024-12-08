from pico2d import *
import map
import gameWorld
import game_framework
import play_mode
import pokemon
import effect

game_width, game_height = 600, 700

class Pokeball:
    def __init__(self, p):
        self.pokeball = load_image('resource/pokeball.png')
        self.pokemon = load_image('resource/pokemons.png')
        self.name = p

    def draw(self, x, y):
        if self.name == 'TURTWIG':
            self.pokemon.clip_draw(1, 460 - 114, 80, 80, x, y, 160, 160)
        elif self.name == 'PIPLUP':
            self.pokemon.clip_draw(245, 460 - 114, 80, 80, x, y, 160, 160)
        elif self.name == 'CHIMCHAR':
            self.pokemon.clip_draw(1, 460 - 344, 80, 80, x, y, 160, 160)


def renderPokeballs():
    global pokeballs
    scale = 6
    x = game_width * 0.25
    y = game_height * 0.75

    for i in range(0, 3):
        if i % 2 == 0:
            pokeballs[i].pokeball.clip_draw(147, 0, 16, 23, x, y, 16 * (scale - 1), 23 * (scale - 1))
            pokeballs[i].draw(x, y + 15)
        else:
            pokeballs[i].pokeball.clip_draw(147, 0, 16, 23, x, y - 30, 16 * scale, 23 * scale)
            pokeballs[i].draw(x, y - 30)
        x += game_width * 0.25


def init():
    global pokeballs, background, touchpad, sound_button
    pokeballs = [Pokeball('TURTWIG'), Pokeball('PIPLUP'), Pokeball('CHIMCHAR')]

    background = map.Map()
    background.image = load_image('resource/intro/intro_background.png')
    gameWorld.addObject(background, 0)
    touchpad = map.TouchPad()
    gameWorld.addObject(touchpad, 0)
    sound_button = load_wav('resource/sound/button.wav')
    sound_button.set_volume(32)

def finish():
    global background, touchpad
    gameWorld.removeObject(background)
    gameWorld.removeObject(touchpad)

def update():
    gameWorld.update()

def draw():
    global pokeball
    clear_canvas()
    gameWorld.render()
    renderPokeballs()
    update_canvas()

def handle_events():
    global pokeballs, sound_button
    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN:
            sound_button.play()
        if (SDL_KEYDOWN, SDLK_ESCAPE) == (e.type, e.key):
            game_framework.quit()
        elif (SDL_KEYDOWN, SDLK_LEFT) == (e.type, e.key):
            delay(0.1)
            pokeballs[0], pokeballs[1], pokeballs[2] = pokeballs[1], pokeballs[2], pokeballs[0]
        elif (SDL_KEYDOWN, SDLK_RIGHT) == (e.type, e.key):
            delay(0.1)
            pokeballs[0], pokeballs[1], pokeballs[2] = pokeballs[2], pokeballs[0], pokeballs[1]
        elif (SDL_KEYDOWN, SDLK_SPACE) == (e.type, e.key):
            if pokeballs[1].name == 'TURTWIG':
                gameWorld.p.addPokemon(pokemon.TURTWIG)
            elif pokeballs[1].name == 'PIPLUP':
                gameWorld.p.addPokemon(pokemon.PIPLUP)
            elif pokeballs[1].name == 'CHIMCHAR':
                gameWorld.p.addPokemon(pokemon.CHIMCHAR)

            effect.b_fade_out()
            game_framework.pop_mode()


def pause(): pass
def resume(): pass