import interpreter


def test_simple_if():
    intr = interpreter.Interpreter()
    program = """int a
if 2 < 3 do
    a := 1
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 1
    assert intr.sym_table[0]['a'].type == 'int'


def test_eldef():
    intr = interpreter.Interpreter()
    program = """int a
if false > true do
    a := 1
done
eldef do
    a := 4
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 4
    assert intr.sym_table[0]['a'].type == 'int'


def test_elund():
    intr = interpreter.Interpreter()
    program = """int a
if false > undef do
    a := 1
done
elund do
    a := 4
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 4
    assert intr.sym_table[0]['a'].type == 'int'


def test_long_if_true():
    intr = interpreter.Interpreter()
    program = """int a
if false > -5 do
    a := 0
done
eldef do
    a := 1
done
elund do
    a := 2
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 0
    assert intr.sym_table[0]['a'].type == 'int'


def test_long_if_false():
    intr = interpreter.Interpreter()
    program = """int a
if false > 5 do
    a := 0
done
eldef do
    a := 1
done
elund do
    a := 2
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 1
    assert intr.sym_table[0]['a'].type == 'int'


def test_long_if_undef():
    intr = interpreter.Interpreter()
    program = """int a
if 1 > nan do
    a := 0
done
eldef do
    a := 1
done
elund do
    a := 2
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 2
    assert intr.sym_table[0]['a'].type == 'int'
