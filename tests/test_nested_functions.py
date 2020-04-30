import interpreter


def test_nested_functions():
    program = """
    function main(argv) do
        function inner(a) do
            test
        done
    done
    
    """
    intr = interpreter.Interpreter()
    intr.interpret(program)
    assert 'inner' in intr.sym_table[0].keys()


def test_scope_error():
    program = """
    function outer(a) do
        function inner(b) do
            var c := 1
        done
    done
    
    function main(argv) do
        int a := 1
        inner(a)
    done
    
    """
    intr = interpreter.Interpreter()
    intr.interpret(program)
    assert 'inner' not in intr.sym_table[0].keys()
    assert len(intr.errors) == 1
    assert intr.errors[0].split()[0] == 'UnknownFuncError:'


def test_scope():
    program = """
    function outer(a) do
        function inner(b) do
            b := 1
        done
        a := 3
        inner(a(1))
    done
    
    function main(argv) do
        int a
        outer(a)
    done
    """
    intr = interpreter.Interpreter()
    intr.interpret(program)
    assert intr.sym_table[0]['a'].value[0].value == 3
    assert intr.sym_table[0]['a'].value[1].value == 1
