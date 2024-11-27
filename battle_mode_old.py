from random import randint
from game_framework import change_mode
from stateMachine import StateMachine
from pico2d import *
import gameWorld
import game_framework
from gameWorld import game_width, game_height
from battle_state import *
from skill import Type, Status

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
        self.selectMode = 'main'

        self.player = gameWorld.p
        self.trainer = other
        self.player_cur_pokemon = self.player.pokemons[0]
        self.trainer_cur_pokemon = self.trainer.pokemons[0]
        self.trainer_skill = 0
        self.status = 'meet'
        self.scriptIdx = 0
        self.turn = 'player'
        self.next_state = ''

        self.cur_script = []
        self.make_script('meet')

    def make_script(self, status):
        self.cur_script.clear()
        self.scriptIdx = 0
        if status == 'meet':
            self.cur_script.append(Battle.meet_script[0] + self.trainer_cur_pokemon.name + Battle.meet_script[1])
            self.cur_script.append(Battle.meet_script[2] + self.player_cur_pokemon.name + Battle.meet_script[3])

        elif status == 'player':
            if self.player_cur_pokemon.status == Status.POISON:
                self.cur_script.append(self.player_cur_pokemon.name + Battle.status_script[1])
            if self.player_cur_pokemon.status == Status.BURN:
                self.cur_script.append(self.player_cur_pokemon.name + Battle.status_script[3])
            if self.player_cur_pokemon.status == Status.PARALYSIS:
                self.cur_script.append(self.player_cur_pokemon.name + Battle.status_script[5])
                return
            self.cur_script.append(self.player_cur_pokemon.name + '(은)는 무엇을 할까?')

        elif status == 'player_attack':
            self.cur_script.append(self.player_cur_pokemon.name + '의 ' + self.player_cur_skill.name + '!')

        elif status == 'status_poison':
            self.cur_script.append(Battle.status_script[0])

        elif status == 'status_burn':
            self.cur_script.append(Battle.status_script[2])

        elif status == 'status_paralysis':
            self.cur_script.append(Battle.status_script[4])

        elif status == 'other':
            if self.trainer_cur_pokemon.status == 'POISON':
                self.cur_script.append(self.trainer_cur_pokemon + Battle.status_script[1])
            if self.trainer_cur_pokemon.status == 'BURN':
                self.cur_script.append(self.trainer_cur_pokemon + Battle.status_script[3])
            if self.trainer_cur_pokemon.status == 'PARALYSIS':
                self.cur_script.append(self.trainer_cur_pokemon + Battle.status_script[5])
                return
            self.cur_script.append(self.trainer_cur_pokemon.name + Battle.attack_script[0] +
                      self.trainer_cur_pokemon.skill[self.trainer_skill].name + Battle.attack_script[1])

        elif status == 'run':
            self.cur_script.append(self.player_cur_pokemon.name + '(은)는 도망쳤다!')

        else:
            print('invalid')

    def handle_status(self):
        if self.scriptIdx == len(self.cur_script):
            if self.status == 'meet':
                self.change_status('player')

            elif self.status == 'run':
                game_framework.pop_mode()

            elif self.status in ('moving', 'status_poison', 'status_burn', 'status_paralysis'):
                if self.turn == 'player':
                    self.change_status('other')
                    self.turn = 'other'
                elif self.turn == 'other':
                    self.change_status('player')
                    self.turn = 'player'

            elif self.status == 'player_attack':
                self.change_status(self.next_state)
                if self.next_state == 'other':
                    self.turn = 'other'
                    self.other_attack()

            elif self.status == 'other':
                self.change_status(self.next_state)
                self.turn = 'player'


    def other_attack(self):
        self.trainer_skill = randint(0, len(self.trainer_cur_pokemon.skill) - 1)
        val = attack(self.trainer_cur_pokemon, self.player_cur_pokemon,
                     self.trainer_cur_pokemon.skill[self.trainer_skill])
        if val != None:
            if val == 'next':
                val = 'player'
            self.next_state = val


    def change_status(self, status):
        self.make_script(status)
        self.status = status


    def render(self):
        print(self.cur_script)
        pp = 0
        if self.selectMode == 'main':
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
            self.player_cur_pokemon.render('m', game_width * 0.4, game_height * 0.335)

        elif self.selectMode == 'skill':
            Battle.touchpad.clip_draw(0, 783 - 406, 255, 202, game_width / 2, game_height * 0.27, game_width, game_height * 0.55)
            # 한 칸당 124, 55
            # 0번째 칸
            Battle.touchpad.clip_draw(0, 317 - (self.player_cur_pokemon.skill[0].type.value - 2) * 55, 124, 55,
                                      game_width * 0.25, game_height * 0.41, 248 * 1.2, 110)
            Battle.font.draw(game_width * 0.06, game_height * 0.43, self.player_cur_pokemon.skill[0].name)
            if self.player_cur_pokemon.skill[0].pp < self.player_cur_pokemon.cur_pp:
                pp = self.player_cur_pokemon.skill[0].pp
            else:
                pp = self.player_cur_pokemon.cur_pp
            Battle.font.draw(game_width * 0.29, game_height * 0.383, str(pp))
            Battle.font.draw(game_width * 0.38, game_height * 0.383, str(self.player_cur_pokemon.skill[0].pp))

            #1번째 칸
            Battle.touchpad.clip_draw(0, 317 - (self.player_cur_pokemon.skill[1].type.value - 2) * 55, 124, 55,
                                      game_width * 0.75, game_height * 0.41, 248 * 1.2, 110)
            Battle.font.draw(game_width * 0.56, game_height * 0.43, self.player_cur_pokemon.skill[1].name)
            if self.player_cur_pokemon.skill[1].pp < self.player_cur_pokemon.cur_pp:
                pp = self.player_cur_pokemon.skill[1].pp
            else:
                pp = self.player_cur_pokemon.cur_pp
            Battle.font.draw(game_width * 0.79, game_height * 0.383, str(pp))
            Battle.font.draw(game_width * 0.88, game_height * 0.383, str(self.player_cur_pokemon.skill[1].pp))

            # 2번째 칸
            if len(self.player_cur_pokemon.skill) > 2:
                Battle.touchpad.clip_draw(0, 317 - (self.player_cur_pokemon.skill[2].type.value - 2) * 55, 124, 55,
                                          game_width * 0.25, game_height * 0.23, 248 * 1.2, 110)
                Battle.font.draw(game_width * 0.06, game_height * 0.25, self.player_cur_pokemon.skill[2].name)
                if self.player_cur_pokemon.skill[2].pp < self.player_cur_pokemon.cur_pp:
                    pp = self.player_cur_pokemon.skill[2].pp
                else:
                    pp = self.player_cur_pokemon.cur_pp
                Battle.font.draw(game_width * 0.29, game_height * 0.205, str(pp))
                Battle.font.draw(game_width * 0.38, game_height * 0.205, str(self.player_cur_pokemon.skill[2].pp))

            if len(self.player_cur_pokemon.skill) > 3:
                Battle.touchpad.clip_draw(0, 317 - (self.player_cur_pokemon.skill[3].type.value - 2) * 55, 124, 55,
                                          game_width * 0.75, game_height * 0.23, 248 * 1.2, 110)
                Battle.font.draw(game_width * 0.56, game_height * 0.25, self.player_cur_pokemon.skill[3].name)
                if self.player_cur_pokemon.skill[3].pp < self.player_cur_pokemon.cur_pp:
                    pp = self.player_cur_pokemon.skill[3].pp
                else:
                    pp = self.player_cur_pokemon.cur_pp
                Battle.font.draw(game_width * 0.79, game_height * 0.205, str(pp))
                Battle.font.draw(game_width * 0.88, game_height * 0.205, str(self.player_cur_pokemon.skill[3].pp))

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
        self.trainer_cur_pokemon.render('f', game_width * 0.7, game_height * 0.87)
        Battle.UI.clip_draw(0, 80, 120, 29, game_width * 0.199, game_height * 0.92, 119*2, 58)
        Battle.font.draw(game_width * 0.01, game_height * 0.93, self.trainer_cur_pokemon.name)
        Battle.UI.clip_draw(1 + 8 * (self.trainer_cur_pokemon.level), 1, 8, 7, game_width * 0.285, game_height * 0.928, 16, 14)

        # 내 포켓몬 UI
        self.player_cur_pokemon.render('b', game_width * 0.23, game_height * 0.73)
        Battle.UI.clip_draw(0, 109-72, 120, 41, game_width * 0.81, game_height * 0.70, 119*2, 41 * 2)
        percentage = int(self.player_cur_pokemon.exp / self.player_cur_pokemon.max_exp * 100)
        Battle.UI.clip_draw(0, 11, 89, 3, game_width * 0.853, game_height * 0.645, 178, 6)
        Battle.UI.clip_draw(1 + 8 * (self.player_cur_pokemon.level), 1, 8, 7, game_width * 0.934, game_height * 0.725, 16, 14)
        hp1 = self.player_cur_pokemon.cur_hp // 100
        if hp1 != 0:
            Battle.UI.clip_draw(9 * hp1, 1, 8, 7, game_width * 0.83, game_height * 0.67, 16, 14)
        hp2 = (self.player_cur_pokemon.cur_hp - 100*hp1) // 10
        Battle.UI.clip_draw(9 * hp2, 1, 8, 7, game_width * 0.855, game_height * 0.67, 16, 14)
        hp3 = (self.player_cur_pokemon.cur_hp - 100 * hp1 - 10 * hp2)
        Battle.UI.clip_draw(9 * hp3, 1, 8, 7, game_width * 0.88, game_height * 0.67, 16, 14)
        hp1 = self.player_cur_pokemon.max_hp // 100

        if hp1 != 0:
            Battle.UI.clip_draw(9 * hp1, 1, 8, 7, game_width * 0.94, game_height * 0.67, 16, 14)
            hp2 = (self.player_cur_pokemon.max_hp - hp1 * 100) // 10
            Battle.UI.clip_draw(9 * hp2, 1, 8, 7, game_width * 0.965, game_height * 0.67, 16, 14)
            hp3 = (self.player_cur_pokemon.max_hp - hp1 * 100 - hp2 * 10)
            Battle.UI.clip_draw(9 * hp3, 1, 8, 7, game_width * 0.99, game_height * 0.67, 16, 14)
        else:
            hp2 = (self.player_cur_pokemon.max_hp - hp1 * 100) // 10
            Battle.UI.clip_draw(9 * hp2, 1, 8, 7, game_width * 0.94, game_height * 0.67, 16, 14)
            hp3 = (self.player_cur_pokemon.max_hp - hp1 * 100 - hp2 * 10)
            Battle.UI.clip_draw(9 * hp3, 1, 8, 7, game_width * 0.965, game_height * 0.67, 16, 14)
        Battle.font.draw(game_width * 0.67, game_height * 0.725, self.player_cur_pokemon.name)

        Battle.textbox.clip_draw(0, 0, 250, 44, game_width * 0.5, game_height * 0.56, 500 * 1.2, 88)
        if self.status == 'run':
            Battle.font.draw(game_width * 0.05, game_height * 0.59, self.player_cur_pokemon.name + '(은)는 도망쳤다!')
        elif self.status == 'moving':
            Battle.font.draw(game_width * 0.05, game_height * 0.59, '그러나 상대는 맞지 않았다!')
        else:
            Battle.font.draw(game_width * 0.05, game_height * 0.59, self.cur_script[self.scriptIdx])


    def update(self):
        self.trainer_cur_pokemon.update()

    def handleSelect(self, e):
        if self.status == 'meet':
            if e.key == SDLK_SPACE:
                self.scriptIdx += 1
                self.handle_status()

        elif self.status == 'run':
            if e.key == SDLK_SPACE:
                self.handle_status()
                self.scriptIdx += 1

        elif self.status == 'player_attack':
            self.scriptIdx += 1
            self.handle_status()

        elif self.status == 'other':
            self.scriptIdx += 1
            self.handle_status()

        elif self.selectMode == 'main':
            if self.player_cur_pokemon.status == 'PARALYSIS':
                self.scriptIdx += 1
                return
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
                    self.selectMode = 'skill'
                elif self.select == 2:
                    self.change_status('run')


        elif self.selectMode == 'skill':
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
                    if len(self.player_cur_pokemon.skill) >= self.select:
                        s = self.player_cur_pokemon.useSkill(self.select)
                        val = attack(self.player_cur_pokemon, self.trainer_cur_pokemon, s)
                        print(val)
                        if val != None:
                            if val == 'next':
                                val = 'other'
                            self.next_state = val
                            self.player_cur_skill = s
                            self.change_status('player_attack')

                if self.select == 4:
                    self.selectMode = 'main'
                    self.select = 0

def attack(caster, subject, skill):
    if skill.pp > caster.cur_pp:
        return None

    r = randint(0, 100)
    if skill.hitRate < r:
        return 'moving'

    subject.cur_hp -= int(skill.attack * 0.2)

    r = randint(0, 100)
    if (r < 30):
        if skill.type == Type.POISON:
            subject.status = Status.POISON
            return 'status_poison'
        elif skill.type == Type.FIRE:
            subject.status = Status.BURN
            return 'status_burn'
        elif skill.type == Type.ELECTR:
            subject.status = Status.PARALYSIS
            return 'status_paralysis'

    return 'next'


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
            battle.handleSelect(e)

def pause(): pass
def resume(): pass