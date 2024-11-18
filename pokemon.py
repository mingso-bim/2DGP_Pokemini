from enum import *
from skill import Status
import skill

class Pokemon:
    def __init__(self, _name, _skill1, _skill2):
        self.name = _name
        self.status = {Status.NONE}
        self.skill = [_skill1, _skill2]
        self.level = 1
        self.exp = 0
        self.max_exp = 100
        self.max_pp = 300
        self.cur_pp = self.max_pp
        self.max_hp = 20
        self.cur_hp = self.max_hp

    def addSkill(self, s):
        self.skill.append(s)

    def UseSkill(self):
        pass

TURTWIG = Pokemon("모부기", skill.QUICK_ATTACK, skill.RAZOR_LEAF)
BULBASAUR = Pokemon("이상해씨", skill.CUTTING_GRASS, skill.BRANCH_POKE)

PIPLUP = Pokemon("팽도리", skill.TACKLE, skill.WATER_CANNONS)
PSYDUCK = Pokemon("고라파덕", skill.TACKLE, skill.HYDROCANNON)  

CHIMCHAR = Pokemon("불꽃숭이", skill.QUICK_ATTACK, skill.EMBER)
CHARMANDER = Pokemon("파이리", skill.TACKLE, skill.INCINERATE)

PIKACHU = Pokemon("피카츄", skill.QUICK_ATTACK, skill.THUNDERBOLT)
PACHIRISU = Pokemon("파치리스", skill.TACKLE, skill.ELECTROBALL)

pokemons = (TURTWIG, BULBASAUR, PIPLUP, PSYDUCK, CHIMCHAR, CHARMANDER, PIKACHU, PACHIRISU)




