from sdl2 import *
import game_framework
import math
import gameWorld

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 3

PIXEL_PER_METER = (30.0 / 1.4)
RUN_SPEED_KMPH = 20.0
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

def start_event(e):
    return e[0] == 'START'

def right_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_RIGHT

def right_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_RIGHT

def left_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_LEFT

def left_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_LEFT


def upkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_UP

def upkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_UP

def downkey_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_DOWN

def downkey_up(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYUP and e[1].key == SDLK_DOWN

def space_down(e):
    return e[0] == 'INPUT' and e[1].type == SDL_KEYDOWN and e[1].key == SDLK_SPACE

def time_out(e):
    return e[0] == 'TIME_OUT'


class RunRight:
    @staticmethod
    def enter(player, e):
        player.dirX = 1
        player.dir = 1

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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)


class RunRightUp:
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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)


class RunRightDown:
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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)


class RunLeft:
    @staticmethod
    def enter(player, e):
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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)


class RunLeftUp:
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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)

class RunLeftDown:
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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)


class RunUp:
    @staticmethod
    def enter(player, e):
        player.dirY = 1
        player.dir = 2

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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)


class RunDown:
    @staticmethod
    def enter(player, e):
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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)


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

        sx = player.x - gameWorld.get_map().window_left
        sy = player.y - gameWorld.get_map().window_bottom

        player.image.clip_draw(player.dir * (player.width * 3) + int(player.frame) * player.width, 0,
                               player.width, player.height,
                               sx, sy, player.width * 2, player.height * 2)