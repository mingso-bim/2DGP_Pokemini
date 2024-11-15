from pico2d import *
import game_framework
from gameWorld import game_width, game_height, p
import play_mode

TIME_PER_ACTION = 0.9
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 4

def init():
    global phase, frame, select, script, scriptIdx, player, playerX, textboxLoc, playerFrame
    phase = 0
    frame = 0
    select = 0
    script = ()
    scriptIdx = 0
    player = p
    playerX = 0
    playerFrame = 0
    textboxLoc = [game_width / 2, game_height * 0.38]

    global font, background, profMa, walkingPlayer, textbox, miniTextbox, arrow, smallPlayer
    font = load_font('resource/font.ttf', 55)
    background = load_image('resource/intro/intro_background.png')
    profMa = load_image('resource/intro/profMa.png')
    walkingPlayer = load_image('resource/intro/intro_player.png')
    textbox = load_image('resource/textbox.png')
    miniTextbox = load_image('resource/miniTextbox.png')
    arrow = load_image('resource/intro/select.png')
    smallPlayer = load_image('resource/intro/smallPlayer.png')

    script = ('흐음!!', '잘 왔다!', '포켓몬스터의 세계에 온 것을', '환영한다!',
                        '내 이름은 마박사!', '모두가 포켓몬 박사님이라고', '부르고 있단다.', '이 세계에는',
                        '포켓몬스터', "줄여서 '포켓몬'이라 불리는", '신기한 생명체가', '도처에 살고 있다!',
                        '우리 인간은 포켓몬과', '사이좋게 지내고 있단다', '이제 자네에 대해서', '알아보도록 하지',
                        '자네는 남자인가?', '아니면 여자인가?', '그렇군!', '자네의 이름은?', '흐음...',
                        '(이)라고 하는가!', '좋은 이름이구나!', '여기 있는 이 소년은', '자네의 친구였지?',
                        '이름이 바람이로군!', '!!', '이제부터 너만의', '이야기가 시작된다!', '너는 여러 포켓몬이나',
                        '많은 사람들을 만나', '무언가를 발견하게 되겠지!!', '그럼', '동료를 골라보게!')


def finish():
    global font, background, profMa, walkingPlayer, textbox, miniTextbox, arrow, smallPlayer
    del font, background, profMa, walkingPlayer, textbox, miniTextbox, arrow, smallPlayer

