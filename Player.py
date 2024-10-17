from pico2d import *


class Player:
    def __init__(self):
        self.name = "player"
        self.gender = "male"
        self.image = load_image("resource/trainer_boy_sprite.png")
        self.frame = 1
        self.x, self.y = 300, 300
        self.moveable = False
        self.pokemons = []
        self.items = []


    def update(self):
        pass


    def render(self):
        width, height = 0, 0
        self.frame = (self.frame + 1) % 3
        # female
        if self.gender == "female":
            width = 31
            height = 30
        else:
            width = 21
            height = 27

        self.image.clip_draw(width * self.frame, height * 3, width, height,
                             self.x, self.y,  width * 2, height * 2)
        delay(0.5)


    def handle_event(self, _event):
        if _event.type == SDL_KEYDOWN:
            if _event.key == SDLK_RIGHT:
                self.x += 1
            elif _event.key == SDLK_LEFT:
                self.x -= 1
            elif _event.key == SDLK_UP:
                self.y += 1
            elif _event.key == SDLK_DOWN:
                self.y -= 1


