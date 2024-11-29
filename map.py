from pico2d import *
import gameWorld
import pickle

game_width = 600
game_height = 700
#map = gameWorld.world[0][0]

startX, startY = 0, 0

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

    def render(self):
        pass

    def update(self):
        pass

    def handle_event(self):
        pass


class Portal:
    def __init__(self, x, y, target):
        self.x = x
        self.y = y
        self.target = target

    def get_bb(self):
        return self.x - 30, self.y - 10, self.x + 30, self.y + 10

    def handle_collision(self, group, other):
        gameWorld.get_map().remove()
        m = None

        if self.target == 'house':
            m = init_house()
        elif self.target == 'village':
            m = init_village()
        elif self.target == 'road':
            m = init_road()

        gameWorld.insertObject(m, 0)

    def render(self):
        pass

    def update(self):
        pass


class Map:
    def __init__(self):
        self.image = None
        self.w, self.h = 0, 0
        self.cw = get_canvas_width()
        self.ch = get_canvas_height() // 2
        self.ob = []
        self.portal = []
        self.scrolling = False
        self.window_left = 0
        self.window_bottom = 0
        self.sx, self.sy = 0, 0

    def render(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.cw, self.ch,
            0, self.ch
        )
        for o in self.ob:
            draw_rectangle(*o.get_bb())
        for p in self.portal:
            draw_rectangle(*p.get_bb())

    def update(self):
        pass

    def handle_event(self, e):
        if e.button == SDL_BUTTON_LEFT:
            if e.type == SDL_MOUSEBUTTONDOWN:
                self.sx = e.x
                self.sy = game_height - e.y
                print(self.sx, self.sy)

            elif e.type == SDL_MOUSEBUTTONUP:
                if self.sx > e.x:
                    sx, e.x = e.x, self.sx
                if self.sy > game_height - e.y:
                    sy, e.y = game_height - e.y, self.sy
                else:
                    e.y = game_height - e.y

                o = Obstacle(self.sx, self.sy, e.x, e.y)
                self.ob.append(o)
                gameWorld.add_collision_pair('player:obstacle', None, o)
                print(e.x, e.y)

        elif e.button == SDL_BUTTON_RIGHT:
            if e.type == SDL_MOUSEBUTTONDOWN:
                for o in self.ob:
                    if 20 > (o.right - o.left) * (o.top - o.bottom):
                        self.ob.remove(o)
                        gameWorld.removeObject(o)
                    if o.left < e.x < o.right:
                        if o.bottom < gameWorld.game_height - e.y < o.top:
                            self.ob.remove(o)
                            gameWorld.removeObject(o)


    def save_map(self):
        with open('village.pkl', 'wb') as file:
            pickle.dump(self.ob, file)

    def change_coordinate(self):
        pass

    def remove(self):
        # 맵 객체릉 포함한 ob, portal 정보까지 전부다 삭제하기
        for o in self.ob:
            gameWorld.removeObject(o)
        for p in self.portal:
            gameWorld.removeObject(p)
        gameWorld.removeObject(self)


def init_house():
    global house
    m = Map()
    m.image = load_image('resource/map/house.png')
    m.w, m.h = m.image.w, m.image.h

    # ob 생성
    with open('house.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        m.ob.append(o)
        gameWorld.add_collision_pair('player:obstacle', None, o)

    # portal 생성
    p = Portal(300, 410, 'village')
    m.portal.append(p)
    gameWorld.add_collision_pair('player:portal', None, p)

    return m


def init_village():
    global village
    m = Map()
    m.image = load_image('resource/map/map_village.png')
    m.w, m.h = m.image.w, m.image.h
    m.scrolling = True

    with open(f'village.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        m.ob.append(o)
        gameWorld.add_collision_pair('player:obstacle', None, o)

    return m


def init_road():
    global road
    m = Map()
    m.image = load_image('resource/map/map_road.png')
    m.w, m.h = m.image.w, m.image.h
    m.scrolling = True

    with open(f'road.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        m.ob.append(o)
        gameWorld.add_collision_pair('player:obstacle', None, o)

    return m



































class TouchPad:
    def __init__(self):
        self.image = load_image('resource/touchPad.png')

    def render(self):
        self.image.draw(game_width * 0.5, game_height * 0.25, game_width, game_height * 0.5)

    def update(self):
        pass

    def handle_event(self, e):
        pass

