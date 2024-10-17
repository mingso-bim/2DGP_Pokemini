from pico2d import *

class UI:
    def __init__(self, _x, _y, _width, _height):
        self.image = None
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        self.clickable = False
        self.visible = True
        self.UI = None


    def render(self):
        if self.visible:
            self.image.draw(self.x, self.y, self.width, self.height)


    def handle_event(self):
        pass


    def update(self):
        pass


open_canvas(600, 700)
mainMenuUI = []

# background
background = UI(300, 350, 600, 700)
background.image = load_image('resource/background.png')
mainMenuUI.append(background)

# logo
logo = UI(300, 520, 556, 178)
logo.image = load_image('resource/PokeminiLogo.png')
mainMenuUI.append(logo)

# menu
menu = UI(300, 170, 226, 88)
menu.image = load_image('resource/miniTextbox.png')
mainMenuUI.append(menu)