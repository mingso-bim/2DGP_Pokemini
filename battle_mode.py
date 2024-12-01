from random import randint
from game_framework import change_mode, pop_mode
from stateMachine import StateMachine
from pico2d import *
import gameWorld
import game_framework
from gameWorld import game_width, game_height
from battle_state import *
from skill import Type, Status
from queue import Queue

other = None

class Battle:
    touchpad = None
    UI = None
    background = None
    font = None
    textbox = None
    meet_script = ('앗! 야생의 ', '(이)가 나타났다!', '가랏! ', '!')
    attack_script = ('의 ', '!')
    counter_script = ('효과가 굉장했다!', '효과가 별로인 듯 하다')
    status_script = ('상대의 몸에 독이 퍼졌다!', '은(는) 독에 의한 데미지를 입었다!',
                     '상대는 화상을 입었다!', '은(는) 화상 데미지를 입었다!',
                     '상대는 마비되어 기술이 나오기 어려워졌다!', '은(는) 몸이 저려서 움직일 수 없다!')


    def __init__(self):
        if Battle.touchpad == None:
            Battle.touchpad = load_image('resource/battleTouchpad.png')
        if Battle.UI == None:
            Battle.UI = load_image('resource/battleUI.png')
        if Battle.background == None:
            Battle.background = load_image('resource/battleBackground.png')
        if Battle.font == None:
            Battle.font = load_font('resource/font.ttf', 40)
        if Battle.textbox == None:
            Battle.textbox = load_image('resource/textbox.png')

        self.select = 0
        self.select_mode = 'main'

        self.player = gameWorld.get_player()
        self.other = other
        self.p_pokemon = self.player.pokemons[0]
        self.o_pokemon = self.other.pokemons[0]

        self.input_enable = False
        self.script_q = Queue()
        self.put_meet_script()
        self.cur_script = self.script_q.get()
        self.turn = 'player'

        self.ending_script = [self.p_pokemon.name + '은(는) 쓰러졌다!', self.cur_script == self.o_pokemon.name + '은(는) 쓰러졌다!',
                              self.p_pokemon.name + '은(는) ' + str(self.o_pokemon.drop_exp) + '경험치를 얻었다!']


    def put_meet_script(self):
        s = '앗 야생의 ' + self.o_pokemon.name + '이(가) 나타났다!'
        self.script_q.put(s)
        s = '가랏! ' + self.p_pokemon.name + '!'
        self.script_q.put(s)


    def put_player_script(self):
        s = self.p_pokemon.name + '은(는) 무엇을 할까?'
        self.script_q.put(s)


    def script_update(self):
        if not self.script_q.empty():
            return

        elif self.turn == 'player':
            self.put_player_script()
        elif self.turn == 'other':
            self.other_attack()

        if self.cur_script == self.p_pokemon.name + '은(는) 무엇을 할까?':
            self.input_enable = True
        elif self.cur_script in self.ending_script :
            self.turn = 'end'


    def other_attack(self):
        idx = randint(0, len(self.o_pokemon.skill) - 1)
        self.attack(self.o_pokemon, self.p_pokemon, idx)
        self.turn = 'player'

    def attack(self, caster, subject, skill):
        self.input_enable = False
        self.turn = 'other'

        if caster.status_turn == 2:
            caster.status = Status.NONE
            caster.status_turn = 0

        print(caster.status)
        if caster.status == Status.POISON:
            s = caster.name + '은(는) 독에 의한 데미지를 입었다!'
            caster.cur_hp - int(caster.max_hp * 0.1)
            caster.status_turn += 1
            self.script_q.put(s)
        elif caster.status == Status.BURN:
            s = caster.name + '은(는) 화상 데미지를 입었다!'
            caster.cur_hp - int(caster.max_hp * 0.1)
            caster.status_turn += 1
            self.script_q.put(s)
        elif caster.status == Status.PARALYSIS:
            s = caster.name + '은(는) 몸이 저려서 움직일 수 없다!'
            caster.status_turn += 1
            self.script_q.put(s)
            return

        skill = caster.skill[skill]
        if skill.pp > caster.cur_pp:
            return

        s = caster.name + '의 ' + skill.name + '!'
        self.script_q.put(s)

        r = randint(0, 100)
        if skill.hitRate < r:
            s = subject.name + '은(는) 맞지 않았다!'
            self.script_q.put(s)
            return

        caster.cur_pp -= skill.pp
        subject.cur_hp -= int(skill.attack * 0.1)

        if subject.cur_hp < 0:
            s = subject.name + '은(는) 쓰러졌다!'
            self.script_q.put(s)
            if caster == self.p_pokemon:
                s = caster.name + '은(는) ' + str(subject.drop_exp) + '경험치를 얻었다!'
                s = caster.name + '은(는) ' + str(subject.drop_exp) + '경험치를 얻었다!'
                caster.cur_exp += subject.drop_exp
                self.script_q.put(s)
            else:
                s = subject.name + '은(는) 쓰러졌다!'

        r = randint(0, 100)
        if (r < 30):
            if skill.type == Type.POISON:
                subject.status = Status.POISON
                s = subject.name + '의 몸에 독이 퍼졌다!'
                self.script_q.put(s)

            elif skill.type == Type.FIRE:
                subject.status = Status.BURN
                s = subject.name + '은(는) 화상을 입었다!'
                self.script_q.put(s)

            elif skill.type == Type.ELECTR:
                subject.status = Status.PARALYSIS
                s = subject.name + '은(는) 마비되어 움직이기 어려워졌다!'
                self.script_q.put(s)


    def handle_input(self, e):
        if self.turn == 'end':
            game_framework.pop_mode()
        if self.input_enable == False:
            if e.key == SDLK_SPACE:
                self.cur_script = self.script_q.get()
            else:
                return
        else:
            if e.key == SDLK_SPACE:
                self.cur_script = self.script_q.get()
            if self.select_mode == 'main':
                self.select_main(e)
            elif self.select_mode == 'skill':
                self.select_skill(e)



    def render(self):
        print(self.turn)
        pp = 0
        if self.select_mode == 'main':
            Battle.touchpad.clip_draw(0, 783 - 202, 255, 202, game_width/2, game_height * 0.27, game_width, game_height * 0.55)
            if self.select == 0:
                Battle.touchpad.clip_draw(295, 783 - 131, 216, 90,
                                          game_width * 0.502, game_height * 0.325, game_width * 0.88, game_height * 0.26)
            elif self.select == 1:
                Battle.touchpad.clip_draw(295, 783 - 246, 78, 44,
                                          game_width * 0.157, game_height * 0.085, 78 * 2, 44 * 2)
            elif self.select == 2:
                Battle.touchpad.clip_draw(295, 783 - 246, 78, 44,
                                          game_width * 0.502, game_height * 0.07, 78 * 2, 44 * 2)
            elif self.select == 3:
                Battle.touchpad.clip_draw(295, 783 - 246, 78, 44,
                                          game_width * 0.845, game_height * 0.085, 78 * 2, 44 * 2)
            self.p_pokemon.render('m', game_width * 0.4, game_height * 0.335)

        elif self.select_mode == 'skill':
            Battle.touchpad.clip_draw(0, 783 - 406, 255, 202, game_width / 2, game_height * 0.27, game_width, game_height * 0.55)
            # 한 칸당 124, 55
            # 0번째 칸
            Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[0].type.value - 2) * 55, 124, 55,
                                      game_width * 0.25, game_height * 0.41, 248 * 1.2, 110)
            Battle.font.draw(game_width * 0.06, game_height * 0.43, self.p_pokemon.skill[0].name)
            if self.p_pokemon.skill[0].pp < self.p_pokemon.cur_pp:
                pp = self.p_pokemon.skill[0].pp
            else:
                pp = self.p_pokemon.cur_pp
            Battle.font.draw(game_width * 0.29, game_height * 0.383, str(pp))
            Battle.font.draw(game_width * 0.38, game_height * 0.383, str(self.p_pokemon.skill[0].pp))

            #1번째 칸
            Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[1].type.value - 2) * 55, 124, 55,
                                      game_width * 0.75, game_height * 0.41, 248 * 1.2, 110)
            Battle.font.draw(game_width * 0.56, game_height * 0.43, self.p_pokemon.skill[1].name)
            if self.p_pokemon.skill[1].pp < self.p_pokemon.cur_pp:
                pp = self.p_pokemon.skill[1].pp
            else:
                pp = self.p_pokemon.cur_pp
            Battle.font.draw(game_width * 0.79, game_height * 0.383, str(pp))
            Battle.font.draw(game_width * 0.88, game_height * 0.383, str(self.p_pokemon.skill[1].pp))

            # 2번째 칸
            if len(self.p_pokemon.skill) > 2:
                Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[2].type.value - 2) * 55, 124, 55,
                                          game_width * 0.25, game_height * 0.23, 248 * 1.2, 110)
                Battle.font.draw(game_width * 0.06, game_height * 0.25, self.p_pokemon.skill[2].name)
                if self.p_pokemon.skill[2].pp < self.p_pokemon.cur_pp:
                    pp = self.p_pokemon.skill[2].pp
                else:
                    pp = self.p_pokemon.cur_pp
                Battle.font.draw(game_width * 0.29, game_height * 0.205, str(pp))
                Battle.font.draw(game_width * 0.38, game_height * 0.205, str(self.p_pokemon.skill[2].pp))

            if len(self.p_pokemon.skill) > 3:
                Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[3].type.value - 2) * 55, 124, 55,
                                          game_width * 0.75, game_height * 0.23, 248 * 1.2, 110)
                Battle.font.draw(game_width * 0.56, game_height * 0.25, self.p_pokemon.skill[3].name)
                if self.p_pokemon.skill[3].pp < self.p_pokemon.cur_pp:
                    pp = self.p_pokemon.skill[3].pp
                else:
                    pp = self.p_pokemon.cur_pp
                Battle.font.draw(game_width * 0.79, game_height * 0.205, str(pp))
                Battle.font.draw(game_width * 0.88, game_height * 0.205, str(self.p_pokemon.skill[3].pp))

            # select 그리기
            if self.select == 0:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, game_width * 0.25, game_height * 0.41, 248 * 1.2, 110)
            elif self.select == 1:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, game_width * 0.75, game_height * 0.41, 248 * 1.2, 110)
            elif self.select == 2:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, game_width * 0.25, game_height * 0.23, 248 * 1.2, 110)
            elif self.select == 3:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, game_width * 0.75, game_height * 0.23, 248 * 1.2, 110)
            elif self.select == 4:
                Battle.touchpad.clip_draw(295, 783 - 300, 236, 45, game_width * 0.5, game_height * 0.06, 472 * 1.2, 90)

        # 화면 상단 출력
        Battle.background.clip_draw(0, 0, 255, 144, game_width/2, game_height * 0.75, game_width, game_height * 0.5)
        Battle.background.clip_draw(257, 0, 259, 144, game_width * 0.46, game_height * 0.88, 259 * 2.5, 144 * 2.5)

        # 상대 포켓몬 UI
        if self.o_pokemon.cur_hp < 0:
            self.o_pokemon.cur_hp = 0
        self.o_pokemon.render('f', game_width * 0.7, game_height * 0.87)
        Battle.UI.clip_draw(0, 80, 120, 29, game_width * 0.199, game_height * 0.92, 119*2, 58)
        Battle.font.draw(game_width * 0.01, game_height * 0.93, self.o_pokemon.name)
        Battle.UI.clip_draw(1 + 8 * (self.o_pokemon.level), 1, 8, 7, game_width * 0.285, game_height * 0.928, 16, 14)
        # 체력 바 render
        hp_percent = self.o_pokemon.cur_hp / self.o_pokemon.max_hp
        length = int(hp_percent * 48)
        if hp_percent > 0.5:
            Battle.UI.clip_draw_to_origin(0, 14, length, 7, game_width * 0.17 - 3, game_height * 0.89 - 2, length * 2, 14)
        elif 0.25 <= hp_percent <= 0.5:
            Battle.UI.clip_draw_to_origin(0, 21, length, 7, game_width * 0.17 - 3, game_height * 0.89 - 2, length * 2, 14)
        elif hp_percent < 0.25:
            Battle.UI.clip_draw_to_origin(0, 28, length, 7, game_width * 0.17 - 3, game_height * 0.89 - 2, length * 2, 14)
        # 상태이상 render 20, 8
        o_h = 0
        if self.o_pokemon.status == Status.POISON:
            o_h = 27
        elif self.o_pokemon.status == Status.BURN:
            o_h = 19
        elif self.o_pokemon.status == Status.PARALYSIS:
            o_h = 11
        Battle.UI.clip_draw(100, o_h, 20, 8, game_width * 0.06, game_height * 0.90 - 2, 40, 16)

        # 내 포켓몬 UI
        self.p_pokemon.render('b', game_width * 0.23, game_height * 0.73)
        Battle.UI.clip_draw(0, 109-72, 120, 41, game_width * 0.81, game_height * 0.70, 119*2, 41 * 2)
        Battle.UI.clip_draw(1 + 8 * self.p_pokemon.level, 1, 8, 7, game_width * 0.934, game_height * 0.725, 16, 14)

        #체력 바 render
        hp_percent = self.p_pokemon.cur_hp / self.p_pokemon.max_hp
        length = int(hp_percent * 48)
        if hp_percent > 0.5:
            Battle.UI.clip_draw_to_origin(0, 14, length, 7, game_width * 0.82 - 1, game_height * 0.68 + 2, length * 2, 14)
        elif 0.25 <= hp_percent <= 0.5:
            Battle.UI.clip_draw_to_origin(0, 21, length, 7, game_width * 0.82 - 1, game_height * 0.68 + 2, length * 2, 14)
        elif hp_percent < 0.25:
            Battle.UI.clip_draw_to_origin(0, 28, length, 7, game_width * 0.82 - 1, game_height * 0.68 + 2, length * 2, 14)

        # 경험치 바 render
        exp_percent = self.p_pokemon.exp / self.p_pokemon.max_exp
        length = int(exp_percent * 89)
        Battle.UI.clip_draw_to_origin(0, 11, length, 3, game_width * 0.72 - 7, game_height * 0.645 - 3, length*2, 6)

        # 상태이상 render 20, 8
        h = 0
        if self.p_pokemon.status == Status.POISON:
            h = 27
        elif self.p_pokemon.status == Status.BURN:
            h = 19
        elif self.p_pokemon.status == Status.PARALYSIS:
            h = 11
        Battle.UI.clip_draw(100, h, 20, 8, game_width * 0.71, game_height * 0.69 + 2, 40, 16)

        if self.p_pokemon.cur_hp < 0:
            self.p_pokemon.cur_hp = 0
        hp1 = self.p_pokemon.cur_hp // 100
        if hp1 != 0:
            Battle.UI.clip_draw(9 * hp1, 1, 8, 7, game_width * 0.83, game_height * 0.67, 16, 14)
        hp2 = (self.p_pokemon.cur_hp - 100*hp1) // 10
        Battle.UI.clip_draw(9 * hp2, 1, 8, 7, game_width * 0.855, game_height * 0.67, 16, 14)
        hp3 = (self.p_pokemon.cur_hp - 100 * hp1 - 10 * hp2)
        Battle.UI.clip_draw(9 * hp3, 1, 8, 7, game_width * 0.88, game_height * 0.67, 16, 14)
        hp1 = self.p_pokemon.max_hp // 100

        if hp1 != 0:
            Battle.UI.clip_draw(9 * hp1, 1, 8, 7, game_width * 0.94, game_height * 0.67, 16, 14)
            hp2 = (self.p_pokemon.max_hp - hp1 * 100) // 10
            Battle.UI.clip_draw(9 * hp2, 1, 8, 7, game_width * 0.965, game_height * 0.67, 16, 14)
            hp3 = (self.p_pokemon.max_hp - hp1 * 100 - hp2 * 10)
            Battle.UI.clip_draw(9 * hp3, 1, 8, 7, game_width * 0.99, game_height * 0.67, 16, 14)
        else:
            hp2 = (self.p_pokemon.max_hp - hp1 * 100) // 10
            Battle.UI.clip_draw(9 * hp2, 1, 8, 7, game_width * 0.94, game_height * 0.67, 16, 14)
            hp3 = (self.p_pokemon.max_hp - hp1 * 100 - hp2 * 10)
            Battle.UI.clip_draw(9 * hp3, 1, 8, 7, game_width * 0.965, game_height * 0.67, 16, 14)
        Battle.font.draw(game_width * 0.67, game_height * 0.725, self.p_pokemon.name)

        Battle.textbox.clip_draw(0, 0, 250, 44, game_width * 0.5, game_height * 0.56, 500 * 1.2, 88)
        Battle.font.draw(game_width * 0.05, game_height * 0.59, self.cur_script)


    def update(self):
        self.o_pokemon.update()
        self.script_update()


    def select_main(self, e):
        if e.key == SDLK_RIGHT:
            if self.select == 3:
                return
            self.select += 1
        elif e.key == SDLK_LEFT:
            if self.select == 0:
                return
            self.select -= 1
        elif e.key == SDLK_DOWN and self.select == 0:
            self.select += 1
        elif e.key == SDLK_UP and self.select > 0:
            self.select = 0
        elif e.key == SDLK_SPACE:
            if self.select == 0:
                self.select_mode = 'skill'
            elif self.select == 2:
                s = self.p_pokemon.name + '은(는) 도망쳤다!'
                self.script_q.put(s)
                self.script_q.put(s)
                self.cur_script = self.script_q.get()
                self.turn = 'end'


    def select_skill(self, e):
        if e.key == SDLK_RIGHT:
            if self.select < 4:
                self.select += 1
        elif e.key == SDLK_LEFT:
            if self.select > 0:
                self.select -= 1
        elif e.key == SDLK_DOWN:
            if self.select < 3:
                self.select += 2
            elif self.select == 3:
                self.select += 1
        elif e.key == SDLK_UP:
            if self.select > 1:
                self.select -= 2
        elif e.key == SDLK_SPACE:
            if self.select < 4:
                if len(self.p_pokemon.skill) >= self.select:
                    self.attack(self.p_pokemon, self.o_pokemon, self.select)
                    self.cur_script = self.script_q.get()
                    self.select_mode = 'main'
                    self.select = 0
            if self.select == 4:
                self.select_mode = 'main'
                self.select = 0

def init():
    global battle
    battle = Battle()
    gameWorld.addObject(battle, 0)

def finish():
    gameWorld.p.visible = True
    gameWorld.removeObject(battle)

def update():
    gameWorld.update()

def draw():
    clear_canvas()
    gameWorld.render()
    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        if (SDL_KEYDOWN, SDLK_F3) == (e.type, e.key):
            game_framework.pop_mode()
            print('end battle mode')
        elif (SDL_KEYDOWN, SDLK_ESCAPE) == (e.type, e.key):
            game_framework.quit()
        elif e.type == SDL_KEYDOWN:
            battle.handle_input(e)

def pause(): pass
def resume(): pass