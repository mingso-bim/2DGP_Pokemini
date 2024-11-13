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



class Run:
    @staticmethod
    def enter(player, e):
        if rightDown(e) or leftUp(e):
            player.dir = 1
        elif leftDown(e) or rightUp(e):
            player.dir = 3
        elif upDown(e) or downUp(e):
            player.dir = 2
        elif downDown(e) or upUp(e):
            player.dir = 0

    @staticmethod
    def exit(player, e):
        print(f'player x:{player.x}, player y:{player.y}')
        player.frame = 0

    @staticmethod
    def do(player):
        if player.dir == 0:
            if player.y < 380:
                return
            player.y -= player.speed * game_framework.frame_time

        elif player.dir == 1:
            if player.x > 590:
                return
            player.x += player.speed * game_framework.frame_time

        elif player.dir == 2:
            if player.y > 690:
                return
            player.y += player.speed * game_framework.frame_time

        elif player.dir == 3:
            if player.x < 10:
                return
            player.x -= player.speed * game_framework.frame_time

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
        if player.image == None:
            return

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               player.x, player.y, player.width * 2, player.height * 2)