from pico2d import draw_rectangle, load_image
import battle_mode
import game_framework
import pokemon
from pokemon import pokemons
import ending_mode


class Trainer:
    def __init__(self):
        self.name = '바람'
        self.image = load_image('resource/friend.png')
        self.w, self.h = 29, 31
        self.frame = 0
        self.x, self.y = 560, 30
        self.dir = 2
        self.ending = False
        self.pokemons = []
        self.pokemons.append(pokemon.CHIMCHAR)
        self.pokemons[0].level = 6
        self.sx, self.sy = 0, 0
        self.visible = True

    def get_bb(self):
        return self.x - 70, self.y - 20, self.x + 20, self.y + 20

    def render(self):
        if not self.visible:
            return
        self.image.clip_draw(self.frame * self.w, self.h * self.dir, self.w, self.h, self.sx, self.sy, self.w * 2, self.h * 2)

    def update(self):
        pass

    def handle_collision(self, group, other):
        if group == 'player:trainer':
            if self.ending:
                return
            ending_mode.trainer = self
            game_framework.push_mode(ending_mode)
