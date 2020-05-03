# Interpreter
This is an interpreter of a simple programming language for robot travelling on a hexagonal grid.

The grid consists of walls, empty cells, cells with boxes on, and an exit cell.

The robot can move into an adjacent cell if there is no obstacle on it. Robot can load and drop boxes.

## Language syntax

Every statement of the language should end with newline. The language is case-insensitive.

### Types

1. `int` - integral decimals and hexadecimals (should end with *h*) of infinite size. Some additional literals are defined: `inf`, `-inf` and `nan`.

2. `bool` - can be `t` or `true`, `f` or `false`, `u` or `undef`.

3. `cell` - a type for cell descriptors: can be `wall`, `box`, `empty`, `exit`, or `undef`.

4. `var` - arbitrary type, will be defined after assignment.


### Type casting

### Variables declaration and assignment

The variable can be declared preliminarily, but it's not obligatory.

The variable type is defined upon declaration and initialization and can be changed upon assigning a value of another type.

Every variable is a one-dimensional array. These arrays may contain links to other variables. Their size is defined upon initialization.
Arrays can be extended if necessary.

The language is strongly typed.

Optional declaration:
`var`|`int`|`cell`|`bool` `name1`,`name2`,`...`

Indexing: `variable(index)`, where index is an integer. If it's incorrect, `undef` will be returned.

Assigning: `variable := another_variable` or `variable(index) := expression`


### Operators

1. Arithmetical - binary plus `+`, binary and unary minus `-`, and `#` - returns the sum of array components (for example, `#array`)
2. Logical - less `<`, greater `>`, equal `=` and xor `^`.

### Loops, conditions and functions

#### While loop
```
while expression do 
    statements 
done
```
 or
```
while expression do 
    statements 
finish 
    statements 
done
```
If the `expression` returns `false`, the `finish` block will be executed once.

#### Conditional

```
if expression do
    statements
done
eldef do
    statements
done
elund do
    statements
done
```

If the `expression` is `false`, `eldef` block will be executed, otherwise if it is `undef`, `elund` block will be executed. `eldef` and `elund` blocks are optional.

#### Functions
##### Declaration:
```
function func_name(arg) do
    statements
    ...
    return
    ...
done
```

##### Usage:
`func_name(arg)`

Functions are isolated scopes and have only one parameter through which it returns values.

Function execution can be interrupted by `return` keyword.

Functions can be declared inside another function. Functions can also be unnamed.

**`main` function is an entry point.**


### Robot operating:

- Move forward/backward: `forward arithmetical_expression` or `backward arithmetical_expression`. If moving is unsuccessful, operators return `false` or `undef`. 
- Turn 60 degrees: `left` or `right`. Can be unsuccessful if robot weight exceeds some limit
- Load and drop box: `load slot` or `drop slot`, where `slot` is a number of slot. Can return `false` if slot ot cell are busy and `undef` is there is nothing to operate with
- `look` returns the distance to the nearest obstacle towards robot
- `test` returns the type of the nearest obstacle towards robot

## Repo description

### Files
**lexer.py**, **parser.py** - lexical and syntax analyzers, both build with Python Lex-Yacc. Receive program text, return syntax tree.

**interpreter.py** - an interpreter. Receives program text, map description, robot description and command line arguments (1 or 0 detecting if the program deals with robot or not). 
Returns error log, robot and map description after interpreting. 

**main.py** - the main file of a project. Receives 4 arguments - program text file, .json file with map and robot description, output file and command line arguments.

There are also some examples of programs and interpreting result: pathfinding program, inputs (map.json and map2.json) and outputs.

Unit tests are also written.

