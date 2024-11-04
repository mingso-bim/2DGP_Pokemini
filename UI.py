from pico2d import *

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


class Text(UI):
    def __init__(self, _x, _y, _text):
        super().__init__(_x, _y, 0, 0)
        self.font = load_font('resource/font.ttf', 55)
        self.text = _text

    def render(self):
        self.font.draw(self.x, self.y, self.text)