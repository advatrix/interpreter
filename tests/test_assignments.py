import pytest
import interpreter


def test_interpreter_interpret_none_node():
    intr = interpreter.Interpreter()
    intr._interpret_node(None)
    assert intr.sym_table == [{}]
    assert intr.scope == 0


def test_intr_int_decl_0_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 2
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_int_decl_expr_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2 + 3\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 5
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_int_decl_inf_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'inf'
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_int_decl_minus_inf_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := -inf\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == '-inf'
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_int_decl_nan_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := nan\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'nan'
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_bool_decl_t_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := t\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_bool_decl_true_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := true\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_bool_decl_f_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := f\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'false'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_bool_decl_false_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := false\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'false'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_bool_decl_u_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := u\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_bool_decl_undef_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := undef\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_cell_decl_undef_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('cell a := undef\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value.type == 'undef'
    assert intr.sym_table[0]['a'].type == 'cell'


def test_intr_cell_decl_box_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('cell a := box\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value.type == 'box'
    assert intr.sym_table[0]['a'].type == 'cell'


def test_intr_cell_decl_wall_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('cell a := wall\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value.type == 'wall'
    assert intr.sym_table[0]['a'].type == 'cell'


def test_intr_cell_decl_empty_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('cell a := empty\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value.type == 'empty'
    assert intr.sym_table[0]['a'].type == 'cell'


def test_intr_cell_decl_exit_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('cell a := exit\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value.type == 'exit'
    assert intr.sym_table[0]['a'].type == 'cell'


def test_intr_mult_int_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 7\nint b := 8\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 7
    assert intr.sym_table[0]['a'].type == 'int'
    assert intr.sym_table[0]['b'].value == 8
    assert intr.sym_table[0]['b'].type == 'int'


def test_intr_redecl_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 7\nint a := 8\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 7
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_cast_int_to_bool_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('bool a := 7\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'true'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_other_var_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 7\nint b := a\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 7
    assert intr.sym_table[0]['a'].type == 'int'
    assert intr.sym_table[0]['b'].value == 7
    assert intr.sym_table[0]['b'].type == 'int'


def test_intr_other_var_expr_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 7\nint b := a + 4\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 7
    assert intr.sym_table[0]['a'].type == 'int'
    assert intr.sym_table[0]['b'].value == 11
    assert intr.sym_table[0]['b'].type == 'int'


def test_intr_var_decl_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('var a\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value is None
    assert intr.sym_table[0]['a'].type == 'var'


def test_intr_var_int_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('var a := 5\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 5
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_var_undef_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('var a := undef\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['a'].type == 'bool'


def test_intr_mult_decl_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('var a, b\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value is None
    assert intr.sym_table[0]['a'].type == 'var'
    assert intr.sym_table[0]['b'].value is None
    assert intr.sym_table[0]['b'].type == 'var'


def test_intr_mult_decl_assign_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('var a, b, c := 4, d, e := t, g\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value is None
    assert intr.sym_table[0]['a'].type == 'var'
    assert intr.sym_table[0]['b'].value is None
    assert intr.sym_table[0]['b'].type == 'var'
    assert intr.sym_table[0]['c'].value == 4
    assert intr.sym_table[0]['c'].type == 'int'
    assert intr.sym_table[0]['d'].value is None
    assert intr.sym_table[0]['d'].type == 'var'
    assert intr.sym_table[0]['e'].value == 'true'
    assert intr.sym_table[0]['e'].type == 'bool'
    assert intr.sym_table[0]['g'].value is None
    assert intr.sym_table[0]['g'].type == 'var'


def test_intr_assign_array_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := [1, 2]\n')
    intr._interpret_node(tree)
    assert len(intr.sym_table[0]['a'].value) == 2
    assert intr.sym_table[0]['a'].value[0].value == 1
    assert intr.sym_table[0]['a'].value[0].type == 'int'
    assert intr.sym_table[0]['a'].value[1].value == 2
    assert intr.sym_table[0]['a'].value[1].type == 'int'
    assert intr.sym_table[0]['a'].type == 'int'


def test_intr_assign_links_arr_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1\nint b := [1, a]\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 1
    assert len(intr.sym_table[0]['b'].value) == 2
    assert intr.sym_table[0]['b'].value[0].value == 1
    assert intr.sym_table[0]['b'].value[1].value == 1


def test_intr_reassign_prog():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 1\na := a + 1\n')
    intr._interpret_node(tree)
    assert intr.sym_table[0]['a'].value == 2


def test_intr_assign_undecl():
    program = """
    function main(argv) do
        bool a := b
        int c := b
        cell d := b
    done
    """
    intr = interpreter.Interpreter()
    intr.interpret(program)
    assert intr.sym_table[0]['a'].value == 'undef'
    assert intr.sym_table[0]['c'].value == 'nan'
    assert intr.sym_table[0]['d'].value.type == 'undef'
