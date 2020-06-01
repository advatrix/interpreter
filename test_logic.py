import interpreter


def test_xor():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := t ^ t\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'false'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_xor_undef():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := u ^ t\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_xor_diff():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := f ^ t\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_ls_int_true():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := 1 < 2\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_ls_int_false():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := inf < 2\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'false'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_ls_int_undef():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := inf < inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_gr_int_undef():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := nan > 5\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_gr_int_undef_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := inf > inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_gr_inf_true():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := inf > -inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_gr_inf_false():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := 5 > inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'false'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_eq_inf():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := inf = inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_eq_nan():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := nan = nan\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_eq_undef():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := undef = undef\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_eq_undef_nan():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := nan = undef\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_eq_expr():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := 2 + 2 = 4\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_eq_wrong_expr():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := 2 + 2 = 5\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'false'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_ls_bool():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := true < false\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'false'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_gr_bool():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := true > false\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_gr_bool_undef():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := true > undef\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'
