from pico2d import *
from gameWorld import game_width, game_height
class Obstacle:
    def __init__(self, l, b, r, t):
        self.left = l
        self.bottom = b
        self.right = r
        self.top = t

    def get_bb(self):
        return self.left, self.bottom, self.right, self.top

    def handle_collision(self, group, other):
        pass

class Map:
    image = None

    def __init__(self):
        Map.image = load_image('resource/map/house.png')
        self.obstacles = []
        self.obstacles.append(Obstacle(100, 500, 200, 600))

    def render(self):
        Map.image.draw(game_width * 0.5, game_height * 0.75, game_width, game_height * 0.5)
        for o in self.obstacles:
            draw_rectangle(*o.get_bb())

    def update(self):
        pass

    def handle_event(self, e):
        pass


class TouchPad:
    def __init__(self):
        self.image = load_image('resource/touchPad.png')

    def render(self):
        self.image.draw(game_width * 0.5, game_height * 0.25, game_width, game_height * 0.5)

    def update(self):
        pass

    def handle_event(self, e):
        pass