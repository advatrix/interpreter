from __future__ import annotations
from cell import *
from typing import List


class Robot:
    def __init__(self, x, y, rot, capacity, map_):
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
        #   ^ Y  ^ X
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
        self.slots = dict()
        self.map = map_

    def __repr__(self):
        return f'''({self.x}, {self.y}):{self.rot}
Slots: {self.slots}
Capacity: {self.sum()}/{self.capacity}'''

    def sum(self):
        return sum([box.weight for box in self.slots.values() if box])

    def next(self) -> Cell:
        """Return a Cell towards robot"""
        if self.rot == 0:
            return self.map[self.x][self.y+1]
        if self.rot == 1:
            return self.map[self.x+1][self.y]
        if self.rot == 2:
            return self.map[self.x+1][self.y-1]
        if self.rot == 3:
            return self.map[self.x][self.y-1]
        if self.rot == 4:
            return self.map[self.x-1][self.y]
        if self.rot == 5:
            return self.map[self.x-1][self.y+1]

    def prev(self) -> Cell:
        """Return a Cell backwards robot"""
        if self.rot == 0:
            return self.map[self.x][self.y-1]
        if self.rot == 1:
            return self.map[self.x-1][self.y]
        if self.rot == 2:
            return self.map[self.x-1][self.y+1]
        if self.rot == 3:
            return self.map[self.x][self.y+1]
        if self.rot == 4:
            return self.map[self.x+1][self.y]
        if self.rot == 5:
            return self.map[self.x+1][self.y-1]

    def forward(self, dist) -> str:  # what if cell = undef??
        for i in range(dist):
            if self.next().type.type in ['box', 'wall']:
                if not i:
                    return 'false'
                elif i < dist:
                    return 'undef'
                break
            if self.rot == 0:
                self.y += 1
            elif self.rot == 1:
                self.x += 1
            elif self.rot == 2:
                self.x += 1
                self.y -= 1
            elif self.rot == 3:
                self.y -= 1
            elif self.rot == 4:
                self.x -= 1
            elif self.rot == 5:
                self.y += 1
                self.x -= 1
        return 'true'

    def backward(self, dist) -> str:
        for i in range(dist):
            if self.prev().type.type in ['box', 'wall']:
                if not i:
                    return 'false'
                elif i < dist:
                    return 'undef'
                break
            if self.rot == 0:
                self.y -= 1
            elif self.rot == 1:
                self.x -= 1
            elif self.rot == 2:
                self.x -= 1
                self.y += 1
            elif self.rot == 3:
                self.y += 1
            elif self.rot == 4:
                self.x += 1
            elif self.rot == 5:
                self.y -= 1
                self.x += 1
        return 'true'

    def left(self) -> str:
        if self.sum() < self.capacity:
            self.rot = (self.rot - 1) % 6
            return 'true'
        return 'false'

    def right(self) -> str:
        if self.sum() < self.capacity:
            self.rot = (self.rot + 1) % 6
            return 'true'
        return 'false'

    def load(self, expr: int) -> str:
        if self.next().type.type != 'box':
            return 'undef'
        if expr in self.slots.keys():
            return 'false'
        self.slots[expr] = self.next().type
        self.next().type = Empty()
        return 'true'

    def drop(self, expr: int) -> str:
        if expr not in self.slots.keys():
            return 'undef'
        if self.next().type.type == 'empty' and expr in self.slots.keys():
            self.next().type = self.slots[expr]
            del self.slots[expr]
            return 'true'
        elif self.next().type.type != 'empty':
            return 'false'
        return 'undef'

    def look(self):
        i = 0
        x = self.x
        y = self.y
        while True:
            if self.map[x][y].type.type in ['box', 'wall']:
                return i
            if self.rot == 0:
                y += 1
            elif self.rot == 1:
                x += 1
            elif self.rot == 2:
                x += 1
                y -= 1
            elif self.rot == 3:
                y -= 1
            elif self.rot == 4:
                x -= 1
            elif self.rot == 5:
                y += 1
                x -= 1
            i += 1

    def test(self):
        i = 0
        x = self.x
        y = self.y
        while True:
            i += 1
            next_ = self.map[x][y]
            if next_.type.type in ['box', 'wall', 'exit']:
                return next_.type.type
            if self.rot == 0:
                y += 1
            elif self.rot == 1:
                x += 1
            elif self.rot == 2:
                x += 1
                y -= 1
            elif self.rot == 3:
                y -= 1
            elif self.rot == 4:
                x -= 1
            elif self.rot == 5:
                y += 1
                x -= 1