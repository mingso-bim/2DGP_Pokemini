import player
game_width = 600
game_height = 700
world = [[], []]
p = player.Player()

def addObject(o, depth):
    world[depth].append(o)

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
            return
    print(f'CRITICAL: 존재하지 않는 객체{o}를 지우려고 합니다')

def clear():
    for layer in world:
        layer.clear()