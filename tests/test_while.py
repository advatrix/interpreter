import interpreter


def test_simple_while():
    intr = interpreter.Interpreter()
    program = """int a := 1, b := 2
while b do
    a := a + 1
    b := b - 1
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 3
    assert intr.sym_table[0]['a'].type == 'int'


def test_simple_while_finish():
    intr = interpreter.Interpreter()
    program = """int a := 1, b := 2
while b do
    a := a + 1
    b := b - 1
finish
    a := a + 1
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 4
    assert intr.sym_table[0]['a'].type == 'int'


def test_simple_finish_undef():
    intr = interpreter.Interpreter()
    program = """int a := 1, b := 2
while nan do
    a := a + 1
    b := b - 1
finish
    a := 0
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 1
    assert intr.sym_table[0]['a'].type == 'int'
