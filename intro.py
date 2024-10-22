from pico2d import load_image
import UI
from UI import game_width, game_height


class Intro:
    def __init__(self):
        self.phase = 0
        self.background = load_image('resource/intro/intro_background.png')
        self.doctorOh = load_image('resource/intro/doctor_oh.png')
        self.walkingPlayer = load_image('resource/intro/intro_player.png')


    def render(self):
        self.background.draw(game_width/2, game_height/2, game_width, game_height)
        if self.phase == 0:
            self.doctorOh.clip_draw(0, 0, 79, 133, game_width/2, game_height * 0.7)
        elif self.phase == 1:
            pass