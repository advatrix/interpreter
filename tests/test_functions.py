import interpreter


def test_function_table():
    intr = interpreter.Interpreter()
    program = """function main(a) do
    look
done
"""
    tree, funcs = intr.parser.parse(program)
    assert funcs['main'].children['param'].value == 'a'


def test_multi_functions_table():
    intr = interpreter.Interpreter()
    program = """function main(a) do
        look
    done
    function foo(g) do
        test
    done
"""
    tree, funcs = intr.parser.parse(program)
    assert funcs['main'].children['param'].value == 'a'
    assert funcs['foo'].children['param'].value == 'g'


def test_function_interpretation():
    intr = interpreter.Interpreter()
    program = """function main(a) do
        int a := 2
    done
"""
    intr.interpret(program)
    assert intr.funcs['main'].children['param'].value == 'a'
    assert intr.sym_table[0]['a'].value == 2


def test_return():
    intr = interpreter.Interpreter()
    program = """function main(a) do
            int a := 2
            return
            a := 3
        done
    """
    intr.interpret(program)
    assert intr.funcs['main'].children['param'].value == 'a'
    assert intr.sym_table[0]['a'].value == 2
