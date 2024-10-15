from pico2d import *

def RenderMainMenu():
    background = load_image('resource/background.png')
    background.draw(250, 300, 500, 600)

    logo = load_image('resource/PokeminiLogo.png')
    logo.draw(250, 460, 430, 150)
    update_canvas()

