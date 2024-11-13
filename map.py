from pico2d import *
from gameWorld import game_width, game_height


class Map:
    house = None

    def __init__(self):
        Map.house = load_image('resource/map/house.png')
        self.curImage = self.house

    def render(self):
        self.curImage.draw(game_width * 0.5, game_height * 0.75, game_width, game_height * 0.5)

    def update(self):
        pass

    def handle_event(self, e):
        pass


class TouchPad:
    def __init__(self):
        self.image = load_image('resource/touchPad.png')

    def render(self):
        self.image.draw(game_width * 0.5, game_height * 0.25, game_width, game_height * 0.5)

    def update(self):
        pass

    def handle_event(self, e):
        pass