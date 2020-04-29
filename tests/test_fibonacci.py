import interpreter

# tests for simple programs

fibonacci = """
function fib(n) do
        if n < 0 do
            n(1) := -1
            return
        done
        if n < 1 do
            n(1) := 1
            return
        done
        if n = nan do
            n(1) := nan
            return
        done
        int i := 1
        int prev := 0
        int curr := 1
        int next := prev + curr
        while i < n do
            next := prev + curr
            prev := curr
            curr := next
            i := i + 1
        finish
            n(1) := curr
            return
        done
    done

"""


def test_fibonacci_negative():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := -inf
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == -1


def test_fibonacci_zero():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 0
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 1


def test_fibonacci_one():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 1
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 1


def test_fibonacci_two():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 2
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 1


def test_fibonacci_three():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 3
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 2


def test_fibonacci_four():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 4
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 3


def test_fibonacci_five():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 5
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 5


def test_fibonacci_six():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 6
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 8


def test_fibonacci_seven():
    intr = interpreter.Interpreter()
    main = """
    function main(argv) do
        int num := 7
        fib(num)
        int res := num(1)
    done
    """
    intr.interpret(fibonacci+main)
    assert intr.sym_table[0]['res'].value == 13
