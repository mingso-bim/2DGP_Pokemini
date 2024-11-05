from pico2d import *
from stateMachine import *
from state import *

class Player:
    def __init__(self):
        self.name = "player"
        self.gender = None
        self.image = None
        self.width, self.height = 0, 0
        self.frame = 1
        self.x, self.y = 300, 500
        self.dir = 1
        self.speed = 1
        self.moveable = False
        self.pokemons = []
        self.items = []
        self.stateMachine = StateMachine(self)
        self.stateMachine.start(Idle)
        self.stateMachine.setTransitions(
            {
                Idle: { rightDown: Run, rightUp: Run, leftDown: Run, leftUp: Run,
                        upDown: Run, upUp: Run, downDown: Run, downUp: Run },
                Run: { rightDown: Idle, rightUp: Idle, leftDown: Idle, leftUp: Idle,
                        upDown: Idle, upUp: Idle, downDown: Idle, downUp: Idle }

            }
        )


    def setGender(self, _gender):
        self.gender = _gender
        if _gender == "male":
            self.image = load_image("resource/trainer_boy_sprite.png")
            self.width = 21
            self.height = 27
        elif _gender == 'female':
            self.image = load_image("resource/trainer_girl_sprite.png")
            self.width = 31
            self.height = 30


    def setDebugMode(self):
        self.setGender('female')
        self.moveable = True


    def update(self):
        self.stateMachine.update()


    def render(self):
        self.stateMachine.render()


    def handle_events(self, e):
        self.stateMachine.addEvent(('INPUT', e))

p = Player()