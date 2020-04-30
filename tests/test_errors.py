import interpreter


def test_no_main():
    intr = interpreter.Interpreter()
    program = "int a := 7\n"
    intr.interpret(program)
    assert len(intr.errors) == 1
    assert intr.errors[0] == 'Error: no main function'


def test_undecl():
    intr = interpreter.Interpreter()
    program = """
    function main(argv) do
        a := 1
    done
    """
    intr.interpret(program)
    assert len(intr.errors) == 1
    assert intr.errors[0].split()[0] == 'UndeclError:'


def test_redecl():
    intr = interpreter.Interpreter()
    program = """
    function main(argv) do
        int a := 1
        int a := 2
    done
    """
    intr.interpret(program)
    assert len(intr.errors) == 1
    assert intr.errors[0].split()[0] == 'RedeclError:'


def test_unfunc():
    intr = interpreter.Interpreter()
    program = """
    function main(argv) do
        int a := 1
        unknown(a)
    done
    """
    intr.interpret(program)
    assert len(intr.errors) == 1
    assert intr.errors[0].split()[0] == 'UnknownFuncError:'


def test_cast():
    intr = interpreter.Interpreter()
    program = """
    function main(argv) do
        cell a := true
    done
    """
    intr.interpret(program)
    assert len(intr.errors) == 1
    assert intr.errors[0].split()[0] == 'CastError:'
