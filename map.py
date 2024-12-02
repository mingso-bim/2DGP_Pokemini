from pico2d import *
import gameWorld
import pickle
import bush

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
        self.move = False
        self.parent = None
        self.tx, self.ty = 0, 0

    def get_bb(self):
        return self.x - 30, self.y - 10, self.x + 30, self.y + 10

    def handle_collision(self, group, other):
        if gameWorld.get_map().type != self.parent.type:
            return

        other.x, other.y = self.tx, self.ty

        m = None
        if self.target == 'house':
            m = init_house()
            other.scrolling = False
        elif self.target == 'village':
            m = init_village()
            other.scrolling = True
        elif self.target == 'road':
            m = init_road()
            other.scrolling = True

        gameWorld.world[0][0] = m
        self.move = True
        self.parent.remove()


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
        self.bush = []
        self.scrolling = False
        self.window_left = 0
        self.window_bottom = 0
        self.sx, self.sy = 0, 0
        self.type = None

    def render(self):
        self.image.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.cw, self.ch,
            0, self.ch
        )
        if self.scrolling:
            for o in self.ob:
                sl, sb = self.world_to_camera(o.left, o.bottom)
                sr, st = self.world_to_camera(o.right, o.top)
                sb += self.ch
                st += self.ch
                sb = clamp(self.ch, sb, self.ch * 2)
                st = clamp(self.ch, st, self.ch * 2)
                draw_rectangle(sl, sb, sr, st)

            for p in self.portal:
                sl, sb, sr, st = p.get_bb()
                sl, sb = self.world_to_camera(sl, sb)
                sr, st = self.world_to_camera(sr, st)
                sb += self.ch
                st += self.ch
                sb = clamp(self.ch, sb, self.ch * 2)
                st = clamp(self.ch, st, self.ch * 2)
                draw_rectangle(sl, sb, sr, st)
        else:
            for o in self.ob:
                draw_rectangle(*o.get_bb())
            for p in self.portal:
                draw_rectangle(*p.get_bb())

    def update(self):
        self.window_left = clamp(0, int(gameWorld.get_player().x - self.cw // 2), self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(gameWorld.get_player().y - self.ch // 2), self.h - self.ch - 1)

    def handle_event(self, e):
        if (SDL_KEYDOWN, SDLK_SPACE) == (e.type, e.key):
            b = bush.Bush(gameWorld.get_player().x, gameWorld.get_player().y)
            gameWorld.addObject(b, 0)
            gameWorld.add_collision_pair('player:bush', None, b)
            self.bush.append(b)
            print('bush added')

        if e.button == SDL_BUTTON_LEFT:
            if e.type == SDL_MOUSEBUTTONDOWN:
                if self.scrolling:
                    self.sx, self.sy = self.camera_to_world(e.x, self.ch * 2 - e.y - self.ch)
                else:
                    self.sx = e.x
                    self.sy = game_height - e.y

            elif e.type == SDL_MOUSEBUTTONUP:
                if self.scrolling:
                    cx, cy = self.camera_to_world(e.x, self.ch * 2 - e.y - self.ch)
                    if self.sx > cx:
                        self.sx, cx = cx, self.sx
                    if self.sy > cy:
                        self.sy , cy = cy, self.sy

                    o = Obstacle(self.sx, self.sy, cx, cy)
                    self.ob.append(o)
                    gameWorld.addObject(o, 0)
                    gameWorld.add_collision_pair('player:obstacle', None, o)
                    print(f'obstacle added: {o.get_bb()}')

                else:
                    if self.sx > e.x:
                        sx, e.x = e.x, self.sx
                    if self.sy > game_height - e.y:
                        sy, e.y = game_height - e.y, self.sy
                    else:
                        e.y = game_height - e.y

                    o = Obstacle(self.sx, self.sy, e.x, e.y)
                    self.ob.append(o)
                    gameWorld.addObject(o, 0)
                    gameWorld.add_collision_pair('player:obstacle', None, o)

        elif e.button == SDL_BUTTON_RIGHT:
            if e.type == SDL_MOUSEBUTTONDOWN:
                for o in self.ob:
                    if 20 > (o.right - o.left) * (o.top - o.bottom):
                        gameWorld.removeObject(o)
                        self.ob.remove(o)
                    if self.scrolling:
                        cx, cy = self.camera_to_world(e.x, self.ch * 2 - e.y - self.ch)
                        if o.left < cx < o.right:
                            if o.bottom < cy < o.top:
                                gameWorld.removeObject(o)
                                self.ob.remove(o)
                    else:
                        if o.left < e.x < o.right:
                            if o.bottom < gameWorld.game_height - e.y < o.top:
                                gameWorld.removeObject(o)
                                self.ob.remove(o)

    def save_map(self):
        file_name = ''
        if self.type == 'house':
            file_name = 'house.pkl'
        elif self.type == 'village':
            file_name = 'village.pkl'
        elif self.type == 'road':
            file_name = 'road.pkl'
            with open('road_bush.pkl', 'wb') as file:
                pickle.dump(self.bush, file)

        with open(file_name, 'wb') as file:
            pickle.dump(self.ob, file)

    def camera_to_world(self, _x, _y):
        # 카메라 좌표 전달
        x = _x + self.window_left
        y = _y + self.window_bottom
        return x, y

    def world_to_camera(self, _x, _y):
        # 월드 좌표 전달
        x = _x - self.window_left
        y = _y - self.window_bottom
        return x, y

    def remove(self):
        # 맵 객체릉 포함한 ob, portal 정보까지 전부다 삭제하기
        for o in self.ob:
            gameWorld.removeObject(o)
        for p in self.portal:
            gameWorld.removeObject(p)
        if bush:
            for b in self.bush:
                gameWorld.removeObject(b)
        gameWorld.removeObject(self)


def init_house():
    global house
    m = Map()
    m.image = load_image('resource/map/house.png')
    m.w, m.h = m.image.w, m.image.h
    m.type = 'house'

    # ob 생성
    with open('house.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        m.ob.append(o)
        gameWorld.addObject(o, 0)
        gameWorld.add_collision_pair('player:obstacle', None, o)

    # portal 생성
    p = Portal(300, 410, 'village')
    p.tx, p.ty = 330, 320
    m.portal.append(p)
    gameWorld.add_collision_pair('player:portal', None, p)
    p.parent = m
    return m


def init_village():
    global village
    m = Map()
    m.image = load_image('resource/map/map_village.png')
    m.w, m.h = m.image.w, m.image.h
    m.scrolling = True
    m.type = 'village'

    with open(f'village.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        m.ob.append(o)
        gameWorld.addObject(o, 0)
        gameWorld.add_collision_pair('player:obstacle', None, o)

    p = Portal(330, 360, 'house')
    p.tx, p.ty = 300, 450
    m.portal.append(p)
    gameWorld.add_collision_pair('player:portal', None, p)
    p.parent = m

    pp = Portal(510, 940, 'road')
    pp.tx, pp.ty = 2030, 480
    m.portal.append(pp)
    gameWorld.add_collision_pair('player:portal', None, pp)
    pp.parent = m

    return m


def init_road():
    global road
    m = Map()
    m.image = load_image('resource/map/map_road.png')
    m.w, m.h = m.image.w, m.image.h
    m.scrolling = True
    m.type = 'road'

    with open(f'road.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        m.ob.append(o)
        gameWorld.addObject(o, 0)
        gameWorld.add_collision_pair('player:obstacle', None, o)

    with open(f'road_bush.pkl', 'rb') as file:
        loaded_data = pickle.load(file)

    for o in loaded_data:
        o.battle = False
        m.bush.append(o)
        gameWorld.addObject(o, 0)
        gameWorld.add_collision_pair('player:bush', None, o)

    p = Portal(2090, 480, 'village')
    p.tx, p.ty = 510, 900
    m.portal.append(p)
    gameWorld.add_collision_pair('player:portal', None, p)
    p.parent = m

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

