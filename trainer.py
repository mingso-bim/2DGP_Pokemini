from pico2d import draw_rectangle
import battle_mode
import game_framework


class Trainer:
    def __init__(self):
        self.name = None
        self.image = None
        self.width, self.height = 0, 0
        self.frame = 0
        self.x, self.y = 280, 500
        self.dir = 1
        self.battle = False
        self.exp = 10
        self.pokemons = []

    def addPokemon(self, p):
        self.pokemons.append(p)

    def get_bb(self):
        return self.x - 20, self.y - 20, self.x + 20, self.y + 20

    def render(self):
        draw_rectangle(*self.get_bb())

    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'player:trainer':
            if self.battle:
                return
            battle_mode.other = self
            game_framework.push_mode(battle_mode)
            self.battle = True

