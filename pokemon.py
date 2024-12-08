from random import randint

from pico2d import load_image
from skill import Status
import skill
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Pokemon:
    image = None
    def __init__(self, _name, _skill1, _skill2, _type):
        self.type = _type
        self.name = _name
        self.frame = 0
        self.status = [Status.NONE]
        self.skill = [_skill1, _skill2]
        self.level = 1
        self.exp = 0
        self.max_exp = 20
        self.drop_exp = randint(14, 20)
        self.max_pp = 300
        self.cur_pp = self.max_pp
        self.max_hp = 20
        self.cur_hp = self.max_hp
        self.status_turn = 0
        self.renderXY = []

    def level_up(self):
        self.max_hp += 4

    def addSkill(self, s):
        if len(self.skill) == 4:
            return
        self.skill.append(s)

    def useSkill(self, s):
        self.cur_pp -= self.skill[s].pp
        return self.skill[s]

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 2


    def render(self, type, x, y):
        if Pokemon.image == None:
            Pokemon.image = load_image('resource/pokemons.png')

        if type == 'f':
            Pokemon.image.clip_draw(self.renderXY[0] + int(self.frame) * 81, self.renderXY[1], 80, 80, x, y, 160, 160)
        elif type == 'b':
            Pokemon.image.clip_draw(self.renderXY[0] + 163, self.renderXY[1], 80, 80, x, y, 160, 160)
        elif type == 'm':
            Pokemon.image.clip_draw(self.renderXY[0] + 178, self.renderXY[1] + 81, 32, 32, x, y, 64, 64)


TURTWIG = Pokemon("모부기", skill.QUICK_ATTACK, skill.RAZOR_LEAF, skill.Type.GRASS)
TURTWIG.renderXY.append(0)
TURTWIG.renderXY.append(346)

CHIKORITA = Pokemon("치코리타", skill.CUTTING_GRASS, skill.BRANCH_POKE, skill.Type.GRASS)
CHIKORITA.renderXY.append(0)
CHIKORITA.renderXY.append(460 - 229)

PIPLUP = Pokemon("팽도리", skill.TACKLE, skill.WATER_CANNONS, skill.Type.WATER)
PIPLUP.renderXY.append(244)
PIPLUP.renderXY.append(460 - 114)

PSYDUCK = Pokemon("고라파덕", skill.TACKLE, skill.HYDROCANNON, skill.Type.WATER)
PSYDUCK.renderXY.append(244)
PSYDUCK.renderXY.append(460 - 229)

CHIMCHAR = Pokemon("불꽃숭이", skill.QUICK_ATTACK, skill.EMBER, skill.Type.FIRE)
CHIMCHAR.renderXY.append(0)
CHIMCHAR.renderXY.append(460 - 344)

CHARMANDER = Pokemon("파이리", skill.TACKLE, skill.INCINERATE, skill.Type.FIRE)
CHARMANDER.renderXY.append(244)
CHARMANDER.renderXY.append(460 - 344)

PIKACHU = Pokemon("피카츄", skill.QUICK_ATTACK, skill.THUNDERBOLT, skill.Type.ELECTR)
PIKACHU.renderXY.append(0)
PIKACHU.renderXY.append(1)

PACHIRISU = Pokemon("파치리스", skill.TACKLE, skill.ELECTROBALL, skill.Type.ELECTR)
PACHIRISU.renderXY.append(245)
PACHIRISU.renderXY.append(1)

pokemons = (TURTWIG, CHIKORITA, PIPLUP, PSYDUCK, CHIMCHAR, CHARMANDER, PIKACHU, PACHIRISU)




