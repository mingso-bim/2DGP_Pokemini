from pico2d import open_canvas
import player

game_width = 600
game_height = 700

world = [[], []]
collision_pairs = {}
p = player.Player()

def add_collision_pair(group, a, b):
    if group not in collision_pairs:
        collision_pairs[group] = [[], []]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)

def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)

def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)
                    print(f'   collide {group}')

def addObject(o, depth):
    world[depth].append(o)

def insertObject(o, depth):
    world[depth].insert(0, o)

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.render()

def removeObject(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            remove_collision_object(o)
            del o
            return
    print(f'CRITICAL: 존재하지 않는 객체{o}를 지우려고 합니다')

def clear():
    for layer in world:
        layer.clear()

def collide(a, b):
    al, ab, ar, at = a.get_bb()
    bl, bb, br, bt = b.get_bb()

    if al > br: return False
    if ar < bl: return False
    if at < bb: return False
    if ab > bt: return False

    return True

def get_player():
    for layer in world:
        for o in layer:
            if o == p:
                return o
    return None

def get_map():
    return world[0][0]