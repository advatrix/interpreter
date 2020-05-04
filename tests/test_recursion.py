import interpreter

fibonacci = """
    function fib(n) do
        if n < 0 do
            n := -1
            return
        done
        if n < 3 do
            n := 1
            return
        done
        if n = nan do
            n := nan
            return
        done
        int prev := n - 1
        int pprev := n - 2
        fib(prev)
        fib(pprev)
        n := prev + pprev
        return
    done
"""


def test_fibonacci_negative():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := -inf
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == -1


def test_fibonacci_zero():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 0
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 1


def test_fibonacci_one():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 1
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 1


def test_fibonacci_two():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 2
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 1


def test_fibonacci_three():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 3
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 2


def test_fibonacci_four():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 4
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 3


def test_fibonacci_five():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 5
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 5


def test_fibonacci_six():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 6
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 8


def test_fibonacci_seven():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 7
        fib(num)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['num'].value == 13
