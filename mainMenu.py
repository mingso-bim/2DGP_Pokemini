from pico2d import *
from UI import *

open_canvas(game_width, game_height)
mainMenuUI = []

# background
main_background = UI(game_width/2, game_height/2, game_width, game_height)
main_background.image = load_image('resource/background.png')
mainMenuUI.append(main_background)

# logo
main_logo = UI(game_width/2, game_height*0.75, 556, 178)
main_logo.image = load_image('resource/PokeminiLogo.png')
mainMenuUI.append(main_logo)

# menu
main_menu = UI(game_width/2, game_height*0.25, 226, 88)
main_menu.image = load_image('resource/miniTextbox.png')
mainMenuUI.append(main_menu)



###


introUI = []

#background
intro_background = UI(game_width/2, game_height/2, game_width, game_height)
intro_background.image = load_image('resource/intro/intro_background.png')
introUI.append(intro_background)