def update():
    global frame, phase
    frame = (frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 4
    if phase == 10:
        game_framework.change_mode(play_mode)

def draw():
    global phase, frame, select, script, scriptIdx, player, playerX, textboxLoc, playerFrame
    global font, background, profMa, walkingPlayer, textbox, miniTextbox, arrow, smallPlayer
    clear_canvas()

    if phase == 0:
        profMa.clip_draw(23, 35, 1, 1, game_width / 2, game_height / 2, game_width, game_height)
        textbox.draw(textboxLoc[0], textboxLoc[1], game_width * 0.95, game_height * 0.18)
        font.draw(textboxLoc[0] - game_width * 0.4, game_height * 0.42, script[scriptIdx])
        update_canvas()
        return

    background.draw(game_width / 2, game_height / 2, game_width, game_height)
    if phase == 1:
        profMa.clip_draw(0, 0, 67, 133, game_width / 2, game_height * 0.75, 134, 266)
        textbox.draw(textboxLoc[0], textboxLoc[1], game_width * 0.95, game_height * 0.18)

    elif phase in [2, 6, 8]:
        profMa.clip_draw(67, 0, 82, 133, game_width / 2, game_height * 0.75, 164, 266)
        textbox.draw(textboxLoc[0], textboxLoc[1], game_width * 0.95, game_height * 0.18)

    elif phase == 3:
        if select == 0:
            walkingPlayer.clip_draw(3 + 46 * int(frame), 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)
            walkingPlayer.clip_draw(189 + 52, 0, 53, 117, game_width * 0.7, game_height * 0.7, 100, 234)
        elif select == 1:
            walkingPlayer.clip_draw(189 + 52 * int(frame), 0, 53, 117, game_width * 0.7, game_height * 0.7, 100,
                                         234)
            walkingPlayer.clip_draw(3, 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)
        else:
            walkingPlayer.clip_draw(189 + 52, 0, 53, 117, game_width * 0.7, game_height * 0.7, 100, 234)
            walkingPlayer.clip_draw(3, 0, 47, 117, game_width * 0.3, game_height * 0.7, 100, 234)

    elif phase == 4:
        if player.gender == 'male':
            if playerX < 0.5:
                playerX += 0.01
            walkingPlayer.clip_draw(3 + 46 * int(frame), 0, 47, 117,
                                         game_width * playerX, game_height * 0.7, 100, 234)
        elif player.gender == 'female':
            if playerX > 0.5:
                playerX -= 0.01
            walkingPlayer.clip_draw(189 + 52 * int(frame), 0, 53, 117,
                                         game_width * playerX, game_height * 0.7, 100, 234)

    elif phase == 5:
        miniTextbox.draw(game_width * 0.8, game_height * 0.58, 226, 88)
        if player.gender == 'male':
            walkingPlayer.clip_draw(3 + 46 * int(frame), 0, 47, 117,
                                         game_width * playerX, game_height * 0.7, 100, 234)
            if select == 0:
                arrow.draw(game_width * 0.66, game_height * 0.605, 12, 20)
                font.draw(game_width * 0.68, game_height * 0.605, '화산')
                font.draw(game_width * 0.66, game_height * 0.55, '상영')
            elif select == 1:
                arrow.draw(game_width * 0.66, game_height * 0.55, 12, 20)
                font.draw(game_width * 0.68, game_height * 0.55, '상영')
                font.draw(game_width * 0.66, game_height * 0.605, '화산')

        elif player.gender == 'female':
            walkingPlayer.clip_draw(189 + 52 * int(frame), 0, 53, 117,
                                         game_width * playerX, game_height * 0.7, 100, 234)
            if select == 0:
                arrow.draw(game_width * 0.66, game_height * 0.605, 12, 20)
                font.draw(game_width * 0.68, game_height * 0.605, '새싹')
                font.draw(game_width * 0.66, game_height * 0.55, '윤진')
            elif select == 1:
                arrow.draw(game_width * 0.66, game_height * 0.55, 12, 20)
                font.draw(game_width * 0.68, game_height * 0.55, '윤진')
                font.draw(game_width * 0.66, game_height * 0.605, '새싹')

    elif phase == 7:
        walkingPlayer.clip_draw(400, 0, 51, 117,
                                     game_width * 0.5, game_height * 0.7, 102, 234)
    elif phase == 9:
        while playerFrame < 6:
            clear_canvas()
            background.draw(game_width / 2, game_height / 2, game_width, game_height)
            phase9Render(playerFrame)
            textbox.draw(textboxLoc[0], textboxLoc[1], game_width * 0.95, game_height * 0.18)
            font.draw(textboxLoc[0] - game_width * 0.4, textboxLoc[0], script[scriptIdx])
            playerFrame += 1
            delay(0.4)
            update_canvas()
        phase += 1

    textbox.draw(textboxLoc[0], textboxLoc[1], game_width * 0.95, game_height * 0.18)
    if scriptIdx == 21:
        font.draw(textboxLoc[0] - game_width * 0.4, game_height * 0.42,
                       player.name + script[scriptIdx])
    else:
        font.draw(textboxLoc[0] - game_width * 0.4, game_height * 0.42, script[scriptIdx])

    update_canvas()

def checkScriptIdx():
    global scriptIdx, phase
    if scriptIdx in [1, 9, 17, 19, 23, 26, 33]:
        phase += 1

def nextScript():
    global scriptIdx, select
    if scriptIdx == 33:
        return
    scriptIdx += 1
    select = 0

def phase3Event(_event):
    global phase, select, player, playerX
    if phase != 3:
        return

    if _event.type == SDL_KEYDOWN:
        if _event.key == SDLK_LEFT and select == 1:
            select = select - 1
        elif _event.key == SDLK_RIGHT and select == 0:
            select = select + 1

        if _event.key == SDLK_SPACE:
            if select == -1:
                return
            elif select == 0:
                player.setGender('male')
                playerX = 0.3
            elif select == 1:
                player.setGender('female')
                playerX = 0.7
            phase += 1
            nextScript()

def phase5Event(_event):
    global phase, select, player, phase
    if _event.type == SDL_KEYDOWN and phase == 5:
        if _event.key == SDLK_UP:
            if select == 1:
                select -= 1
        elif _event.key == SDLK_DOWN:
            if select == 0:
                select += 1
        elif _event.key == SDLK_SPACE:
            if player.gender == 'male':
                if select == 0:
                    player.name = '화산'
                elif select == 1:
                    player.name = '상영'
            elif player.gender == 'female':
                if select == 0:
                    player.name = '새싹'
                elif select == 1:
                    player.name = '윤진'
            phase += 1
            nextScript()

def phase9Render(frame):
    global smallPlayer, player
    if player.gender == 'male':
        if frame == 0:
            smallPlayer.clip_draw(0, 0, 50, 123,
                              game_width * 0.5, game_height * 0.7, 100, 246)
        elif frame == 1:
            smallPlayer.clip_draw(55, 0, 44, 123,
                              game_width * 0.5, game_height * 0.7, 88, 246)
        elif frame == 2:
            smallPlayer.clip_draw(110, 0, 35, 123,
                              game_width * 0.5, game_height * 0.7, 70, 246)
        elif frame == 3:
            smallPlayer.clip_draw(165, 0, 29, 123,
                              game_width * 0.5, game_height * 0.7, 58, 246)
        elif frame == 4:
            smallPlayer.clip_draw(220, 0, 22, 123,
                              game_width * 0.5, game_height * 0.7, 44, 246)

    elif player.gender == 'female':
        if frame == 0:
            smallPlayer.clip_draw(345, 0, 58, 123,
                              game_width * 0.5, game_height * 0.7, 116, 246)
        elif frame == 1:
            smallPlayer.clip_draw(408, 0, 46, 123,
                                  game_width * 0.5, game_height * 0.7, 92, 246)
        elif frame == 2:
            smallPlayer.clip_draw(460, 0, 34, 123,
                                  game_width * 0.5, game_height * 0.7, 68, 246)
        elif frame == 3:
            smallPlayer.clip_draw(499, 0, 26, 123,
                                  game_width * 0.5, game_height * 0.7, 52, 246)
        elif frame == 4:
            smallPlayer.clip_draw(529, 0, 22, 123,
                                  game_width * 0.5, game_height * 0.7, 44, 246)

def handle_events():
    events = get_events()
    for e in events:
        if (e.type, e.key) == (SDL_KEYDOWN, SDLK_ESCAPE):
            game_framework.quit()
        if phase == 3:
            phase3Event(e)
        elif phase == 5:
            phase5Event(e)
        elif e.type == SDL_KEYDOWN and e.key == SDLK_SPACE:
            nextScript()
            checkScriptIdx()


def pause(): pass
def resume(): pass