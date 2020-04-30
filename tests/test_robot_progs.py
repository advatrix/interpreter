import interpreter
from json_convert import convert
from copy import deepcopy

map_dict, robot_description = convert('map.json')


def test_test():
    intr = interpreter.Interpreter()
    program = """
    function main(argv) do
        cell a := test
    done        
    """
    local_map = deepcopy(map_dict)
    local_robot = deepcopy(robot_description)
    intr.interpret(program, local_map, local_robot, True)
    assert intr.sym_table[0]['a'].type == 'cell'
    assert intr.sym_table[0]['a'].value == 'wall'


def test_forward():
    intr = interpreter.Interpreter()
    program = """
    function main(argv) do
        bool b := forward 1
    done        
    """
    local_map = deepcopy(map_dict)
    local_robot = deepcopy(robot_description)
    intr.interpret(program, local_map, local_robot, True)
    assert intr.sym_table[0]['b'].type == 'bool'
    assert intr.sym_table[0]['b'].value == 'true'
    assert intr.robot.x == 2
    assert intr.robot.y == -2


def test_backward():
    intr = interpreter.Interpreter()
    program = """
        function main(argv) do
            bool b := backward 177
        done        
        """
    local_map = deepcopy(map_dict)
    local_robot = deepcopy(robot_description)
    intr.interpret(program, local_map, local_robot, True)
    assert intr.sym_table[0]['b'].type == 'bool'
    assert intr.sym_table[0]['b'].value == 'false'
    assert intr.robot.x == 2
    assert intr.robot.y == -3