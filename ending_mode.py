import gameWorld
import game_framework
import play_mode, battle_mode
from pico2d import *

trainer = None

class Ending:
    textbox = None
    font = None

    def __init__(self):
        if Ending.textbox == None:
            Ending.textbox = load_image('resource/textbox.png')
        if Ending.font == None:
            Ending.font = load_font('resource/font.ttf', 40)

        self.p = gameWorld.get_player()
        self.t = trainer

        self.meet_script = (str(self.p.name) + '!', '모험을 떠나기 전에', '얼마나 준비되었나 볼까?', '승부야!')
        self.defeat_script = ('아직 준비가 더 필요할 것 같은데?', '이렇게 약해서는 모험을 떠나지 못할 거야!')
        self.victory_script = ('꽤나 강해졌구나?', '다음엔 지지 않을거야!', '그럼 즐거운 모험 되길 바래!')
        self.return_script = ('나랑 승부해서 이기기 전엔 갈 수 없어!', '포켓몬을 회복하고 오도록 해')

        self.idx = 0

        if self.p.pokemons[0].cur_hp <= 0:
            self.script = self.return_script
            self.state = 'return'
        else:
            self.script = self.meet_script
            self.state = 'meet'

        for pokemon in self.t.pokemons:
            pokemon.cur_hp = pokemon.max_hp
            pokemon.cur_pp = pokemon.max_pp


    def render(self):
        print(f'state: {self.state}, mode: {game_framework.stack[-1]}')
        if self.state == 'battle':
            return
        Ending.textbox.clip_draw(0, 0, 250, 44, gameWorld.game_width * 0.5, gameWorld.game_height * 0.56, 500 * 1.2, 88)
        Ending.font.draw(gameWorld.game_width * 0.05, gameWorld.game_height * 0.59, self.script[self.idx])

    def handle_events(self, e):
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_SPACE):
            self.manage_script()
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()

    def manage_script(self):
        # 마지막 스크립트일 때
        if not self.idx == len(self.script) - 1:
            self.idx += 1
            return

        if self.state == 'meet':
            self.idx = 0
            self.state = 'battle'
            battle_mode.other = self.t
            self.t.visible = False
            game_framework.push_mode(battle_mode)

        elif self.state == 'defeat':
            self.t.visible = True
            self.p.visible = True
            game_framework.pop_mode()

        elif self.state == 'victory':
            self.t.ending = True
            self.t.visible = True
            self.p.visible = True
            self.p.ending = True
            game_framework.pop_mode()

        elif self.state == 'return':
            self.t.visible = True
            self.p.visible = True
            game_framework.pop_mode()


    def update(self):
        if self.state == 'battle' and game_framework.stack[-1] != battle_mode:
            if self.p.pokemons[0].cur_hp <= 0:
                self.state = 'defeat'
                self.script = self.defeat_script
            elif self.t.pokemons[0].cur_hp <= 0:
                self.state = 'victory'
                self.script = self.victory_script
            self.t.visible = True
            self.p.visible = True


def init():
    global e
    e = Ending()
    gameWorld.addObject(e, 1)
    print('enter ending')

def finish():
    gameWorld.removeObject(e)

def update():
    e.update()

def draw():
    clear_canvas()
    play_mode.draw()
    e.render()
    update_canvas()

def handle_events():
    events = get_events()
    for ev in events:
        e.handle_events(ev)

def pause(): pass
def resume(): pass