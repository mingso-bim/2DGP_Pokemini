from pico2d import *
import gameWorld
import game_framework
import play_mode

class Tutorial:
    textbox = None
    font = None

    def __init__(self):
        if Tutorial.textbox == None:
            Tutorial.textbox = load_image('resource/textbox.png')
        if Tutorial.font == None:
            Tutorial.font = load_font('resource/font.ttf', 40)

        self.script = ('키보드 방향키로 움직일 수 있고', 'SPACE로 결정할 수 있어!', 'tv를 보고 SPACE를 누르면',  '저장하고 휴식할 수 있어!',
                       '마을 밖으로 나가는 도로에서', '바람이가 기다리고 있을 거야',
                        '바람이와 배틀에서 이길 수 있도록 훈련하자!')
        self.idx = 0

    def handle_events(self, e):
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_SPACE):
            self.manage_script()
        elif (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()

    def manage_script(self):
        if self.idx != len(self.script) - 1:
            self.idx += 1
            return
        game_framework.pop_mode()

    def render(self):
        Tutorial.textbox.clip_draw(0, 0, 250, 44, gameWorld.game_width * 0.5, gameWorld.game_height * 0.56, 500 * 1.2, 88)
        Tutorial.font.draw(gameWorld.game_width * 0.05, gameWorld.game_height * 0.59, self.script[self.idx])

    def update(self):
        pass

def init():
    global tutorial
    tutorial = Tutorial()
    gameWorld.addObject(tutorial, 1)

def finish():
    gameWorld.removeObject(tutorial)

def update():
    tutorial.update()

def draw():
    clear_canvas()
    play_mode.draw()
    tutorial.render()
    update_canvas()

def handle_events():
    events = get_events()
    for e in events:
        tutorial.handle_events(e)

def pause(): pass
def resume(): pass