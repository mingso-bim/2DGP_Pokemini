

class Map:
    house = None
    village = None
    road = None

    def __init__(self):
        if Map.house == None:
            Map.house = load_image('resource/map/house.png')
        if Map.village == None:
            Map.village = load_image('resource/map/map_village.png')
        if Map.road == None:
            Map.road = load_image('resource/map/map_road.png')

        self.cur_map = None
        self.w, self.h = 0, 0
        self.cw = get_canvas_width()
        self.ch = get_canvas_height() // 2

        self.house_ob = []
        self.house_portal = []
        self.village_ob = []
        self.village_portal = []
        self.road_ob = []
        self.road_portal = []

        self.window_left = 0
        self.window_bottom = 0

        self.init_ob()
        self.init_portals()
        self.set_map('v')

    def render(self):
        #self.image.draw(game_width * 0.5, game_height * 0.75, game_width, game_height * 0.5)
        self.cur_map.clip_draw_to_origin(
            self.window_left, self.window_bottom,
            self.cw, self.ch,
            0, self.ch
        )
        if self.cur_map == Map.house:
            for o in self.house_ob:
                draw_rectangle(*o.get_bb())
            for o in self.house_portal:
                draw_rectangle(*o.get_bb())

        elif self.cur_map == Map.village:
            for o in self.village_ob:
                draw_rectangle(*o.get_bb())
            for o in self.village_portal:
                draw_rectangle(*o.get_bb())

        elif self.cur_map == Map.road:
            for o in self.road_ob:
                draw_rectangle(*o.get_bb())
            for o in self.road_portal:
                draw_rectangle(*o.get_bb())


    def init_portals(self):
        portal = Portal(300, 410, Map.village)
        self.house_portal.append(portal)
        gameWorld.add_collision_pair('player:portal', None, portal)

    def init_ob(self):
        with open(f'Map.house.pkl', 'rb') as file:
            loaded_data = pickle.load(file)

        for o in loaded_data:
            self.house_ob.append(o)
            #gameWorld.add_collision_pair('player:obstacle', None, o)

        with open(f'Map.village.pkl', 'rb') as file:
            loaded_data = pickle.load(file)

        for o in loaded_data:
            self.village_ob.append(o)
            #gameWorld.add_collision_pair('player:obstacle', None, o)

        with open(f'Map.road.pkl', 'rb') as file:
            loaded_data = pickle.load(file)

        for o in loaded_data:
            self.road_ob.append(o)
            #gameWorld.add_collision_pair('player:obstacle', None, o)

    def save_map(self):
        if self.cur_map == Map.house:
            with open(f'{self.cur_map}.pkl', 'wb') as file:
                pickle.dump(self.house_ob, file)
        elif self.cur_map == Map.village:
            with open(f'{self.cur_map}.pkl', 'wb') as file:
                pickle.dump(self.village_ob, file)
        elif self.cur_map == Map.road:
            with open(f'{self.cur_map}.pkl', 'wb') as file:
                pickle.dump(self.road_ob + self.road_portal, file)

    def load_map(self, target):
        if self.cur_map == Map.house:
            for o in self.house_ob:
                gameWorld.removeObject(o)
            for o in self.house_portal:
                gameWorld.removeObject(o)

        elif self.cur_map == Map.village:
            for o in self.village_ob:
                gameWorld.removeObject(o)
            for o in self.village_portal:
                gameWorld.removeObject(o)

        elif self.cur_map == Map.road:
            for o in self.road_ob:
                gameWorld.removeObject(o)
            for o in self.road_portal:
                gameWorld.removeObject(o)

        elif self.cur_map == None:
            pass

        self.cur_map = target

        if target == Map.house:
            self.w, self.h = Map.house.w, Map.house.h
            for o in self.house_ob:
                gameWorld.addObject(o, 0)
                gameWorld.add_collision_pair('player:obstacle', None, o)
            for o in self.house_portal:
                gameWorld.addObject(o, 0)
                gameWorld.add_collision_pair('player:portal', None, o)

        elif target == Map.village:
            self.w, self.h = Map.village.w, Map.village.h
            for o in self.village_ob:
                gameWorld.addObject(o, 0)
                gameWorld.add_collision_pair('player:obstacle', None, o)
            for o in self.village_portal:
                gameWorld.addObject(o, 0)
                gameWorld.add_collision_pair('player:portal', None, o)

        elif target == Map.road:
            self.w, self.h = Map.road.w, Map.road.h
            for o in self.road_ob:
                gameWorld.addObject(o, 0)
                gameWorld.add_collision_pair('player:obstacle', None, o)
            for o in self.road_portal:
                gameWorld.addObject(o, 0)
                gameWorld.add_collision_pair('player:portal', None, o)

    def set_map(self, map):
        if map == 'v':
            self.load_map(Map.village)
        elif map == 'h':
            self.load_map(Map.house)
        elif map == 'r':
            self.load_map(Map.road)

    def update(self):
        self.window_left = clamp(0, int(gameWorld.get_player().x) - self.cw // 2, self.w - self.cw - 1)
        self.window_bottom = clamp(0, int(gameWorld.get_player().y - self.cw // 2), self.h - self.ch - 1)

    def handle_event(self, e):
        self.make_ob(e)

    def get_window(self):
        return self.window_left, self.window_bottom, self.window_left + self.cw, self.window_bottom + self.ch

    def make_ob(self, e):
        global startX, startY
        if e.type == SDL_MOUSEBUTTONDOWN:
            if e.button == SDL_BUTTON_LEFT:
                startX = e.x
                startY = gameWorld.game_height - e.y

            if e.button == SDL_BUTTON_RIGHT:
                if self.cur_map == Map.house:
                    for o in self.house_ob:
                        gameWorld.removeObject(o)
                        if 20 > (o.right - o.left) * (o.top - o.bottom):
                            self.house_ob.remove(o)
                            gameWorld.removeObject(o)
                        if o.left < e.x < o.right:
                            if o.bottom < gameWorld.game_height - e.y < o.top:
                                self.house_ob.remove(o)
                                gameWorld.removeObject(o)

                elif self.cur_map == Map.village:
                    for o in self.village_ob:
                        gameWorld.removeObject(o)

                elif self.cur_map == Map.road:
                    for o in self.road_ob:
                        gameWorld.removeObject(o)

                for o in map.map_house.obstacles:
                    if 20 > (o.right - o.left) * (o.top - o.bottom):
                        map.map_house.obstacles.remove(o)
                        gameWorld.remove_collision_object(o)
                    if o.left < e.x < o.right:
                        if o.bottom < gameWorld.game_height - e.y < o.top:
                            map.map_house.obstacles.remove(o)
                            gameWorld.remove_collision_object(o)
                            return
        elif e.type == SDL_MOUSEBUTTONUP:
            if e.button == SDL_BUTTON_RIGHT:
                return
            if startX > e.x:
                startX, e.x = e.x, startX
            if startY > gameWorld.game_height - e.y:
                startY, e.y = gameWorld.game_height - e.y, startY
            else:
                e.y = gameWorld.game_height - e.y

            o = Obstacle(startX, startY, e.x, e.y)
            map.map_house.obstacles.append(o)
            gameWorld.add_collision_pair('player:obstacle', None, o)

