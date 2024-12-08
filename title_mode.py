from pico2d import *
import effect
import gameWorld
import game_framework
from UI import UI, Text
import intro_mode, play_mode

game_width, game_height = 600, 700

def init():
    global select
    select = 0

    global main_background, main_logo, main_menu, newText, continueText, arrow, sound_button, music
    # background
    main_background = UI(game_width / 2, game_height / 2, game_width, game_height)
    main_background.image = load_image('resource/background.png')
    gameWorld.addObject(main_background, 0)

    # logo
    main_logo = UI(game_width / 2, game_height * 0.75, 556, 178)
    main_logo.image = load_image('resource/PokeminiLogo.png')
    gameWorld.addObject(main_logo, 1)

    # menu
    main_menu = UI(game_width / 2, game_height * 0.25, 226, 88)
    main_menu.image = load_image('resource/miniTextbox.png')
    gameWorld.addObject(main_menu, 0)

    # text
    newText = Text(game_width * 0.4, game_height * 0.275, '새 모험')
    continueText = Text(game_width * 0.35, game_height * 0.225, '이어서')
    gameWorld.addObject(newText, 1)
    gameWorld.addObject(continueText, 1)

    # arrow
    arrow = UI(game_width * 0.35, game_height * 0.275, 12, 20)
    arrow.image = load_image('resource/intro/select.png')
    gameWorld.addObject(arrow, 1)

    # sound_button
    sound_button = load_wav('resource/sound/button.wav')
    sound_button.set_volume(32)

    # music
    music = load_music('resource/sound/music_title.mp3')
    music.repeat_play()
    music.set_volume(100)

def finish():
    global main_background, main_logo, main_menu, newText, continueText, arrow
    gameWorld.clear()
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
                    effect.b_fade_out()
                    game_framework.change_mode(intro_mode)
            elif select == 1:
                if e.key == SDLK_UP:
                    select = 0
                if e.key == SDLK_SPACE:
                    effect.b_fade_out()
                    gameWorld.p.load()
                    game_framework.change_mode(play_mode)



def pause(): pass
def resume(): pass