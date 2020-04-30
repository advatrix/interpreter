class CellType:
    type = 'cell'

    def __init__(self):
        pass

    def __repr__(self):
        return self.type


class Empty(CellType):
    type = 'empty'


class Wall(CellType):
    type = 'wall'


class Undef(CellType):
    type = 'undef'


class Exit(CellType):
    type = 'exit'


class Box:
    type = 'box'

    def __init__(self, weight):
        self.weight = weight

    def __repr__(self):
        return f'box, weight: {self.weight}'


class Cell:
    def __init__(self, x, y, type_):
        self.x = x
        self.y = y
        self.type = type_

    def __repr__(self):
        return f'{self.x} {self.y} : {self.type}'
