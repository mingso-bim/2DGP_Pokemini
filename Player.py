from pico2d import *


class Player:
    def __init__(self):
        self.name = "player"
        self.gender = "male"
        self.image = load_image('resource/trainer_boy_sprite.png')
        self.x, self.y = 0, 0
        self.moveable = False
        self.pokemons = []
        self.items = []


    def update(self):
        pass


    def render(self):
        self.image.clip_draw(21, 27, 21, 27, 300, 300)