from enum import *
from Skill import Status, AllAttackSkills

class Pokemon:
    def __init__(self, _name, _skill1, _skill2):
        self.name = _name
        self.status = {Status.NONE}
        self.skill = [_skill1, _skill2]

    def addSkill(self):
        pass

    def UseSkill(self):
        pass

TURTWIG = Pokemon("모부기", AllAttackSkills.QUICK_ATTACK, AllAttackSkills.RAZOR_LEAF)
BULBASAUR = Pokemon("이상해씨", AllAttackSkills.CUTTING_GRASS, AllAttackSkills.BRANCH_POKE)

PIPLUP = Pokemon("팽도리", AllAttackSkills.TACKLE, AllAttackSkills.WATER_CANNONS)
PSYDUCK = Pokemon("고라파덕", AllAttackSkills.TACKLE, AllAttackSkills.HYDROCANNON)  

CHIMCHAR = Pokemon("불꽃숭이", AllAttackSkills.QUICK_ATTACK, AllAttackSkills.EMBER)
CHARMANDER = Pokemon("파이리", AllAttackSkills.TACKLE, AllAttackSkills.INCINERATE)

PIKACHU = Pokemon("피카츄", AllAttackSkills.QUICK_ATTACK, AllAttackSkills.THUNDERBOLT)
EMOLGA = Pokemon("에몽가", AllAttackSkills.TACKLE, AllAttackSkills.ELECTROBALL)

pokemons = (TURTWIG, BULBASAUR, PIPLUP, PSYDUCK, CHIMCHAR, CHARMANDER, PIKACHU, EMOLGA)




