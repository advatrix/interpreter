import interpreter


def test_plus():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + 2\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 4


def test_int_plus_true():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + true\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 3


def test_int_plus_false():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + f\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 2


def test_int_plus_undef():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + u\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_int_plus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'inf'


def test_int_plus_minus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + -inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == '-inf'


def test_int_plus_nan():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + nan\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_inf_plus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := inf + inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_inf_plus_minus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := inf + -inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_minus():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1 - 18\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == -17


def test_minus_true():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1 - t\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 0


def test_minus_false():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1 - false\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 1


def test_minus_undef():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1 - u\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_minus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1 - inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == '-inf'


def test_minus_minus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1 - -inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'inf'


def test_minus_nan():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1 - nan\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_inf_minus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := inf - inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_inf_minus_minus_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := inf - -inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'


def test_hexadecimal():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := ah\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 10


def test_hexadecimal_expr():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := ffh + 3\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 258


def test_chain_operators():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := ffh + 3 + t - 258\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 1
