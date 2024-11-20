

class Trainer:
    def __init__(self):
        self.name = None
        self.image = None
        self.width, self.height = 0, 0
        self.frame = 0
        self.x, self.y = 280, 500
        self.dir = 1
        self.pokemons = []

    def addPokemon(self, p):
        self.pokemons.append(p)
        