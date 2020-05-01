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
    assert intr.sym_table[0]['a'].value.type == 'wall'


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


def test_test_cast():
    intr = interpreter.Interpreter()
    program = """
            function main(argv) do
                left
                forward 1
                left
                forward 1
                right
                forward 1
                right
                int weight := test
            done        
            """
    local_map = deepcopy(map_dict)
    local_robot = deepcopy(robot_description)
    intr.interpret(program, local_map, local_robot, True)
    assert intr.robot.x == -1
    assert intr.robot.y == -1
    assert intr.sym_table[0]['weight'].value == 10


def test_look_at_exit():
    intr = interpreter.Interpreter()
    program = """
                function main(argv) do
                    forward 1
                    right
                    int a := look
                    cell b := test
                done        
                """
    local_map = deepcopy(map_dict)
    local_robot = deepcopy(robot_description)
    intr.interpret(program, local_map, local_robot, True)
    assert intr.sym_table[0]['a'].value == 0
    assert intr.sym_table[0]['b'].value.type == 'exit'
