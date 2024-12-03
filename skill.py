from enum import *

class Type(Enum):
    NONE = 1
    NORMAL = 2
    WATER = 3
    FIRE = 4
    GRASS = 5
    ELECTR = 6
    POISON = 7


class Status(Enum):
    NONE = 1
    POISON = 2
    BURN = 3
    PARALYSIS = 4


# 분류 위력 명중 PP 상태이상
class Skill:
    def __init__(self, _name, _attack, _hitRate, _Type, _pp, _statusChange):
        self.name = _name
        self.attack = _attack
        self.hitRate = _hitRate
        self.type = _Type
        self.power = 1
        self.pp = _pp
        self.statusChange = _statusChange

advantage = {Type.FIRE: Type.GRASS, Type.WATER: Type.FIRE, Type.GRASS: Type.WATER, Type.ELECTR: Type.WATER, Type.POISON: Type.GRASS}
disadvantage = {Type.FIRE: Type.WATER, Type.WATER: Type.GRASS, Type.GRASS: Type.FIRE, Type.ELECTR: Type.GRASS}

# TYPE NORMAL
#몸통박치기
TACKLE = Skill('몸통박치기', 40, 100, Type.NORMAL, 35, Status.NONE)
#전광석화
QUICK_ATTACK = Skill('전광석화', 40, 100, Type.NORMAL, 30, Status.NONE)
#풀베기
CUTTING_GRASS = Skill('풀베기', 50, 95, Type.NORMAL, 30, Status.NONE)
#버둥거리기
STRUGGLING = Skill('버둥거리기', 30, 90, Type.NORMAL, 0, Status.NONE)

# TYPE WATER
#물대포
WATER_CANNONS = Skill('물대포', 40, 100, Type.WATER, 25, Status.NONE)
#하이드로캐논
HYDROCANNON = Skill('하이드로캐논', 120, 70, Type.WATER, 30, Status.NONE)
#바다회오리
SEA_TORNADO = Skill('바다회오리', 85, 85, Type.WATER, 15, Status.NONE)

# TYPE FIRE
#불꽃세례
EMBER = Skill('불꽃세례', 40, 100, Type.FIRE, 25, Status.BURN)
#불꽃엄니
FIRE_FANG = Skill('불꽃엄니', 65, 95, Type.FIRE, 15, Status.NONE)
#불태우기
INCINERATE = Skill('불태우기', 60, 100, Type.FIRE, 30, Status.BURN)

# TYPE GRASS
#잎날가르기
RAZOR_LEAF = Skill('잎날가르기', 55, 95, Type.GRASS, 25, Status.NONE)
#가지찌르기
BRANCH_POKE = Skill('가지찌르기', 40, 100, Type.GRASS, 40, Status.NONE)
#씨폭탄
SEED_BOMB = Skill('씨폭탄', 80, 100, Type.GRASS, 15, Status.NONE)

# TYPE ELECTR
#10만볼트
THUNDERBOLT = Skill('10만볼트', 90, 75, Type.ELECTR, 15, Status.PARALYSIS)
#번개
THUNDER = Skill('번개', 110, 60, Type.ELECTR, 35, Status.NONE)
#일렉트릭볼
ELECTROBALL = Skill('일렉트릭볼', 70, 85, Type.ELECTR, 15, Status.NONE)

# TYPE POISON
#독침
POISON_STING = Skill('독침', 40, 100, Type.POISON, 35, Status.POISON)
#독찌르기
POSION_JAB = Skill('독찌르기', 80, 100, Type.POISON, 20, Status.POISON)
#스모그
SMOG = Skill('스모그', 30, 70, Type.POISON, 10, Status.POISON)
