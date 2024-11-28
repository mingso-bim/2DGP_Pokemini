from pico2d import *

import map
from stateMachine import *
from state import *

PIXEL_PER_METER = (30.0 / 1.4)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

class Player:
    def __init__(self):
        self.name = "player"
        self.gender = None
        self.image = None
        self.width, self.height = 0, 0
        self.frame = 1
        self.x, self.y = 280, 500
        self.prevX, self.prevY = 200, 200
        self.dirX, self.dirY, self.dir = 1, 1, 0
        self.speed = RUN_SPEED_PPS
        self.visible = True
        self.pokemons = []
        self.items = []
        self.stateMachine = StateMachine(self)
        self.stateMachine.start(Idle)
        self.stateMachine.setTransitions(
            {
                Idle: {right_down: RunRight, left_down: RunLeft, left_up: RunRight, right_up: RunLeft,
                       upkey_down: RunUp, downkey_down: RunDown, upkey_up: RunDown, downkey_up: RunUp},
                RunRight: {right_up: Idle, left_down: Idle, upkey_down: RunRightUp, upkey_up: RunRightDown,
                           downkey_down: RunRightDown, downkey_up: RunRightUp},
                RunRightUp: {upkey_up: RunRight, right_up: RunUp, left_down: RunUp, downkey_down: RunRight},
                RunUp: {upkey_up: Idle, left_down: RunLeftUp, downkey_down: Idle, right_down: RunRightUp,
                        left_up: RunRightUp, right_up: RunLeftUp},
                RunLeftUp: {right_down: RunUp, downkey_down: RunLeft, left_up: RunUp, upkey_up: RunLeft},
                RunLeft: {left_up: Idle, upkey_down: RunLeftUp, right_down: Idle, downkey_down: RunLeftDown,
                          upkey_up: RunLeftDown, downkey_up: RunLeftUp},
                RunLeftDown: {left_up: RunDown, downkey_up: RunLeft, upkey_down: RunLeft, right_down: RunDown},
                RunDown: {downkey_up: Idle, left_down: RunLeftDown, upkey_down: Idle, right_down: RunRightDown,
                          left_up: RunRightDown, right_up: RunLeftDown},
                RunRightDown: {right_up: RunDown, downkey_up: RunRight, left_down: RunDown, upkey_down: RunRight}
            }
        )
    def addPokemon(self, p):
        self.pokemons.append(p)

    def setGender(self, _gender):
        self.gender = _gender
        if _gender == "male":
            self.image = load_image("resource/trainer_boy_sprite.png")
        elif _gender == 'female':
            self.image = load_image("resource/trainer_girl_sprite.png")
        self.width = 35
        self.height = 39


    def setDebugMode(self):
        self.setGender('female')
        self.moveable = True


    def update(self):
        self.stateMachine.update()


    def render(self):
        if self.visible == False:
            return
        self.stateMachine.render()
        draw_rectangle(*self.get_bb())


    def handle_events(self, e):
        self.stateMachine.addEvent(('INPUT', e))


    def get_bb(self):
        return self.x - 15, self.y - 25, self.x + 25, self.y + 20


    def handle_collision(self, group, other):
        if group == 'player:obstacle':
            self.x = self.prevX
            self.y = self.prevY
        elif group == 'player:portal':
            pass
        elif group == 'player:trainer':
            self.x = self.prevX
            self.y = self.prevY
            if other.battle:
                return
            self.visible = False
            self.stateMachine.start(Idle)
            self.frame = 0

p = Player()
m = map.curMap
