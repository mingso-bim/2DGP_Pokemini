from pico2d import *
import gameWorld
from gameWorld import game_width, game_height
import pickle


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
    def __init__(self):
        self.image = None
        self.obstacles = []

    def render(self):
        self.image.draw(game_width * 0.5, game_height * 0.75, game_width, game_height * 0.5)
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

map_house = Map()

def initMap():
    global map_house
    map_house = Map()
    map_house.image = load_image('resource/map/house.png')
    #map_house.obstacles.append(Obstacle(168, 500, 241, 600))

    gameWorld.addObject(map_house, 0)
    for o in map_house.obstacles:
        gameWorld.add_collision_pair('player:obstacle', None, o)


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