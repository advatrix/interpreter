import interpreter


def test_simple_if():
    intr = interpreter.Interpreter()
    program = """int a
if 2 < 3 do
    a := 1
done
eldef do
    a := 0
done
"""
    tree, _ = intr.parser.parse(program)
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 1
    assert intr.sym_table[0]['a'].type == 'int'
