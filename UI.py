from pico2d import *

game_width = 600
game_height = 700

class UI:
    def __init__(self, _x, _y, _width, _height):
        self.image = None
        self.x = _x
        self.y = _y
        self.width = _width
        self.height = _height
        self.clickable = False
        self.visible = True


    def render(self):
        if self.visible:
            self.image.draw(self.x, self.y, self.width, self.height)


    def handle_event(self):
        pass


    def update(self):
        pass

