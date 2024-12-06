from pico2d import draw_rectangle
import pokemon
import random


class Bush:
    def __init__(self, x, y):
        self.pokemons = []
        self.pokemons.append(pokemon.pokemons[random.randint(0, 7)])
        self.x, self.y = x, y
        self.battle = False
        # 불러올때 모든 부시 False로 바꾸기 필요

    def update(self):
        pass

    def render(self):
        draw_rectangle(*self.get_bb())

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def handle_event(self):
        pass

    def handle_collision(self, group, other):
        if group == 'player:bush':
            pass