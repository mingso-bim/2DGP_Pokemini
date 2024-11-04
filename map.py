from pico2d import *
from gameWorld import game_width, game_height


class Map:
    def __init__(self):
        self.house = load_image('resource/map/house.png')
        self.curImage = self.house

    def draw(self):
        self.curImage.draw(0, game_height * 0.5, game_width, game_height * 0.5 )

    def update(self):
        pass

    def handle_event(self, e):
        pass


class TouchPad:
    def __init__(self):
        self.image = load_image('resource/touchPad.png')

    def draw(self):
        self.image.draw(0, 0, game_width, game_height * 0.5)

    def update(self):
        pass

    def handle_event(self, e):
        pass