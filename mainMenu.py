from pico2d import *
from UI import *

open_canvas(game_width, game_height)

class MainMenu:
    def __init__(self, _intro):
        self.enable = True
        self.select = 0
        self.objs = []
        self.intro = _intro

        # background
        main_background = UI(game_width/2, game_height/2, game_width, game_height)
        main_background.image = load_image('resource/background.png')
        self.objs.append(main_background)
        
        # logo
        main_logo = UI(game_width/2, game_height*0.75, 556, 178)
        main_logo.image = load_image('resource/PokeminiLogo.png')
        self.objs.append(main_logo)
        
        # menu
        main_menu = UI(game_width/2, game_height*0.25, 226, 88)
        main_menu.image = load_image('resource/miniTextbox.png')
        self.objs.append(main_menu)
        
        # text
        newText = Text(game_width * 0.4, game_height * 0.275, '새 모험')
        self.objs.append(newText)
        continueText = Text(game_width * 0.35, game_height * 0.225, '이어서')
        self.objs.append(continueText)

        # arrow
        arrow = UI(game_width * 0.35, game_height * 0.275, 12, 20)
        arrow.image = load_image('resource/intro/select.png')
        self.objs.append(arrow)

    def gameStart(self):
        self.enable = False
        self.intro.enable = True

    def handle_event(self, e):
        if e.type == SDL_KEYDOWN:
            if self.select == 0:
                if e.key == SDLK_DOWN:
                    self.select = 1
                if e.key == SDLK_SPACE:
                    self.gameStart()
            elif self.select == 1:
                if e.key == SDLK_UP:
                    self.select = 0

    def update(self):
        if self.select == 0:
            self.objs[3].x = game_width * 0.38
            self.objs[4].x = game_width * 0.35
            self.objs[5].y = game_height * 0.275

        elif self.select == 1:
            self.objs[4].x = game_width * 0.38
            self.objs[3].x = game_width * 0.35
            self.objs[5].y = game_height * 0.225