import interpreter


def test_indexing():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := [1, 2]\nint b := a(0)\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['b'].value == 1


def test_indexing_assign():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := [1, 2]\na(0) := 5\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value[0].value == 5


def test_multidim_array():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int b := [2, 3]\nint a := [1, b]\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value[0].value == 1
    assert intr.sym_table[0]['a'].value[1].value[0].value == 2
    assert intr.sym_table[0]['a'].value[1].value[1].value == 3


def test_wrong_index():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int b := [2, 3]\nint a := b(16)\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'
    assert intr.sym_table[0]['a'].type == 'int'


def test_number_to_array():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int b := 1\nb(1) := 2\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['b'].value[0].value == 1
    assert intr.sym_table[0]['b'].value[1].value == 2
