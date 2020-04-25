import pytest
import interpreter

def test_interpreter_interpret_none_node():
    intr = interpreter.Interpreter()
    intr._interpret_node(None)
    assert intr.sym_table == [{}]
    assert intr.scope == 0
    
def test_intr_intr_plus_node():
    intr = interpreter.Interpreter()
    tree, _ = intr.parser.parse('int a := 2\n')
    tree.print()
    res = intr._interpret_node(tree)
    assert res.value == 6
