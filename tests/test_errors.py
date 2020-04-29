import interpreter


def test_no_main():
    intr = interpreter.Interpreter()
    program = "int a := 7\n"
    intr.interpret(program)
    assert len(intr.errors) == 1
    assert intr.errors[0] == 'Error: no main function'
