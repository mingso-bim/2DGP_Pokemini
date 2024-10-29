from pico2d import *
from UI import game_width, game_height


class Intro:
    def __init__(self):
        self.enable = True
        self.phase = 0
        self.frame = 0
        self.select = -1
        self.script = ()
        self.scriptIdx = 0

        self.textboxLoc = [game_width / 2, game_height * 0.38]

        self.font = load_font('resource/font.ttf', 55)
        self.background = load_image('resource/intro/intro_background.png')
        self.profMa = load_image('resource/intro/profMa.png')
        self.walkingPlayer = load_image('resource/intro/intro_player.png')
        self.textbox = load_image('resource/textbox.png')
        self.initScript()


    def render(self):
        if self.phase == 0:
            self.profMa.clip_draw(23, 35, 1, 1, game_width/2, game_height/2, game_width, game_height)
            self.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)
            self.font.draw(self.textboxLoc[0] - game_width * 0.4, self.textboxLoc[0], self.script[self.scriptIdx])
            return

        self.background.draw(game_width/2, game_height/2, game_width, game_height)
        if self.phase == 1:
            self.profMa.clip_draw(0, 0, 67, 133, game_width/2, game_height * 0.75, 134, 266)
            self.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)

        elif self.phase == 2:
            self.profMa.clip_draw(67, 0, 82, 133, game_width / 2, game_height * 0.75, 164, 266)
            self.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)


    def update(self):
        self.frame = (self.frame+1) % 4
        delay(0.3)
        if self.scriptIdx == 2 and self.scriptIdx == 9:
            self.phase += 1

    def handle_event(self, _event):
        self.checkScriptIdx()
        if _event.type == SDL_KEYDOWN and self.phase == 2:
            if self.select == -1:
                self.select = 0
            elif _event.key == SDLK_LEFT and self.select == 1:
                self.select = self.select - 1
            elif _event.key == SDLK_RIGHT and self.select == 0:
                self.select = self.select + 1
        elif _event.type == SDL_KEYDOWN and _event.key == SDLK_SPACE:
            self.scriptIdx += 1


    def checkScriptIdx(self):
        pass


    def initScript(self):
        self.script += ('흐음!!', '잘 왔다!', '포켓몬스터의 세계에 온 것을', '환영한다!',
                        '내 이름은 마박사!', '모두가 포켓몬 박사님이라고', '부르고 있단다.', '이 세계에는',
                        '포켓몬스터', "줄여서 '포켓몬'이라 불리는", '신기한 생명체가', '도처에 살고 있다!',
                        '우리 인간은 포켓몬과', '사이좋게 지내고 있단다', '이제 자네에 대해서', '알아보도록 하지',
                        '자네는 남자인가?', '아니면 여자인가?', '그렇군!', '자네의 이름은?', '흐음...',
                        '라고 하는가!', '좋은 이름이구나!', '여기 있는 이 소년은', '자네의 친구였지?',
                        '이름이 바람이로군!', '!!', '이제부터 너만의', '이야기가 시작된다!', '너는 여러 포켓몬이나',
                        '많은 사람들을 만나', '무언가를 발견하게 되겠지!!', '그럼', '포켓몬스터의 세계로!')
