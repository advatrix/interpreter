import robot
from json_convert import convert
from copy import deepcopy

map_dict = convert('map.json')[0]


def test_forward_one():
    x = 2
    y = -3
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.forward(1) == 'true'
    assert r.x == 2
    assert r.y == -2
    assert r.capacity == 100
    assert r.slots == {}


def test_forward_two():
    x = 2
    y = -3
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.forward(2) == 'true'
    assert r.x == 2
    assert r.y == -1


def test_forward_three():
    x = 2
    y = -3
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.forward(3) == 'true'
    assert r.x == 2
    assert r.y == 0


def test_forward_four():
    x = 2
    y = -3
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.forward(4) == 'undef'
    assert r.x == 2
    assert r.y == 0


def test_forward_false():
    x = 2
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.forward(1) == 'false'
    assert r.x == 2
    assert r.y == 0


def test_backward_one():
    x = 2
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.backward(1) == 'true'
    assert r.x == 2
    assert r.y == -1


def test_backward_two():
    x = 2
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.backward(2) == 'true'
    assert r.x == 2
    assert r.y == -2


def test_backward_three():
    x = 2
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.backward(3) == 'true'
    assert r.x == 2
    assert r.y == -3


def test_backward_four():
    x = 2
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.backward(4) == 'undef'
    assert r.x == 2
    assert r.y == -3


def test_backward_false():
    x = 2
    y = -3
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.backward(1) == 'false'
    assert r.x == 2
    assert r.y == -3


def test_left():
    x = 2
    y = -3
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.left() == 'true'
    assert r.rot == 5
    assert r.left() == 'true'
    assert r.rot == 4
    assert r.left() == 'true'
    assert r.rot == 3
    assert r.left() == 'true'
    assert r.rot == 2
    assert r.left() == 'true'
    assert r.rot == 1
    assert r.left() == 'true'
    assert r.rot == 0


def test_right():
    x = 2
    y = -3
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.right() == 'true'
    assert r.rot == 1
    assert r.right() == 'true'
    assert r.rot == 2
    assert r.right() == 'true'
    assert r.rot == 3
    assert r.right() == 'true'
    assert r.rot == 4
    assert r.right() == 'true'
    assert r.rot == 5
    assert r.right() == 'true'
    assert r.rot == 0


def test_load_true():
    x = -1
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, deepcopy(map_dict))
    assert r.load(0) == 'true'
    assert r.capacity == 100
    assert r.slots[0].weight == 10


def test_load_undef():
    x = 2
    y = -1
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.load(0) == 'undef'
    assert r.capacity == 100
    assert 0 not in r.slots.keys()


def test_next():
    x = 0
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.next().x == 0
    assert r.next().y == 1
    r.right()
    assert r.next().x == 1
    assert r.next().y == 0
    r.right()
    assert r.next().x == 1
    assert r.next().y == -1
    r.right()
    assert r.next().x == 0
    assert r.next().y == -1
    r.right()
    assert r.next().x == -1
    assert r.next().y == 0
    r.right()
    assert r.next().x == -1
    assert r.next().y == 1
    r.right()
    assert r.next().x == 0
    assert r.next().y == 1


def test_prev():
    x = 0
    y = 0
    rot = 0
    capacity = 100
    r = robot.Robot(x, y, rot, capacity, map_dict)
    assert r.prev().x == 0
    assert r.prev().y == -1
    r.right()
    assert r.prev().x == -1
    assert r.prev().y == 0
    r.right()
    assert r.prev().x == -1
    assert r.prev().y == 1
    r.right()
    assert r.prev().x == 0
    assert r.prev().y == 1
    r.right()
    assert r.prev().x == 1
    assert r.prev().y == 0
    r.right()
    assert r.prev().x == 1
    assert r.prev().y == -1
    r.right()
    assert r.prev().x == 0
    assert r.prev().y == -1


def test_load_false():
    x = -2
    y = 2
    rot = 2
    capacity = 15
    r = robot.Robot(x, y, rot, capacity, deepcopy(map_dict))
    assert r.load(0) == 'true'
    r.right()
    assert r.load(1) == 'true'
    assert r.right() == 'false'
    assert r.sum() == 20


def test_drop():
    x = -2
    y = 2
    rot = 2
    capacity = 15
    r = robot.Robot(x, y, rot, capacity, deepcopy(map_dict))
    assert r.load(0) == 'true'
    assert r.drop(0) == 'true'
    assert not r.sum()


def test_drop_false():
    x = -2
    y = 2
    rot = 2
    capacity = 15
    r = robot.Robot(x, y, rot, capacity, deepcopy(map_dict))
    assert r.load(0) == 'true'
    r.right()
    assert r.drop(0) == 'false'
    assert r.sum() == 10


def test_drop_undef():
    x = -2
    y = 2
    rot = 2
    capacity = 15
    r = robot.Robot(x, y, rot, capacity, deepcopy(map_dict))
    assert r.drop(9) == 'undef'
    assert not r.sum()


def test_look():
    x = 2
    y = -3
    rot = 0
    capacity = 15
    r = robot.Robot(x, y, rot, capacity, deepcopy(map_dict))
    assert r.look() == 3
    r.forward(1)
    assert r.look() == 2
    r.forward(1)
    assert r.look() == 1
    r.forward(1)
    assert r.look() == 0
    r.backward(2)
    assert r.look() == 2


def test_test():
    x = -2
    y = 2
    rot = 0
    capacity = 15
    r = robot.Robot(x, y, rot, capacity, deepcopy(map_dict))
    assert r.test().type == 'wall'
    r.right()
    r.right()
    assert r.test().type == 'box'
    r.x = 2
    r.y = -2
    r.rot = 1
    assert r.test().type == 'exit'
    r.backward(2)
    assert r.test().type == 'exit'
