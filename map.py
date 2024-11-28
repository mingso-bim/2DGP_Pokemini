from pico2d import *
import gameWorld
import pickle

game_width = 600
game_height = 700

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

class Portal:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target

    def get_bb(self):
        return self.x - 30, self.y + 10, self.x + 30, self.y - 10

    def handle_collision(self, group, other):
        setMap(self.target)


class Map:
    def __init__(self, image):
        self.image = load_image(image)
        self.w, self.h = self.image.w, self.image.h
        self.cw = get_canvas_width()
        self.ch = get_canvas_height() // 2
        self.obstacles = []
        self.portal = []

        self.window_left = 0
        self.window_bottom = 0

    def render(self):
        #self.image.draw(game_width * 0.5, game_height * 0.75, game_width, game_height * 0.5)
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.cw, self.ch,
            0, self.ch
        )
        for o in self.obstacles:
            draw_rectangle(*o.get_bb())
        for p in self.portal:
            draw_rectangle(*p.get_bb())

    def update(self):
        self.window_left = clamp(0, int(gameWorld.get_player().x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(gameWorld.get_player().y - self.cw // 2), self.h - self.ch - 1)

    def handle_event(self, e):
        pass

    def get_window(self):
        return self.window_left, self.window_bottom, self.window_left + self.cw, self.window_bottom + self.ch


class TouchPad:
    def __init__(self):
        self.image = load_image('resource/touchPad.png')

    def render(self):
        self.image.draw(game_width * 0.5, game_height * 0.25, game_width, game_height * 0.5)

    def update(self):
        pass

    def handle_event(self, e):
        pass

global map_house, curMap
def initMap():
    global map_house
    global curMap
    # 맵 - 집
    map_house = Map('resource/map/house.png')
    gameWorld.addObject(map_house, 0)
    curMap = map_house
    # 맵 - 마을
    map_village = Map('resource/map/map_village.png')



    for o in map_house.obstacles:
        gameWorld.add_collision_pair('player:obstacle', None, o)

    portal = Portal(300, 410, map_village)
    map_house.portal.append(portal)
    gameWorld.add_collision_pair('player:portal', None, portal)


def saveMap():
    global map_house
    with open('map_house.pkl', 'wb') as file:
        pickle.dump(map_house.obstacles, file)

def loadMap():
    # 데이터 불러오기
    with open('map_house.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        map_house.obstacles.append(o)
        gameWorld.add_collision_pair('player:obstacle', None, o)

def setMap(m):
    global curMap
    gameWorld.removeObject(curMap)
    gameWorld.addObject(m, 0)
    curMap = m