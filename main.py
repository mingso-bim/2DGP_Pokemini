from pico2d import *
import game_framework
from gameWorld import game_width, game_height
import play_mode as start_mode

open_canvas(game_width, game_height)
game_framework.run(start_mode)
close_canvas()