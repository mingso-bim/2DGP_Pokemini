from pico2d import *


class Player:
    def __init__(self):
        self.name = "player"
        self.gender = "female"
        self.image = None
        self.x, self.y = 0, 0
        self.moveable = False
        self.pokemons = []
        self.items = []


    def update(self):
        pass


    def render(self):
        if self.image == None:
            return
        self.image.clip_draw(31, 40, 31, 40, 300, 300)