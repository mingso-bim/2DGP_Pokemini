import time
from pico2d import *
import pickle
import battle_mode
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
        self.frame = 0
        self.x, self.y = 300, 450
        self.prevX, self.prevY = 200, 200
        self.dirX, self.dirY, self.dir = 1, 1, 0
        self.scrolling = False
        self.speed = RUN_SPEED_PPS
        self.visible = True
        self.moveable = True
        self.pokemons = []
        self.items = []
        self.start_time = 0
        self.stateMachine = StateMachine(self)
        self.stateMachine.start(Idle)
        self.heal_sound = None
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


    def update(self):
        self.stateMachine.update()
        if self.start_time != 0:
            if time.time() - self.start_time > 2.7:
                self.start_time = 0
                self.moveable = True


    def render(self):
        if self.visible == False:
            return
        self.stateMachine.render()

        if self.scrolling:
            sx = self.x - gameWorld.get_map().window_left
            sy = self.y - gameWorld.get_map().window_bottom + gameWorld.get_map().ch
            draw_rectangle(*self.get_bb(sx, sy))
        else:
            draw_rectangle(*self.get_bb())

    def handle_events(self, e):
        if not self.moveable:
            return
        self.stateMachine.addEvent(('INPUT', e))
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_SPACE):
            self.heal()

    def save(self):
        data = Data(self.name, self.gender)
        data.pokemons = self.pokemons

        with open('player.pkl', 'wb') as file:
            pickle.dump(data, file)
            print('saved')

    def load(self):
        with open('player.pkl', 'rb') as file:
            data = pickle.load(file)  # 저장된 객체를 읽어옴
            self.name = data.name
            self.gender = data.gender
            self.pokemons = data.pokemons
            if self.gender == "male":
                self.image = load_image("resource/trainer_boy_sprite.png")
            elif self.gender == 'female':
                self.image = load_image("resource/trainer_girl_sprite.png")
            print(f'loaded: {self.name}, {self.gender}, {self.pokemons}')

    def heal(self):
        if gameWorld.get_map().type != 'house':
            return
        if self.dir != 2:
            return

        al, ab, ar, at = 315 - 10, 551 - 10, 315 + 10, 551 + 10
        bl, bb, br, bt = self.get_bb()

        if al > br: return
        if ar < bl: return
        if at < bb: return
        if ab > bt: return
        print('heal')

        for p in self.pokemons:
            p.cur_hp = p.max_hp
            p.cur_pp = p.max_pp

        if self.heal_sound == None:
            self.heal_sound = load_wav('resource/sound/pokemon_center.wav')
            self.heal_sound.set_volume(32)

        self.heal_sound.play()
        self.start_time = time.time()
        self.moveable = False

        self.save()


    def get_bb(self, locX = None, locY = None):
        if locX and locY:
            return locX - 15, locY - 25, locX + 25, locY + 20
        return self.x - 15, self.y - 25, self.x + 25, self.y + 20


    def handle_collision(self, group, other):
        if group == 'player:obstacle':
            self.x = self.prevX
            self.y = self.prevY

        elif group == 'player:portal':
            pass

        elif group == 'player:trainer':
            if other.ending:
                return

            self.frame = 0
            self.stateMachine.start(Idle)

            if self.pokemons[0].cur_hp <= 0:
                self.x = self.prevX
                self.y = self.prevY
                return

            self.visible = False

        elif group == 'player:bush':
            if not other.battle:
                return
            self.visible = False
            self.stateMachine.start(Idle)
            self.frame = 0

            battle_mode.other = other
            game_framework.push_mode(battle_mode)
            other.battle = True



class Data:
    def __init__(self, _name, _gender):
        self.name = _name
        self.gender = _gender
        self.pokemons = []
