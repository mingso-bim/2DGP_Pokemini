from enum import *

class Type(Enum):
    NONE = 1
    NORMAL = 2
    WATER = 3
    FIRE = 4
    GRASS = 5
    ELECTR = 8
    POISON = 9


class Status(Enum):
    NONE = 1
    POISON = 2
    BURN = 3
    PARALYSIS = 4


# 분류 위력 명중 PP 상태이상
class Skill:
    def __init__(self, _attack, _hitRate, _Type, _pp, _statusChange):
        self.attack = _attack
        self.hitRate = _hitRate
        self.type = _Type
        self.power = 1
        self.pp = _pp
        self.statusChange = _statusChange


class AllAttackSkills(Enum):
    # TYPE NORMAL
    #몸통박치기
    TACKLE = Skill(40, 100, Type.NORMAL, 35, Status.NONE)
    #전광석화
    QUICK_ATTACK = Skill(40, 100, Type.NORMAL, 30, Status.NONE)
    #풀베기
    CUTTING_GRASS = Skill(50, 95, Type.NORMAL, 30, Status.NONE)

    # TYPE WATER
    #물대포
    WATER_CANNONS = Skill(40, 100, Type.WATER, 25, Status.NONE)
    #하이드로캐논
    HYDROCANNON = Skill(150, 90, Type.WATER, 30, Status.NONE)
    #바다회오리
    SEA_TORNADO = Skill(85, 85, Type.WATER, 15, Status.NONE)

    # TYPE FIRE
    #불꽃세례
    EMBER = Skill(40, 100, Type.FIRE, 25, Status.BURN)
    #불꽃엄니
    FIRE_FANG = Skill(65, 95, Type.FIRE, 15, Status.NONE)
    #불태우기
    INCINERATE = Skill(60, 100, Type.FIRE, 30, Status.BURN)

    # TYPE GRASS
    #잎날가르기
    RAZOR_LEAF = Skill(55, 95, Type.GRASS, 25, Status.NONE)
    #가지찌르기
    BRANCH_POKE = Skill(40, 100, Type.GRASS, 40, Status.NONE)
    #씨폭탄
    SEED_BOMB = Skill(80, 100, Type.GRASS, 15, Status.NONE)

    # TYPE ELECTR
    #10만볼트
    THUNDERBOLT = Skill(90, 75, Type.ELECTR, 15, Status.PARALYSIS)
    #번개
    THUNDER = Skill(110, 60, Type.ELECTR, 35, Status.NONE)
    #일렉트릭볼
    ELECTROBALL = Skill(70, 85, Type.ELECTR, 15, Status.NONE)

    # TYPE POISON
    #독침
    POISON_STING = Skill(40, 100, Type.POISON, 35, Status.POISON)
    #독찌르기
    POSION_JAB = Skill(80, 100, Type.POISON, 20, Status.POISON)
    #스모그
    SMOG = Skill(30, 70, Type.POISON, 10, Status.POISON)
