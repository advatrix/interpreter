from __future__ import annotations
from cell import *
from typing import List


class Robot:
    def __init__(self, x, y, z, rot, capacity, map_):
        # Rotation:
        #  -1 <-- -->+1
        #    --------
        #   /   0    \
        #  /5        1\
        # /            \
        # \            /
        #  \4        2/
        #   \   3    /
        #    --------
        #
        #   Coordinates:
        #   ^ Y  ^ Z
        #   |   /
        #   |  /
        #   | /
        #   |/
        #   /
        #
        #
        #
        self.x = x
        self.y = y
        self.rot = rot
        self.capacity = capacity
        self.slots = []
        self.map = map_

    def __repr__(self):
        return f'''({self.x}, {self.y}, {self.z}):{self.rot}
Slots: {self.slots}
Capacity: {self.sum()}/{self.capacity}'''

    def sum(self):
        return sum([box.weight for box in self.slots if box])

    def next(self):
        if self.rot == 0:
            return self.map[self.y + 1][self.x]
        if self.rot == 1:
            return self.map[self.y][self.x + 1]
        if self.rot == 2:
            return self.map[self.y - 1][self.x + 1]
        if self.rot == 3:
            return self.map[self.y - 1][self.x]
        if self.rot == 4:
            return self.map[self.y][self.x - 1]
        if self.rot == 5:
            return self.map[self.y + 1][self.x - 1]

    def forward(self, dist):  # what if cell = undef??
        for i in range(dist):
            if self.rot == 0:
                _next = self.map[self.y + 1][self.x][self.z - 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.y += 1
                self.z -= 1
            elif self.rot == 1:
                _next = self.map[self.y][self.x + 1][self.z - 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.x += 1
                self.z -= 1
            elif self.rot == 2:
                _next = self.map[self.y - 1][self.x + 1][self.z]
                if _next.type.type in ['box', 'wall']:
                    return
                self.x += 1
                self.y -= 1
            elif self.rot == 3:
                _next = self.map[self.y - 1][self.x][self.z + 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.z += 1
                self.y -= 1
            elif self.rot == 4:
                _next = self.map[self.y][self.x - 1][self.z + 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.z += 1
                self.x -= 1
            elif self.rot == 5:
                _next = self.map[self.y + 1][self.x - 1][self.z]
                if _next.type.type in ['box', 'wall']:
                    return
                self.y += 1
                self.x -= 1

    def backward(self, dist):
        for i in range(dist):
            if self.rot == 0:
                _next = self.map[self.y - 1][self.x][self.z + 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.y -= 1
                self.z += 1
            elif self.rot == 1:
                _next = self.map[self.y][self.x - 1][self.z + 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.x -= 1
                self.z += 1
            elif self.rot == 2:
                _next = self.map[self.y + 1][self.x - 1][self.z]
                if _next.type.type in ['box', 'wall']:
                    return
                self.x -= 1
                self.y += 1
            elif self.rot == 3:
                _next = self.map[self.y + 1][self.x][self.z - 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.z -= 1
                self.y += 1
            elif self.rot == 4:
                _next = self.map[self.y][self.x + 1][self.z - 1]
                if _next.type.type in ['box', 'wall']:
                    return
                self.z -= 1
                self.x += 1
            elif self.rot == 5:
                _next = self.map[self.y - 1][self.x + 1][self.z]
                if _next.type.type in ['box', 'wall']:
                    return
                self.y -= 1
                self.x += 1

    def left(self):
        if self.sum() < self.capacity:
            self.rot = (self.rot + 1) % 6

    def right(self):
        if self.sum() < self.capacity:
            self.rot = (2 * self.rot - 1) % 6

    def load(self, expr: int) -> str:
        if self.next().type.type != 'box':
            return 'undef'
        if expr > len(self.slots):
            self.slots += [None for _ in range(expr - len(self.slots) + 1)]
            self.slots[expr] = self.next().type
            return 'true'
        elif self.slots[expr]:
            return 'false'

    def drop(self, expr: int) -> str:
        if self.next.type.type == 'empty' and self.slots[expr]:
            self.next.type = self.slots[expr]
            self.slots[expr] = None
            return 'true'
        elif self.next.type.type != 'empty':
            return 'false'
        else:
            return 'undef'

    def look(self):
        i = 0
        x = self.x
        y = self.y
        z = self.z
        while True:
            i += 1
            if self.map[x][y][z].type.type in ['box', 'wall']:
                return i
            if self.rot == 0:
                y += 1
                z -= 1
            elif self.rot == 1:
                x += 1
                z -= 1
            elif self.rot == 2:
                x += 1
                y -= 1
            elif self.rot == 3:
                z += 1
                y -= 1
            elif self.rot == 4:
                z += 1
                x -= 1
            elif self.rot == 5:
                y += 1
                x -= 1

    def test(self):
        i = 0
        x = self.x
        y = self.y
        z = self.z
        while True:
            i += 1
            if self.map[x][y][z].type.type in ['box', 'wall']:
                return self.map[x][y][z].type.type
            if self.rot == 0:
                y += 1
                z -= 1
            elif self.rot == 1:
                x += 1
                z -= 1
            elif self.rot == 2:
                x += 1
                y -= 1
            elif self.rot == 3:
                z += 1
                y -= 1
            elif self.rot == 4:
                z += 1
                x -= 1
            elif self.rot == 5:
                y += 1
                x -= 1
