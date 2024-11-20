from pico2d import *
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
        self.prevX, self.prevY = 0, 0
        self.dirX, self.dirY, self.dir = 1, 1, 0
        self.speed = RUN_SPEED_PPS
        self.visible = True
        self.pokemons = []
        self.items = []
        self.stateMachine = StateMachine(self)
        self.stateMachine.start(Idle)
        self.stateMachine.setTransitions(
            {
                Idle: { rightDown: RunX, rightUp: RunX, leftDown: RunX, leftUp: RunX,
                        upDown: RunY, upUp: RunY, downDown: RunY, downUp: RunY },
                RunX: { rightDown: Idle, rightUp: Idle, leftDown: Idle, leftUp: Idle,
                        upDown: RunX, upUp: RunX, downDown: RunX, downUp: RunX },
                RunY: { rightDown: RunY, rightUp: RunY, leftDown: RunY, leftUp: RunY,
                        upDown: Idle, upUp: Idle, downDown: Idle, downUp: Idle }
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