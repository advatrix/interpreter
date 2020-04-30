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


def test_scope():
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

