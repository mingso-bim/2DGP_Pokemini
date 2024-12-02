from pico2d import *
import game_framework
from gameWorld import game_height, game_width
from UI import UI, Text
import intro_mode

def init():
    global select
    select = 0

    global main_background, main_logo, main_menu, newText, continueText, arrow, sound_button
    # background
    main_background = UI(game_width / 2, game_height / 2, game_width, game_height)
    main_background.image = load_image('resource/background.png')

    # logo
    main_logo = UI(game_width / 2, game_height * 0.75, 556, 178)
    main_logo.image = load_image('resource/PokeminiLogo.png')

    # menu
    main_menu = UI(game_width / 2, game_height * 0.25, 226, 88)
    main_menu.image = load_image('resource/miniTextbox.png')

    # text
    newText = Text(game_width * 0.4, game_height * 0.275, '새 모험')
    continueText = Text(game_width * 0.35, game_height * 0.225, '이어서')

    # arrow
    arrow = UI(game_width * 0.35, game_height * 0.275, 12, 20)
    arrow.image = load_image('resource/intro/select.png')

    # sound_button
    sound_button = load_wav('resource/sound/button.wav')
    sound_button.set_volume(32)

def finish():
    global main_background, main_logo, main_menu, newText, continueText, arrow
    del main_background, main_logo, main_menu, newText, continueText, arrow

def update():
    global select
    if select == 0:
        newText.x = game_width * 0.38
        continueText.x = game_width * 0.35
        arrow.y = game_height * 0.275

    elif select == 1:
        continueText.x = game_width * 0.38
        newText.x = game_width * 0.35
        arrow.y = game_height * 0.225

def draw():
    clear_canvas()

    main_background.render()
    main_logo.render()
    main_menu.render()
    newText.render()
    continueText.render()
    arrow.render()

    update_canvas()

def handle_events():
    global select, sound_button

    events = get_events()
    for e in events:
        if e.type == SDL_KEYDOWN:
            sound_button.play()
        if e.type == SDL_KEYDOWN and e.key == SDLK_ESCAPE:
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            if select == 0:
                if e.key == SDLK_DOWN:
                    select = 1
                if e.key == SDLK_SPACE:
                    game_framework.change_mode(intro_mode)
            elif select == 1:
                if e.key == SDLK_UP:
                    select = 0


def pause(): pass
def resume(): pass