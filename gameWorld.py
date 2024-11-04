
game_width = 600
game_height = 700
world = [[], []]

def addObject(o, depth):
    world[depth].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()

def render():
    for layer in world:
        for o in layer:
            o.draw()

def removeObject(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return
