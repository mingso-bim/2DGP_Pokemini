from pico2d import load_image
from skill import Status
import skill
import game_framework

TIME_PER_ACTION = 1
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 2

class Pokemon:
    image = None
    def __init__(self, _name, _skill1, _skill2):
        self.name = _name
        self.frame = 0
        self.status = [Status.NONE]
        self.skill = [_skill1, _skill2]
        self.level = 1
        self.exp = 0
        self.max_exp = 100
        self.max_pp = 300
        self.cur_pp = self.max_pp
        self.max_hp = 20
        self.cur_hp = self.max_hp
        self.renderXY = []

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


TURTWIG = Pokemon("모부기", skill.QUICK_ATTACK, skill.RAZOR_LEAF)
TURTWIG.renderXY.append(0)
TURTWIG.renderXY.append(346)

CHIKORITA = Pokemon("이상해씨", skill.CUTTING_GRASS, skill.BRANCH_POKE)
CHIKORITA.renderXY.append(0)
CHIKORITA.renderXY.append(460 - 229)

PIPLUP = Pokemon("팽도리", skill.TACKLE, skill.WATER_CANNONS)
PIPLUP.renderXY.append(244)
PIPLUP.renderXY.append(460 - 114)

PSYDUCK = Pokemon("고라파덕", skill.TACKLE, skill.HYDROCANNON)
PSYDUCK.renderXY.append(244)
PSYDUCK.renderXY.append(460 - 229)

CHIMCHAR = Pokemon("불꽃숭이", skill.QUICK_ATTACK, skill.EMBER)
CHIMCHAR.renderXY.append(0)
CHIMCHAR.renderXY.append(460 - 344)

CHARMANDER = Pokemon("파이리", skill.TACKLE, skill.INCINERATE)
CHARMANDER.renderXY.append(244)
CHARMANDER.renderXY.append(460 - 344)

PIKACHU = Pokemon("피카츄", skill.QUICK_ATTACK, skill.THUNDERBOLT)
PIKACHU.renderXY.append(0)
PIKACHU.renderXY.append(1)

PACHIRISU = Pokemon("파치리스", skill.TACKLE, skill.ELECTROBALL)
PACHIRISU.renderXY.append(245)
PACHIRISU.renderXY.append(1)

pokemons = (TURTWIG, CHIKORITA, PIPLUP, PSYDUCK, CHIMCHAR, CHARMANDER, PIKACHU, PACHIRISU)




