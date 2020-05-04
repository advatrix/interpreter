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


def test_multiple_errors():
    intr = interpreter.Interpreter()
    program = """
    function main(argv) do
        cell a := true
        b := a
        unknown(a)
        cell a := 5
    done
    """
    intr.interpret(program)
    assert len(intr.errors) == 4
    assert intr.errors[0].split()[0] == 'CastError:'
    assert intr.errors[1].split()[0] == 'UndeclError:'
    assert intr.errors[2].split()[0] == 'UnknownFuncError:'
    assert intr.errors[3].split()[0] == 'RedeclError:'


def test_recursion_exceeding():
    intr = interpreter.Interpreter()
    program = """
    function rec(n) do
        rec(n)
    done
    
    function main(argv) do
        int n := 0
        rec(n)
    done
    """
    intr.interpret(program)
    assert len(intr.errors) == 1
    assert intr.errors[0].split()[0] == 'RecursionError:'