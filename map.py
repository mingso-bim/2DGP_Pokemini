from pico2d import *

def RenderMainMenu():
    background = load_image('resource/background.png')
    background.draw(300, 350, 600, 700)

    logo = load_image('resource/PokeminiLogo.png')
    logo.draw(300, 520)
    update_canvas()

