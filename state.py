from sdl2 import *
import game_framework

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

def rightDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT


def rightUp(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT


def leftDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT


def leftUp(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def upDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP


def upUp(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP


def downDown(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN


def downUp(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN


def space_down(e):
    return (e[0] == 'INPUT' and
            e[1].type == SDL_KEYDOWN and
            e[1].key == SDLK_SPACE)



class RunX:
    @staticmethod
    def enter(player, e):
        if rightDown(e) or leftUp(e):
            player.dirX = 1
            player.dir = 1
        elif leftDown(e) or rightUp(e):
            player.dirX = -1
            player.dir = 3


    @staticmethod
    def exit(player, e):
        player.frame = 0


    @staticmethod
    def do(player):
        player.prevX = player.x
        player.prevY = player.y

        player.x += player.speed * game_framework.frame_time * player.dirX
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def render(player):
        if player.image == None:
            return
        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               player.x, player.y, player.width * 2, player.height * 2)

class RunY:
    @staticmethod
    def enter(player, e):
        if upDown(e) or downUp(e):
            player.dirY = 1
            player.dir = 2
        elif downDown(e) or upUp(e):
            player.dirY = -1
            player.dir = 0

    @staticmethod
    def exit(player, e):
        player.frame = 0

    @staticmethod
    def do(player):
        player.prevX = player.x
        player.prevY = player.y
        player.y += player.speed * game_framework.frame_time * player.dirY
        player.frame = (player.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 3

    @staticmethod
    def render(player):
        if player.image == None:
            return
        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               player.x, player.y, player.width * 2, player.height * 2)


class Idle:
    @staticmethod
    def enter(player, e):
        pass

    @staticmethod
    def exit(player, e):
        pass

    @staticmethod
    def do(player):
        pass

    @staticmethod
    def render(player):
        if player.image == None or player.visible == False:
            return

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               player.x, player.y, player.width * 2, player.height * 2)

