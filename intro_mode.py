from pico2d import *
import gameWorld
import game_framework
import startPokemonEvent_mode, play_mode
import effect

game_width, game_height = 600, 700

TIME_PER_ACTION = 0.9
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

class Intro:
    font = None
    background = None
    profMa = None
    walkingPlayer = None
    textbox = None
    miniTextbox = None
    arrow = None
    smallPlayer = None
    sound_button = None
    music = None

    def __init__(self):
        self.phase = 0
        self.frame = 0
        self.select = 0
        self.script = ()
        self.scriptIdx = 0
        self.player = gameWorld.p
        self.playerX = 0
        self.playerFrame = 0
        self.textboxLoc = [game_width / 2, game_height * 0.38]
        self.selected = False

        if Intro.font == None:
            Intro.font = load_font('resource/font.ttf', 55)
        if Intro.background == None:
            Intro.background = load_image('resource/intro/intro_background.png')
        if Intro.profMa == None:
            Intro.profMa = load_image('resource/intro/profMa.png')
        if Intro.walkingPlayer == None:
            Intro.walkingPlayer = load_image('resource/intro/intro_player.png')
        if Intro.textbox == None:
            Intro.textbox = load_image('resource/textbox.png')
        if Intro.miniTextbox == None:
            Intro.miniTextbox = load_image('resource/miniTextbox.png')
        if Intro.arrow == None:
            Intro.arrow = load_image('resource/intro/select.png')
        if Intro.smallPlayer == None:
            Intro.smallPlayer = load_image('resource/intro/smallPlayer.png')
        if Intro.sound_button == None:
            Intro.sound_button = load_wav('resource/sound/button.wav')
            Intro.sound_button.set_volume(32)
        if Intro.music == None:
            Intro.music = load_music('resource/sound/music_intro.mp3')
            Intro.music.repeat_play()
            Intro.music.set_volume(32)

        self.script = ('흐음!!', '잘 왔다!', '포켓몬스터의 세계에 온 것을', '환영한다!',
                  '내 이름은 마박사!', '모두가 포켓몬 박사님이라고', '부르고 있단다.', '이 세계에는',
                  '포켓몬스터', "줄여서 '포켓몬'이라 불리는", '신기한 생명체가', '도처에 살고 있다!',
                  '우리 인간은 포켓몬과', '사이좋게 지내고 있단다', '이제 자네에 대해서', '알아보도록 하지',
                  '자네는 남자인가?', '아니면 여자인가?', '그렇군!', '자네의 이름은?', '흐음...',
                  '(이)라고 하는가!', '좋은 이름이구나!', '자네의 동료를 골라보게!', '좋은 동료를 골랐군!', '여기 있는 이 소년은', '자네의 친구였지?',
                  '이름이 바람이로군!', '!!', '이제부터 너만의', '이야기가 시작된다!', '너는 여러 포켓몬이나',
                  '많은 사람들을 만나', '무언가를 발견하게 되겠지!!', '그럼', '포켓몬스터의 세계로!')

    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
        if self.phase == 10:
            game_framework.change_mode(play_mode)

    def render(self):
        if self.phase == 0:
            Intro.profMa.clip_draw(23, 35, 1, 1, game_width / 2, game_height / 2, game_width, game_height)
            Intro.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)
            Intro.font.draw(self.textboxLoc[0] - game_width * 0.4, game_height * 0.42, self.script[self.scriptIdx])
            update_canvas()
            return

        Intro.background.draw(game_width / 2, game_height / 2, game_width, game_height)
        if self.phase == 1:
            Intro.profMa.clip_draw(0, 0, 67, 133, game_width / 2, game_height * 0.75, 134, 266)
            Intro.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)

        elif self.phase in [2, 6, 8]:
            Intro.profMa.clip_draw(67, 0, 82, 133, game_width / 2, game_height * 0.75, 164, 266)
            Intro.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)

        elif self.phase == 3:
            if self.select == 0:
                Intro.walkingPlayer.clip_draw(3 + 46 * int(self.frame), 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)
                Intro.walkingPlayer.clip_draw(189 + 52, 0, 53, 117, game_width * 0.7, game_height * 0.7, 100, 234)
            elif self.select == 1:
                Intro.walkingPlayer.clip_draw(189 + 52 * int(self.frame), 0, 53, 117, game_width * 0.7, game_height * 0.7, 100,
                                        234)
                Intro.walkingPlayer.clip_draw(3, 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)
            else:
                Intro.walkingPlayer.clip_draw(189 + 52, 0, 53, 117, game_width * 0.7, game_height * 0.7, 100, 234)
                Intro.walkingPlayer.clip_draw(3, 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)

        elif self.phase == 4:
            if self.player.gender == 'male':
                if self.playerX < 0.5:
                    self.playerX += 0.01
                Intro.walkingPlayer.clip_draw(3 + 46 * int(self.frame), 0, 47, 117,
                                        game_width * self.playerX, game_height * 0.7, 100, 234)
            elif self.player.gender == 'female':
                if self.playerX > 0.5:
                    self.playerX -= 0.01
                Intro.walkingPlayer.clip_draw(189 + 52 * int(self.frame), 0, 53, 117,
                                        game_width * self.playerX, game_height * 0.7, 100, 234)

        elif self.phase == 5:
            Intro.miniTextbox.draw(game_width * 0.8, game_height * 0.58, 226, 88)
            if self.player.gender == 'male':
                Intro.walkingPlayer.clip_draw(3 + 46 * int(self.frame), 0, 47, 117,
                                        game_width * self.playerX, game_height * 0.7, 100, 234)
                if self.select == 0:
                    Intro.arrow.draw(game_width * 0.66, game_height * 0.605, 12, 20)
                    Intro.font.draw(game_width * 0.68, game_height * 0.605, '화산')
                    Intro.font.draw(game_width * 0.66, game_height * 0.55, '상영')
                elif self.select == 1:
                    Intro.arrow.draw(game_width * 0.66, game_height * 0.55, 12, 20)
                    Intro.font.draw(game_width * 0.68, game_height * 0.55, '상영')
                    Intro.font.draw(game_width * 0.66, game_height * 0.605, '화산')

            elif self.player.gender == 'female':
                Intro.walkingPlayer.clip_draw(189 + 52 * int(self.frame), 0, 53, 117,
                                        game_width * self.playerX, game_height * 0.7, 100, 234)
                if self.select == 0:
                    Intro.arrow.draw(game_width * 0.66, game_height * 0.605, 12, 20)
                    Intro.font.draw(game_width * 0.68, game_height * 0.605, '새싹')
                    Intro.font.draw(game_width * 0.66, game_height * 0.55, '윤진')
                elif self.select == 1:
                    Intro.arrow.draw(game_width * 0.66, game_height * 0.55, 12, 20)
                    Intro.font.draw(game_width * 0.68, game_height * 0.55, '윤진')
                    Intro.font.draw(game_width * 0.66, game_height * 0.605, '새싹')

        elif self.phase == 7:
            Intro.walkingPlayer.clip_draw(400, 0, 51, 117,
                                    game_width * 0.5, game_height * 0.7, 102, 234)
        elif self.phase == 9:
            while self.playerFrame < 6:
                clear_canvas()
                Intro.background.draw(game_width / 2, game_height / 2, game_width, game_height)
                self.phase9Render(self.playerFrame)
                Intro.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)
                Intro.font.draw(self.textboxLoc[0] - game_width * 0.4, game_height * 0.42, self.script[self.scriptIdx])
                self.playerFrame += 1
                delay(0.4)
                update_canvas()
            self.phase += 1

        Intro.textbox.draw(self.textboxLoc[0], self.textboxLoc[1], game_width * 0.95, game_height * 0.18)
        if self.scriptIdx == 21:
            Intro.font.draw(self.textboxLoc[0] - game_width * 0.4, game_height * 0.42,
                      self.player.name + self.script[self.scriptIdx])
        elif self.scriptIdx == 24 and self.selected == False:
            pass
        else:
            Intro.font.draw(self.textboxLoc[0] - game_width * 0.4, game_height * 0.42, self.script[self.scriptIdx])


    def checkScriptIdx(self):
        if self.scriptIdx in [1, 9, 17, 19, 25, 28, 35]:
            self.phase += 1
            if self.scriptIdx == 1:
                effect.b_fade_in()
            if self.scriptIdx == 9:
                effect.w_blink()
        if self.scriptIdx == 24:
            effect.b_fade_out()
            game_framework.push_mode(startPokemonEvent_mode)
            self.selected = True

    def handle_events(self, e):
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        if self.phase == 3:
            self.phase3Event(e)
        elif self.phase == 5:
            self.phase5Event(e)
        elif e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            self.nextScript()
            self.checkScriptIdx()
            Intro.sound_button.play()

    def nextScript(self):
        if self.scriptIdx == 35:
            return
        self.scriptIdx += 1
        self.select = 0

    def phase3Event(self, _event):
        if _event.type == SDL_KEYDOWN:
            Intro.sound_button.play()
        if self.phase != 3:
            return

        if _event.type == SDL_KEYDOWN:
            if _event.key == SDLK_LEFT and self.select == 1:
                self.select -= 1
            elif _event.key == SDLK_RIGHT and self.select == 0:
                self.select += 1

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
        if _event.type == SDL_KEYDOWN:
            Intro.sound_button.play()
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
                        self.player.name = '윤진'
                self.phase += 1
                self.nextScript()

    def phase9Render(self, frame):
        if self.player.gender == 'male':
            if self.playerFrame == 0:
                Intro.smallPlayer.clip_draw(0, 0, 50, 123,
                                      game_width * 0.5, game_height * 0.7, 100, 246)
            elif self.playerFrame == 1:
                Intro.smallPlayer.clip_draw(55, 0, 44, 123,
                                      game_width * 0.5, game_height * 0.7, 88, 246)
            elif self.playerFrame == 2:
                Intro.smallPlayer.clip_draw(110, 0, 35, 123,
                                      game_width * 0.5, game_height * 0.7, 70, 246)
            elif self.playerFrame == 3:
                Intro.smallPlayer.clip_draw(165, 0, 29, 123,
                                      game_width * 0.5, game_height * 0.7, 58, 246)
            elif self.playerFrame == 4:
                Intro.smallPlayer.clip_draw(220, 0, 22, 123,
                                      game_width * 0.5, game_height * 0.7, 44, 246)

        elif self.player.gender == 'female':
            if self.playerFrame == 0:
                Intro.smallPlayer.clip_draw(345, 0, 58, 123,
                                      game_width * 0.5, game_height * 0.7, 116, 246)
            elif self.playerFrame == 1:
                Intro.smallPlayer.clip_draw(408, 0, 46, 123,
                                      game_width * 0.5, game_height * 0.7, 92, 246)
            elif self.playerFrame == 2:
                Intro.smallPlayer.clip_draw(460, 0, 34, 123,
                                      game_width * 0.5, game_height * 0.7, 68, 246)
            elif self.playerFrame == 3:
                Intro.smallPlayer.clip_draw(499, 0, 26, 123,
                                      game_width * 0.5, game_height * 0.7, 52, 246)
            elif self.playerFrame == 4:
                Intro.smallPlayer.clip_draw(529, 0, 22, 123,
                                      game_width * 0.5, game_height * 0.7, 44, 246)

def init():
    global intro
    intro = Intro()
    gameWorld.addObject(intro, 0)

def update():
    gameWorld.update()

def draw():
    clear_canvas()
    gameWorld.render()
    update_canvas()

def handle_events():
    global intro
    events = get_events()
    for e in events:
        intro.handle_events(e)

def finish():
    effect.b_fade_out()
    gameWorld.clear()

def pause(): pass
def resume(): pass