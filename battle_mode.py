from random import randint

import effect
import gameWorld
from pico2d import *
import game_framework
from skill import Type, Status
from queue import Queue
from skill import advantage, disadvantage

other = None

class Battle:
    touchpad = None
    UI = None
    background = None
    font = None
    textbox = None
    music = None
    sound_button = None
    sound_attack = None
    sound_win = None
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
        if Battle.music == None:
            Battle.music = load_music('resource/sound/music_battle.mp3')
            Battle.music.set_volume(32)
        if Battle.sound_button == None:
            Battle.sound_button = load_wav('resource/sound/button.wav')
            Battle.sound_button.set_volume(32)
        if Battle.sound_attack == None:
            Battle.sound_attack = load_wav('resource/sound/attack.wav')
            Battle.sound_attack.set_volume(32)
        if Battle.sound_win == None:
            Battle.sound_win = load_music('resource/sound/battle_win.mp3')
            Battle.sound_win.set_volume(32)

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
        self.playing = False
        self.o_damage = 0

        self.player_attacked = False

        self.ending_script = [self.p_pokemon.name + '은(는) 쓰러졌다!', self.cur_script == self.o_pokemon.name + '은(는) 쓰러졌다!',
                              self.p_pokemon.name + '은(는) ' + str(self.o_pokemon.drop_exp) + '경험치를 얻었다!']


    def put_meet_script(self):
        if hasattr(self.other, 'name'):
            s = '바람이 싸움을 걸어왔다!'
            self.script_q.put(s)
        else:
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
            if self.player_attacked:
                self.turn = 'other'
            else:
                self.put_player_script()

        elif self.turn == 'other':
            self.other_attack()
            self.player_attacked = False


        if self.cur_script == self.p_pokemon.name + '은(는) 무엇을 할까?':
            self.input_enable = True
        elif self.cur_script in self.ending_script :
            self.turn = 'end'
            if self.playing == False and self.p_pokemon.cur_hp > 0:
                Battle.music.stop()
                Battle.sound_win.repeat_play()
                self.playing = True

    def other_attack(self):
        idx = randint(0, len(self.o_pokemon.skill) - 1)
        self.attack(self.o_pokemon, self.p_pokemon, idx)
        self.turn = 'player'

    def attack(self, caster, subject, skill):
        self.input_enable = False
        Battle.sound_attack.play()

        if caster == self.p_pokemon:
            self.player_attacked = True

        if caster.status_turn == 2:
            caster.status = Status.NONE
            caster.status_turn = 0

        if caster.status == Status.POISON:
            s = caster.name + '은(는) 독에 의한 데미지를 입었다!'
            caster.cur_hp -= int(caster.max_hp * 0.1)
            caster.status_turn += 1
            self.script_q.put(s)
        elif caster.status == Status.BURN:
            s = caster.name + '은(는) 화상 데미지를 입었다!'
            caster.cur_hp -= int(caster.max_hp * 0.1)
            caster.status_turn += 1
            self.script_q.put(s)
        elif caster.status == Status.PARALYSIS:
            s = caster.name + '은(는) 몸이 저려서 움직일 수 없다!'
            caster.status_turn += 1
            self.script_q.put(s)
            return

        if caster.cur_hp <= 0:
            s = caster.name + '은(는) 쓰러졌다!'
            self.script_q.put(s)
            if caster != self.p_pokemon:

                s = self.p_pokemon.name + '은(는) ' + str(caster.drop_exp) + '경험치를 얻었다!'
                s = self.p_pokemon.name + '은(는) ' + str(caster.drop_exp) + '경험치를 얻었다!'
                self.p_pokemon.exp += caster.drop_exp
                self.script_q.put(s)
                if self.p_pokemon.exp > self.p_pokemon.max_exp:
                    e = self.p_pokemon.exp - self.p_pokemon.max_exp
                    self.p_pokemon.level += 1
                    self.p_pokemon.exp = e
                    self.p_pokemon.level_up()
            return

        skill = caster.skill[skill]
        if skill.pp > caster.cur_pp:
            skill = skill.STRUGGLING

        s = caster.name + '의 ' + skill.name + '!'
        self.script_q.put(s)

        r = randint(0, 100)
        if skill.hitRate < r:
            s = subject.name + '은(는) 맞지 않았다!'
            self.script_q.put(s)
            return

        caster.cur_pp -= skill.pp
        
        # 상성
        ad = advantage.get(skill.type)
        disad = disadvantage.get(skill.type)

        efficient = 0
        if ad != None:
            if ad == subject.type:
                efficient = 0.2
                s = '효과가 굉장했다!'
                self.script_q.put(s)
        if disad != None:
            if disad == subject.type:
                efficient = 0.05
                s = '효과가 별로인 듯 하다'
                self.script_q.put(s)
        if efficient == 0:
            efficient = 0.1

        if skill.type == caster.type:
            efficient *= 1.2

        if caster == self.p_pokemon:
            subject.cur_hp -= int(skill.attack * efficient) + caster.level * 2
        else:
            self.o_damage = int(skill.attack * efficient) + caster.level * 2

        if subject.cur_hp <= 0:
            s = subject.name + '은(는) 쓰러졌다!'
            self.script_q.put(s)
            if caster == self.p_pokemon:

                s = caster.name + '은(는) ' + str(subject.drop_exp) + '경험치를 얻었다!'
                s = caster.name + '은(는) ' + str(subject.drop_exp) + '경험치를 얻었다!'
                caster.exp += subject.drop_exp
                self.script_q.put(s)
                if self.p_pokemon.exp > self.p_pokemon.max_exp:
                    e = self.p_pokemon.exp - self.p_pokemon.max_exp
                    self.p_pokemon.level += 1
                    self.p_pokemon.exp = e
                    self.p_pokemon.level_up()
            else:
                s = subject.name + '은(는) 쓰러졌다!'
            return

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
        if e.type == SDL_KEYDOWN:
            Battle.sound_button.play()

        if self.turn == 'end':
            self.p_pokemon.cur_pp = self.p_pokemon.max_pp
            self.music.stop()
            game_framework.pop_mode()
            return

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
        print(self.turn, self.script_q.qsize())
        pp = 0
        if self.select_mode == 'main':
            Battle.touchpad.clip_draw(0, 783 - 202, 255, 202, gameWorld.game_width/2, gameWorld.game_height * 0.27, gameWorld.game_width, gameWorld.game_height * 0.55)
            if self.select == 0:
                Battle.touchpad.clip_draw(295, 783 - 131, 216, 90,
                                          gameWorld.game_width * 0.502, gameWorld.game_height * 0.325, gameWorld.game_width * 0.88, gameWorld.game_height * 0.26)
            elif self.select == 1:
                Battle.touchpad.clip_draw(295, 783 - 246, 78, 44,
                                          gameWorld.game_width * 0.157, gameWorld.game_height * 0.085, 78 * 2, 44 * 2)
            elif self.select == 2:
                Battle.touchpad.clip_draw(295, 783 - 246, 78, 44,
                                          gameWorld.game_width * 0.502, gameWorld.game_height * 0.07, 78 * 2, 44 * 2)
            elif self.select == 3:
                Battle.touchpad.clip_draw(295, 783 - 246, 78, 44,
                                          gameWorld.game_width * 0.845, gameWorld.game_height * 0.085, 78 * 2, 44 * 2)
            self.p_pokemon.render('m', gameWorld.game_width * 0.4, gameWorld.game_height * 0.335)

        elif self.select_mode == 'skill':
            Battle.touchpad.clip_draw(0, 783 - 406, 255, 202, gameWorld.game_width / 2, gameWorld.game_height * 0.27, gameWorld.game_width, gameWorld.game_height * 0.55)
            # 한 칸당 124, 55
            # 0번째 칸
            Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[0].type.value - 2) * 55, 124, 55,
                                      gameWorld.game_width * 0.25, gameWorld.game_height * 0.41, 248 * 1.2, 110)
            Battle.font.draw(gameWorld.game_width * 0.06, gameWorld.game_height * 0.43, self.p_pokemon.skill[0].name)
            if self.p_pokemon.skill[0].pp < self.p_pokemon.cur_pp:
                pp = self.p_pokemon.skill[0].pp
            else:
                pp = self.p_pokemon.cur_pp
            Battle.font.draw(gameWorld.game_width * 0.29, gameWorld.game_height * 0.383, str(pp))
            Battle.font.draw(gameWorld.game_width * 0.38, gameWorld.game_height * 0.383, str(self.p_pokemon.skill[0].pp))

            #1번째 칸
            Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[1].type.value - 2) * 55, 124, 55,
                                      gameWorld.game_width * 0.75, gameWorld.game_height * 0.41, 248 * 1.2, 110)
            Battle.font.draw(gameWorld.game_width * 0.56, gameWorld.game_height * 0.43, self.p_pokemon.skill[1].name)
            if self.p_pokemon.skill[1].pp < self.p_pokemon.cur_pp:
                pp = self.p_pokemon.skill[1].pp
            else:
                pp = self.p_pokemon.cur_pp
            Battle.font.draw(gameWorld.game_width * 0.79, gameWorld.game_height * 0.383, str(pp))
            Battle.font.draw(gameWorld.game_width * 0.88, gameWorld.game_height * 0.383, str(self.p_pokemon.skill[1].pp))

            # 2번째 칸
            if len(self.p_pokemon.skill) > 2:
                Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[2].type.value - 2) * 55, 124, 55,
                                          gameWorld.game_width * 0.25, gameWorld.game_height * 0.23, 248 * 1.2, 110)
                Battle.font.draw(gameWorld.game_width * 0.06, gameWorld.game_height * 0.25, self.p_pokemon.skill[2].name)
                if self.p_pokemon.skill[2].pp < self.p_pokemon.cur_pp:
                    pp = self.p_pokemon.skill[2].pp
                else:
                    pp = self.p_pokemon.cur_pp
                Battle.font.draw(gameWorld.game_width * 0.29, gameWorld.game_height * 0.205, str(pp))
                Battle.font.draw(gameWorld.game_width * 0.38, gameWorld.game_height * 0.205, str(self.p_pokemon.skill[2].pp))

            if len(self.p_pokemon.skill) > 3:
                Battle.touchpad.clip_draw(0, 317 - (self.p_pokemon.skill[3].type.value - 2) * 55, 124, 55,
                                          gameWorld.game_width * 0.75, gameWorld.game_height * 0.23, 248 * 1.2, 110)
                Battle.font.draw(gameWorld.game_width * 0.56, gameWorld.game_height * 0.25, self.p_pokemon.skill[3].name)
                if self.p_pokemon.skill[3].pp < self.p_pokemon.cur_pp:
                    pp = self.p_pokemon.skill[3].pp
                else:
                    pp = self.p_pokemon.cur_pp
                Battle.font.draw(gameWorld.game_width * 0.79, gameWorld.game_height * 0.205, str(pp))
                Battle.font.draw(gameWorld.game_width * 0.88, gameWorld.game_height * 0.205, str(self.p_pokemon.skill[3].pp))

            # select 그리기
            if self.select == 0:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, gameWorld.game_width * 0.25, gameWorld.game_height * 0.41, 248 * 1.2, 110)
            elif self.select == 1:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, gameWorld.game_width * 0.75, gameWorld.game_height * 0.41, 248 * 1.2, 110)
            elif self.select == 2:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, gameWorld.game_width * 0.25, gameWorld.game_height * 0.23, 248 * 1.2, 110)
            elif self.select == 3:
                Battle.touchpad.clip_draw(295, 783 - 194, 124, 55, gameWorld.game_width * 0.75, gameWorld.game_height * 0.23, 248 * 1.2, 110)
            elif self.select == 4:
                Battle.touchpad.clip_draw(295, 783 - 300, 236, 45, gameWorld.game_width * 0.5, gameWorld.game_height * 0.06, 472 * 1.2, 90)

        # 화면 상단 출력
        Battle.background.clip_draw(0, 0, 255, 144, gameWorld.game_width/2, gameWorld.game_height * 0.75, gameWorld.game_width, gameWorld.game_height * 0.5)
        Battle.background.clip_draw(257, 0, 259, 144, gameWorld.game_width * 0.46, gameWorld.game_height * 0.88, 259 * 2.5, 144 * 2.5)

        # 상대 포켓몬 UI
        if self.o_pokemon.cur_hp < 0:
            self.o_pokemon.cur_hp = 0
        self.o_pokemon.render('f', gameWorld.game_width * 0.7, gameWorld.game_height * 0.87)
        Battle.UI.clip_draw(0, 80, 120, 29, gameWorld.game_width * 0.199, gameWorld.game_height * 0.92, 119*2, 58)
        Battle.font.draw(gameWorld.game_width * 0.01, gameWorld.game_height * 0.93, self.o_pokemon.name)

        # 레벨 render
        Battle.UI.clip_draw(8 * self.o_pokemon.level, 0, 8, 7, gameWorld.game_width * 0.285, gameWorld.game_height * 0.928, 16, 14)

        # 체력 바 render
        hp_percent = self.o_pokemon.cur_hp / self.o_pokemon.max_hp
        length = int(hp_percent * 48)
        if hp_percent > 0.5:
            Battle.UI.clip_draw_to_origin(0, 14, length, 7, gameWorld.game_width * 0.17 - 3, gameWorld.game_height * 0.89 - 2, length * 2, 14)
        elif 0.25 <= hp_percent <= 0.5:
            Battle.UI.clip_draw_to_origin(0, 21, length, 7, gameWorld.game_width * 0.17 - 3, gameWorld.game_height * 0.89 - 2, length * 2, 14)
        elif hp_percent < 0.25:
            Battle.UI.clip_draw_to_origin(0, 28, length, 7, gameWorld.game_width * 0.17 - 3, gameWorld.game_height * 0.89 - 2, length * 2, 14)
        # 상태이상 render 20, 8
        o_h = 0
        if self.o_pokemon.status == Status.POISON:
            o_h = 27
        elif self.o_pokemon.status == Status.BURN:
            o_h = 19
        elif self.o_pokemon.status == Status.PARALYSIS:
            o_h = 11
        Battle.UI.clip_draw(100, o_h, 20, 8, gameWorld.game_width * 0.06, gameWorld.game_height * 0.90 - 2, 40, 16)

        # 내 포켓몬 UI
        self.p_pokemon.render('b', gameWorld.game_width * 0.23, gameWorld.game_height * 0.73)
        Battle.UI.clip_draw(0, 109-72, 120, 41, gameWorld.game_width * 0.81, gameWorld.game_height * 0.70, 119*2, 41 * 2)

        # 레벨 render
        Battle.UI.clip_draw(8 * self.p_pokemon.level, 0, 8, 7, gameWorld.game_width * 0.934, gameWorld.game_height * 0.725, 16, 14)

        #체력 바 render
        if self.p_pokemon.cur_hp < 0:
            self.p_pokemon.cur_hp = 0

        hp_percent = self.p_pokemon.cur_hp / self.p_pokemon.max_hp
        length = int(hp_percent * 48)
        if hp_percent > 0.5:
            Battle.UI.clip_draw_to_origin(0, 14, length, 7, gameWorld.game_width * 0.82 - 1, gameWorld.game_height * 0.68 + 2, length * 2, 14)
        elif 0.25 <= hp_percent <= 0.5:
            Battle.UI.clip_draw_to_origin(0, 21, length, 7, gameWorld.game_width * 0.82 - 1, gameWorld.game_height * 0.68 + 2, length * 2, 14)
        elif hp_percent < 0.25:
            Battle.UI.clip_draw_to_origin(0, 28, length, 7, gameWorld.game_width * 0.82 - 1, gameWorld.game_height * 0.68 + 2, length * 2, 14)

        # 경험치 바 render
        exp_percent = self.p_pokemon.exp / self.p_pokemon.max_exp
        length = int(exp_percent * 89)
        Battle.UI.clip_draw_to_origin(0, 11, length, 3, gameWorld.game_width * 0.72 - 7, gameWorld.game_height * 0.645 - 3, length*2, 6)

        # 상태이상 render 20, 8
        h = 0
        if self.p_pokemon.status == Status.POISON:
            h = 27
        elif self.p_pokemon.status == Status.BURN:
            h = 19
        elif self.p_pokemon.status == Status.PARALYSIS:
            h = 11
        Battle.UI.clip_draw(100, h, 20, 8, gameWorld.game_width * 0.71, gameWorld.game_height * 0.69 + 2, 40, 16)

        # 체력
        if self.p_pokemon.cur_hp < 0:
            self.p_pokemon.cur_hp = 0
        hp1 = self.p_pokemon.cur_hp // 100
        if hp1 != 0:
            Battle.UI.clip_draw(8 * hp1, 0, 8, 7, gameWorld.game_width * 0.83, gameWorld.game_height * 0.67, 16, 14)
        hp2 = (self.p_pokemon.cur_hp - 100*hp1) // 10
        Battle.UI.clip_draw(8 * hp2, 0, 8, 7, gameWorld.game_width * 0.855, gameWorld.game_height * 0.67, 16, 14)
        hp3 = (self.p_pokemon.cur_hp - 100 * hp1 - 10 * hp2)
        Battle.UI.clip_draw(8 * hp3, 0, 8, 7, gameWorld.game_width * 0.88, gameWorld.game_height * 0.67, 16, 14)
        hp1 = self.p_pokemon.max_hp // 100

        if hp1 != 0:
            Battle.UI.clip_draw(8 * hp1, 0, 8, 7, gameWorld.game_width * 0.94, gameWorld.game_height * 0.67, 16, 14)
            hp2 = (self.p_pokemon.max_hp - hp1 * 100) // 10
            Battle.UI.clip_draw(8 * hp2, 0, 8, 7, gameWorld.game_width * 0.965, gameWorld.game_height * 0.67, 16, 14)
            hp3 = (self.p_pokemon.max_hp - hp1 * 100 - hp2 * 10)
            Battle.UI.clip_draw(8 * hp3, 0, 8, 7, gameWorld.game_width * 0.99, gameWorld.game_height * 0.67, 16, 14)
        else:
            hp2 = (self.p_pokemon.max_hp - hp1 * 100) // 10
            Battle.UI.clip_draw(8 * hp2, 0, 8, 7, gameWorld.game_width * 0.94, gameWorld.game_height * 0.67, 16, 14)
            hp3 = (self.p_pokemon.max_hp - hp1 * 100 - hp2 * 10)
            Battle.UI.clip_draw(8 * hp3, 0, 8, 7, gameWorld.game_width * 0.965, gameWorld.game_height * 0.67, 16, 14)
        Battle.font.draw(gameWorld.game_width * 0.67, gameWorld.game_height * 0.725, self.p_pokemon.name)

        Battle.textbox.clip_draw(0, 0, 250, 44, gameWorld.game_width * 0.5, gameWorld.game_height * 0.56, 500 * 1.2, 88)
        Battle.font.draw(gameWorld.game_width * 0.05, gameWorld.game_height * 0.59, self.cur_script)


    def update(self):
        self.o_pokemon.update()
        self.script_update()
        s = str(self.o_pokemon.name) + '의'
        if s in self.cur_script:
            if self.o_damage > 0:
                self.p_pokemon.cur_hp -= self.o_damage
                self.o_damage = 0
                Battle.sound_attack.play()

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
    Battle.music.repeat_play()
    gameWorld.addObject(battle, 1)
    effect.b_fade_in()

def finish():
    gameWorld.get_player().visible = True
    battle.music.stop()
    battle.sound_win.stop()
    gameWorld.get_map().music.play()
    effect.b_fade_out()
    gameWorld.removeObject(battle)
    effect.b_fade_in()

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