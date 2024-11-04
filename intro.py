from pico2d import *
from gameWorld import game_width, game_height


class Intro:
    def __init__(self, p):
        self.enable = False
        self.phase = 0
        self.frame = 0
        self.select = 0
        self.script = ()
        self.scriptIdx = 0
        self.player = p
        self.playerX = 0

        self.textboxLoc = [game_width / 2, game_height * 0.38]

        self.font = load_font('resource/font.ttf', 55)
        self.background = load_image('resource/intro/intro_background.png')
        self.profMa = load_image('resource/intro/profMa.png')
        self.walkingPlayer = load_image('resource/intro/intro_player.png')
        self.textbox = load_image('resource/textbox.png')
        self.miniTextbox = load_image('resource/miniTextbox.png')
        self.arrow = load_image('resource/intro/select.png')
        self.smallPlayer = load_image('resource/intro/smallPlayer.png')
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

        elif self.phase in [2, 6, 8]:
            self.profMa.clip_draw(67, 0, 82, 133, game_width / 2, game_height * 0.75, 164, 266)
            self.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)

        elif self.phase == 3:
            if self.select == 0:
                self.walkingPlayer.clip_draw(3 + 46 * self.frame, 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)
                self.walkingPlayer.clip_draw(189 + 52, 0, 53, 117, game_width * 0.7, game_height * 0.7, 100, 234)
            elif self.select == 1:
                self.walkingPlayer.clip_draw(189 + 52 * self.frame, 0, 53, 117, game_width * 0.7, game_height * 0.7, 100, 234)
                self.walkingPlayer.clip_draw(3, 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)
            else:
                self.walkingPlayer.clip_draw(189 + 52, 0, 53, 117, game_width * 0.7, game_height * 0.7, 100, 234)
                self.walkingPlayer.clip_draw(3, 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)

        elif self.phase == 4:
            if self.player.gender == 'male':
                if self.playerX < 0.5:
                    self.playerX += 0.01
                self.walkingPlayer.clip_draw(3 + 46 * self.frame, 0, 47, 117,
                                             game_width * self.playerX, game_height * 0.7, 100, 234)
            elif self.player.gender == 'female':
                if self.playerX > 0.5:
                    self.playerX -= 0.01
                self.walkingPlayer.clip_draw(189 + 52 * self.frame, 0, 53, 117,
                                            game_width * self.playerX, game_height * 0.7, 100, 234)

        elif self.phase == 5:
            self.miniTextbox.draw(game_width * 0.8, game_height * 0.58, 226, 88)
            if self.player.gender == 'male':
                self.walkingPlayer.clip_draw(3 + 46 * self.frame, 0, 47, 117,
                                             game_width * self.playerX, game_height * 0.7, 100, 234)
                if self.select == 0:
                    self.arrow.draw(game_width * 0.66, game_height * 0.605, 12, 20)
                    self.font.draw(game_width * 0.68, game_height * 0.605, '화산')
                    self.font.draw(game_width * 0.66, game_height * 0.55, '상영')
                elif self.select == 1:
                    self.arrow.draw(game_width * 0.66, game_height * 0.55, 12, 20)
                    self.font.draw(game_width * 0.68, game_height * 0.55, '상영')
                    self.font.draw(game_width * 0.66, game_height * 0.605, '화산')

            elif self.player.gender == 'female':
                self.walkingPlayer.clip_draw(189 + 52 * self.frame, 0, 53, 117,
                                            game_width * self.playerX, game_height * 0.7, 100, 234)
                if self.select == 0:
                    self.arrow.draw(game_width * 0.66, game_height * 0.605, 12, 20)
                    self.font.draw(game_width * 0.68, game_height * 0.605, '새싹')
                    self.font.draw(game_width * 0.66, game_height * 0.55, '아리')
                elif self.select == 1:
                    self.arrow.draw(game_width * 0.66, game_height * 0.55, 12, 20)
                    self.font.draw(game_width * 0.68, game_height * 0.55, '아리')
                    self.font.draw(game_width * 0.66, game_height * 0.605, '새싹')

        elif self.phase == 7:
            self.walkingPlayer.clip_draw(400, 0, 51, 117,
                                         game_width * 0.5, game_height * 0.7, 102, 234)\

        elif self.phase == 9:
            if self.player.gender == 'male':
                self.smallPlayer.clip_draw(52 * self.frame, 0, 46, 123,
                                           game_width * 0.5, game_height * 0.7, 102, 146)
            elif self.player.gender == 'female':
                self.smallPlayer.clip_draw(350 + 52 * self.frame, 0, 48, 123,
                                           game_width * 0.5, game_height * 0.7, 102, 146)
            delay(0.5)

        self.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)
        if self.scriptIdx == 21:
            self.font.draw(self.textboxLoc[0] - game_width * 0.4, self.textboxLoc[0],
                          self.player.name + self.script[self.scriptIdx])
        else:
            self.font.draw(self.textboxLoc[0] - game_width * 0.4, self.textboxLoc[0], self.script[self.scriptIdx])

    def update(self):
        self.frame = (self.frame+1) % 4
        if self.phase == 10:
            self.enable = False

    def nextScript(self):
        if self.scriptIdx == 33:
            return
        self.scriptIdx += 1

    def phase3Event(self, _event):
        if self.phase != 3:
            return

        if _event.type == SDL_KEYDOWN:
            if _event.key == SDLK_LEFT and self.select == 1:
                self.select = self.select - 1
            elif _event.key == SDLK_RIGHT and self.select == 0:
                self.select = self.select + 1

            if _event.key == SDLK_SPACE:
                if self.select == -1:
                    return
                elif self.select == 0:
                    self.player.setGender('male')
                    self.playerX = 0.3
                elif self.select == 1:
                    self.player.setGender('female')
                    self.playerX = 0.7
                self.phase += 1
                self.nextScript()

    def phase5Event(self, _event):
        if _event.type == SDL_KEYDOWN and self.phase == 5:
            if _event.key == SDLK_UP:
                if self.select == 1:
                    self.select -= 1
            elif _event.key == SDLK_DOWN:
                if self.select == 0:
                    self.select += 1
            elif _event.key == SDLK_SPACE:
                if self.player.gender == 'male':
                    if self.select == 0:
                        self.player.name = '화산'
                    elif self.select == 1:
                        self.player.name = '상영'
                elif self.player.gender == 'female':
                    if self.select == 0:
                        self.player.name = '새싹'
                    elif self.select == 1:
                        self.player.name = '아리'
                self.phase += 1
                self.nextScript()

    def handle_event(self, _event):
        if self.phase == 3:
            self.phase3Event(_event)
        elif self.phase == 5:
            self.phase5Event(_event)
        elif _event.type == SDL_KEYDOWN and _event.key == SDLK_SPACE:
            self.nextScript()
            self.checkScriptIdx()


    def checkScriptIdx(self):
        if self.scriptIdx in [1, 9, 17, 19, 23, 26, 33]:
            self.phase += 1


    def initScript(self):
        self.script += ('흐음!!', '잘 왔다!', '포켓몬스터의 세계에 온 것을', '환영한다!',
                        '내 이름은 마박사!', '모두가 포켓몬 박사님이라고', '부르고 있단다.', '이 세계에는',
                        '포켓몬스터', "줄여서 '포켓몬'이라 불리는", '신기한 생명체가', '도처에 살고 있다!',
                        '우리 인간은 포켓몬과', '사이좋게 지내고 있단다', '이제 자네에 대해서', '알아보도록 하지',
                        '자네는 남자인가?', '아니면 여자인가?', '그렇군!', '자네의 이름은?', '흐음...',
                        '(이)라고 하는가!', '좋은 이름이구나!', '여기 있는 이 소년은', '자네의 친구였지?',
                        '이름이 바람이로군!', '!!', '이제부터 너만의', '이야기가 시작된다!', '너는 여러 포켓몬이나',
                        '많은 사람들을 만나', '무언가를 발견하게 되겠지!!', '그럼', '포켓몬스터의 세계로!')
