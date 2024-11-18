from pico2d import *
import gameWorld
import game_framework
from gameWorld import game_width, game_height


class Battle:
    touchpad = None
    UI = None
    background = None
    font = None


    def __init__(self):
        if Battle.touchpad == None:
            Battle.touchpad = load_image('resource/battleTouchpad.png')
        if Battle.UI == None:
            Battle.UI = load_image('resource/battleUI.png')
        if Battle.background == None:
            Battle.background = load_image('resource/battleBackground.png')
        if Battle.font == None:
            Battle.font = load_font('resource/font.ttf', 55)
        self.select = 0
        self.player = gameWorld.p
        self.trainer = None
        self.player_cur_pokemon = self.player.pokemons[0]
        #self.trainer_cur_pokemon = self.trainer.pokemons[0]


    def render(self):
        Battle.touchpad.clip_draw(0, 783 - 202, 255, 202, game_width/2, game_height * 0.27, game_width, game_height * 0.55)
        Battle.background.clip_draw(0, 0, 255, 144, game_width/2, game_height * 0.75, game_width, game_height * 0.5)
        Battle.background.clip_draw(257, 0, 259, 144, game_width * 0.46, game_height * 0.77, 259 * 2.5, 144 * 2.5)

        # 상대 포켓몬 UI
        Battle.UI.clip_draw(0, 80, 120, 29, game_width * 0.199, game_height * 0.89, 119*2, 58)


        # 내 포켓몬 UI
        Battle.UI.clip_draw(0, 109-69, 120, 38, game_width * 0.81, game_height * 0.63, 119*2, 38 * 2)


    def update(self):
        pass


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

def pause(): pass
def resume(): pass