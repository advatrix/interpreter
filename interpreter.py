#! usr/bin/env python


# TODO: error handling refactoring:
# Interpreter should collect errors and return them afterwards

# TODO: lvalue and rvalue indexing
# map description
# robot loading

from __future__ import annotations
import sys
import parser
import random
from typing import List, NamedTuple, Optional, Tuple
from copy import deepcopy
import robot
import cell
import map


class Var:
    def __init__(self, symtype='var', value=None):
        self.type = symtype
        self.value = value
        
    def __repr__(self):
        return f'{self.type}, {self.value}'

    def __deepcopy__(self, memodict={}):
        return Var(self.type, self.value)


class RedeclarationError(Exception):
    """Exception for re-declared variables"""
    pass


class CastError(Exception):
    """Exception for casting failure"""
    pass


class ReturnError(Exception):
    """Exception for RETURN keyword outside any function"""
    pass


class StopExecution(Exception):
    """Exception for RETURN keyword inside a function (like StopIteration in generators)"""
    pass


class CastManager:
    def __init__(self):
        pass
    
    def __repr__(self):
        return "I'm just a cast manager, and I have nothing interesting to show you!"
    
    @staticmethod
    def cast(type_, var):
        if type_ == var.type:
            return var
        if type_ == 'bool':
            if var.type == 'int':
                return CastManager.int_to_bool(var)
            if var.type == 'cell':
                return CastManager.cell_to_bool(var)
        if type_ == 'int':
            if var.type == 'bool':
                return CastManager.bool_to_int(var)
            if var.type == 'cell':
                return CastManager.cell_to_int(var)
        if type_ == 'cell':
            if var.type == 'bool':
                return CastManager.bool_to_cell(var)
            if var.type == 'int':
                return CastManager.int_to_cell(var)
        else:
            raise ValueError('wrong type')
    
    @staticmethod
    def bool_to_int(value):
        if value.value == 'true':
            return Var('int', 1)
        elif value.value == 'false':
            return Var('int', 0)
        elif value.value == 'undef':
            return Var('int', 'nan')
        raise ValueError
        
    @staticmethod
    def int_to_bool(value):
        if value.value == 0:
            return Var('bool', 'false')
        elif isinstance(value.value, int):
            return Var('bool', 'true')
        raise ValueError
    
    @staticmethod
    def cell_to_bool(value):
        if value.value in ['empty', 'exit']:
            return Var('bool', 'true')
        elif value.value in ['box', 'wall']:
            return Var('bool', 'false')
        return value
    
    @staticmethod
    def bool_to_cell(value):
        if value.value == 'undef':
            return Var('cell', robot.Undef())
        raise CastError
        
    @staticmethod
    def cell_to_int(value):
        if value.value.type == 'empty':
            return Var('int', 0)
        elif value.value.type == 'wall':
            return Var('int', 'inf')
        elif value.value.type == 'box':
            return Var('int', value.weight)
        elif value.value.type == 'exit':
            return Var('int', '-inf')
        elif value.value.type == 'undef':
            return Var('int', 'nan')
        raise ValueError
            
    @staticmethod
    def int_to_cell(value):
        if value.value == 0:
            return Var('cell', cell.Empty())
        elif value.value == 'inf':
            return Var('cell', cell.Wall())
        elif value == '-inf':
            return Var('cell', cell.Exit())
        elif value == 'nan':
            return Var('cell', cell.Undef())
        elif isinstance(value.value, int):
            return Var('cell', cell.Box(value))
        raise ValueError


class Interpreter:
    """
    
    ERRORS:
    (1) - 'nomain' - no main function (no entry point in code)
    (2) - 'redecl' - redeclaration of a variable
    (3) - 'undecl' - undeclared variable usage -- TODO: delete this because it's not an error
    (4) - 'index' - IndexError
    (5) - 'unfunc' - undeclared function usage
    (6) - 'cast' - CastError
    (7) - 'value' - ValueError
    (8) - 'return' - RETURN outside any function
    (9) - 'gen' - this is not a program!
    
    """
       
    def __init__(self, parser=parser.Parser(), caster=CastManager()):
        """
        Object fields:
        self.sym_table -- scoped symbol table: array of symbol tables,
            first index -- scope depth (used in function calls since functions are isolated scopes), 0 by default
            second index -- symbol name as a key in 'symbol table' dict
        """
        self.parser = parser
        self.cast = caster
        self.map = None
        self.program = None
        self.sym_table = [dict()]
        self.scope = 0
        self.robot = self.tree = self.funcs = self.argv = None
        self._rval = False  # rvalue flag
        
    def interpret(self, program: str, map_description: list = None, initial_conditions: Optional[NamedTuple] = None,
                  robot_mode: bool = False, argv: list = None):
        """
        Interpret a program

        Parameters:
            program(str): program text
            map_description(list): a three-dimensional array of Cell objects
            initial_conditions(NamedTuple): initial conditions for robot (position, rotation etc)
            robot_mode(bool): if True, interpret a program for robot, otherwise interpret abstract code
            argv(list[int]): console params vector
        """
        # TODO: robot implementation
        self.map = map_description  # Three-dimensional array of Cell objects
        if robot_mode:
            self.robot = robot.Robot(initial_conditions[x],
                               initial_conditions[y],
                               initial_conditions[z],
                               initial_conditions[rot],
                               initial_conditions[capacity],
                               map_description)
        self.program = program  # Program code
        self.tree, self.funcs = self.parser.parse(program)
        self.argv = argv
        # self._interpret_node(self.tree)
        try:
            self._main(self.funcs['main'])
        except StopExecution:
            pass
    
    def _interpret_node(self, node):
        if node is None:
            return
        if node.type == 'program':
            self._interpret_node(node.children)
        elif node.type == 'stmt_list':
            for child in node.children:
                self._interpret_node(child)
        elif node.type == 'declaration_list':
            vars_type = node.value
            children = node.children.children
            if isinstance(children, list):
                for child in children:
                    self._declaration(child, vars_type)
            else:
                self._declaration(children, vars_type)
        elif node.type == 'variable':
            return self._variable(node)
        elif node.type == 'indexing':
            return self._indexing(node)
        elif node.type == 'const':
            return self._const(node.value)
        elif node.type == 'un_op':
            if node.value == '-':
                return self._negative(node.children)
            elif node.value == '#':
                return self._sum(node.children)
        elif node.type == 'bin_op':
            if node.value == '+':
                return self._plus(node.children[0], node.children[1])
            elif node.value == '-':
                return self._minus(node.children[0], node.children[1])
            elif node.value == '^':
                return self._xor(node.children[0], node.children[1])
            elif node.value == '>':
                return self._gr(node.children[0], node.children[1])
            elif node.value == '<':
                return self._ls(node.children[0], node.children[1])
            elif node.value == '=':
                return self._eq(node.children[0], node.children[1])
        elif node.type == 'function_call':
            self._function_call(node)
        elif node.type == 'operator':
            if node.value.lower() == 'forward':
                return self._forward(node.children)
            elif node.value.lower() == 'backward':
                return self._backward(node.childen)
            elif node.value.lower() == 'left':
                self._left()
            elif node.value.lower() == 'right':
                self._right()
            elif node.value.lower() == 'load':
                return self._load(node.children)
            elif node.value.lower() == 'drop':
                return self._drop(node.children)
            elif node.value.lower() == 'look':
                return self._look()
            elif node.value.lower() == 'test':
                return self._test()
            elif node.value.lower() == 'sizeof':
                return self._sizeof(node.children)
        elif node.type == 'while':
            self._while(node)
        elif node.type == 'if':
            self._if(node)
        elif node.type == 'unnamed_function':
            return self._unnamed_function(node)
        elif node.type == 'function_description':
            pass
        elif node.type == 'assignment':
            self._assignment(node)
        elif node.type == 'return':
            raise StopExecution

    def _main(self, node: parser.SyntaxTreeNode):
        if self.argv:
            argv = [Var('int', arg) for arg in self.argv]
            self.sym_table[0]['argv'] = Var('int', argv)
        try:
            self._interpret_node(node.children['body'])
        except StopExecution:
            pass

    def _assignment(self, node: parser.SyntaxTreeNode):
        var = self._interpret_node(node.children[0])
        expr = self._interpret_node(node.children[1])
        var.type = expr.type
        var.value = expr.value

    def _variable(self, node):
        var = node.value
        return self._find_var(var)

    def _indexing(self, node) -> Var:
        index = self.cast.cast('int', self._interpret_node(node.children))
        if self._rval:  # need to return only value
            var = self._find_var(node.value)
            if var:
                try:
                    return var.value[index.value]
                except IndexError:
                    return Var('bool', 'undef')
            return Var('bool', 'undef')
        var = self._find_var(node.value)
        if not isinstance(var.value, list):
            var.value = [Var(var.type, var.value)]
        try:
            return var.value[index.value]
        except IndexError:
            var.value += \
                [self.cast.cast(var.type, Var('bool', 'undef'))
                 for _ in range(index.value-len(var.value)+1)]  # extend the array
            return var.value[index.value]
        
    def _function_call(self, node):
        param = self._interpret_node(node.children[0]) if isinstance(node.children, list) \
            else self._interpret_node(node.children)
        func_name = node.value
        if func_name not in self.funcs.keys() and func_name not in self.sym_table[self.scope].keys():
            self._error('name', node)
            return
        self.scope += 1
        self.sym_table.append(dict())
        func_subtree = self.funcs[func_name] if func_name in self.funcs.keys() \
            else self.sym_table[self.scope-1][func_name]
        self.sym_table[self.scope][func_subtree.children['param'].value] = param
        try:
            self._interpret_node(func_subtree.children['body'])
        except StopExecution:
            pass
        self.scope -= 1
        self.sym_table.pop()
        
    def _while(self, node):
        try:
            while True:
                condition = self.cast.cast('bool', self._interpret_node(node.children['condition'])).value
                if condition == 'true':
                    self._interpret_node(node.children['body'])
                else:
                    if node.children['finish'] and condition == 'false':
                        self._interpret_node(node.children['finish'])
                    break
        except CastError:
            self._error('cast', node)
        except ValueError:
            self._error('value', node)
        except NameError:
            self._error('name', node)
                
    def _if(self, node):
        condition = self.cast.cast('bool', self._interpret_node(node.children['condition'])).value
        if condition == 'true':
            self._interpret_node(node.children['body'])
        elif condition == 'false':
            self._interpret_node(node.children['eldef'])
        else:
            self._interpret_node(node.children['elund'])
        
    def _unnamed_function(self, node):
        param = self._interpret_node(node.children['param'])
        self.scope += 1
        self.sym_table.append(dict())
        self.sym_table[self.scope][node.children['param'].value] = param
        self._interpret_node(node.children['body'])
        self.scope -= 1
        self.sym_table.pop()

    def _find_var(self, expr) -> Var:
        if expr in self.sym_table[0].keys():
            return self.sym_table[0][expr]
        if expr in self.sym_table[self.scope].keys():
            return self.sym_table[self.scope][expr]
        
    def _sizeof(self, node):
        expr = self._interpret_node(node)
        var = self._find_var(expr)
        if var:
            return Var('int', len(var.value)) if isinstance(var.value, list) else Var('int', 1)
        self._error('undeclared', node)
        
    # ROBOT OPERATORS #
    
    def _forward(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            self.robot.forward(expr)
        except CastError:
            self._error('cast', node)
    
    def _backward(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            self.robot.backward(expr)
        except CastError:
            self._error('cast', node)
            
    def _left(self):
        self.robot.left()
        
    def _right(self):
        self.robot.right()
        
    def _load(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return Var('bool', self.robot.load(expr))
        except CastError:
            self._error('cast', node)
        
    def _drop(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return Var('bool', self.robot.drop(expr))
        except CastError:
            self._error('cast', node)
            
    def _look(self):
        return Var('int', self.robot.look())
    
    def _test(self):
        return Var('cell', self.robot.test())
    
    # ARITHMETICAL AND LOGICAL OPERATORS #
    
    def _negative(self, node):
        expr = self._interpret_node(node)
        try:
            casted_expr = self.cast.cast('int', expr)
            return Var('int', casted_expr.value * (-1))
        except CastError:
            self._error('cast', node)
    
    def _sum(self, node):
        expr = self._interpret_node(node)
        if isinstance(expr.value, list):
            return Var('int', sum([self.cast.cast('int', a).value for a in expr.value]))
        return self.cast.cast('int', expr)
    
    def _plus(self, op1: parser.SyntaxTreeNode, op2: parser.SyntaxTreeNode) -> Var:
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        if 'nan' in [expr1.value, expr2.value] \
                or (expr1.value in ['inf', '-inf'] and expr2.value in ['inf', '-inf']):
            return Var('int', 'nan')
        if expr1.value == 'inf' or expr2.value == 'inf':
            return Var('int', 'inf')
        if expr1.value == '-inf' or expr2.value == '-inf':
            return Var('int', '-inf')
        return Var('int', expr1.value + expr2.value)
    
    def _minus(self, op1: parser.SyntaxTreeNode, op2: parser.SyntaxTreeNode) -> Var:
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        if 'nan' in [expr1.value, expr2.value] \
                or (expr1.value in ['inf', '-inf'] and expr2.value in ['inf', '-inf']):
            return Var('int', 'nan')
        if expr1.value == 'inf' or expr2.value == '-inf':
            return Var('int', 'inf')
        if expr1.value == '-inf' or expr2.value == 'inf':
            return Var('int', '-inf')
        return Var('int', expr1.value - expr2.value)
    
    def _xor(self, op1: parser.SyntaxTreeNode, op2: parser.SyntaxTreeNode) -> Var:
        expr1 = self.cast.cast('bool', self._interpret_node(op1))
        expr2 = self.cast.cast('bool', self._interpret_node(op2))
        if expr1.value == 'undef' or expr2.value == 'undef':
            return Var('bool', 'undef')
        if expr1.value in ['true', 'false'] and expr2.value in ['true', 'false'] and expr1.value != expr2.value:
            return Var('bool', 'true')
        return Var('bool', 'false')
    
    def _gr(self, op1: parser.SyntaxTreeNode, op2: parser.SyntaxTreeNode) -> Var:
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        if expr1.value == 'nan' or expr2.value == 'nan':
            return Var('bool', 'undef')
        if expr1.value == expr2.value and expr1.value in ['inf', '-inf']:
            return Var('bool', 'undef')
        if expr1.value == 'inf' or expr2.value == '-inf':
            return Var('bool', 'true')
        if expr1.value == '-inf' or expr2.value == 'inf':
            return Var('bool', 'false')
        if expr1.value == expr2.value:
            return Var('bool', 'false')
        return Var('bool', 'true') if expr1.value > expr2.value else Var('bool', 'false')
    
    def _ls(self, op1: parser.SyntaxTreeNode, op2: parser.SyntaxTreeNode) -> Var:
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        if expr1.value == 'nan' or expr2.value == 'nan':
            return Var('bool', 'undef')
        if expr1.value == expr2.value and expr1.value in ['inf', '-inf']:
            return Var('bool', 'undef')
        if expr1.value == 'inf' or expr2.value == '-inf':
            return Var('bool', 'false')
        if expr1.value == '-inf' or expr2.value == 'inf':
            return Var('bool', 'true')
        if expr1.value == expr2.value:
            return Var('bool', 'false')
        return Var('bool', 'true') if expr1.value < expr2.value else Var('bool', 'false')
    
    def _eq(self, op1: parser.SyntaxTreeNode, op2: parser.SyntaxTreeNode) -> Var:
        expr1 = self._interpret_node(op1)
        expr2 = self.cast.cast(expr1.type, self._interpret_node(op2))
        if expr1.value == 'nan' or expr2.value == 'nan':
            return Var('bool', 'undef')
        return Var('bool', 'true') if expr1.value == expr2.value else Var('bool', 'false')
    
    # VARIABLES STATEMENTS #
        
    def _const(self, value):
        if value.isdigit():
            return Var('int', int(value))
        elif value == 'inf':
            return Var('int', 'inf')
        elif value == '-inf':
            return Var('int', '-inf')
        elif value == 'nan':
            return Var('int', 'nan')
        elif value in ['t', 'true']:
            return Var('bool', 'true')
        elif value in ['f', 'false']:
            return Var('bool', 'false')
        elif value in ['u', 'undef']:
            return Var('bool', 'undef')
        elif value == 'empty':
            return Var('cell', cell.Empty())
        elif value == 'wall':
            return Var('cell', cell.Wall())
        elif value == 'box':
            return Var('cell', cell.Box(random.randint(0, 100)))
        elif value == 'exit':
            return Var('cell', cell.Exit())
        else:
            return Var('int', int(value[:-1], 16))
                                
    def _declaration(self, node: parser.SyntaxTreeNode, _type: parser.SyntaxTreeNode):
        if node.type == 'vars_list':
            for child in node.children:
                self._declaration(child, _type)
        else:
            try:
                if node.type == 'assignment':
                    self._create_new_var(_type.value, node.children[0].value)
                else:
                    self._create_new_var(_type.value, node.value)
            except RedeclarationError:
                self._error('redecl', node)
                return
        if node.type == 'assignment':
            variable = node.children[0].value
            if node.children[1].type != 'array':
                self._rval = True
                expr = self._interpret_node(node.children[1])
                self._rval = False
                try:
                    self._assign(_type.value, variable, expr, casting=False)
                except CastError:
                    self._error('cast', node)
                except ValueError:
                    self._error('value', node)
            else:
                nodearr = self._array(node.children[1])
                arr = [self._interpret_node(i) for i in nodearr]
                self._assign_array(_type.value, variable, arr)
                
    def _create_new_var(self, _type, name: str):
        if name in self.sym_table[self.scope].keys():
            raise RedeclarationError
        self.sym_table[self.scope][name] = Var(_type, None)
                
    def _assign(self, _type: str, variable: str, expr: Var, casting=True) -> None:
        """Assign a variable to expression

        Parameters:
            casting (bool): flag of variable necessity to be casted to expr type
                for example, if the variable is assigned just after being declared, casting is not needed

        Raises:
            CastError -- if expr casting to variable type was unsuccessful
        """
        # expr = deepcopy(expr)
        var = self._find_var(variable)
        if var:
            if isinstance(expr.value, list):
                self._assign_array(_type, variable, expr.value, casting)
            else:
                if var.type in ['var', expr.type] or casting:
                    var.value = expr.value
                    var.type = expr.type
                else:
                    var.value = self.cast.cast(var.type, expr).value

    def _assign_array(self, _type: str, variable: str, arr: List[Var], casting=True):
        var = self._find_var(variable)
        if var:
            if casting:
                if len({a.type for a in arr}) > 1:  # array elements are of different types
                    var.type = 'var'
                else:
                    var.type = arr[0].type
                var.value = arr
            else:
                var.value = [self.cast.cast(var.type, a) for a in arr]
            
    def _array(self, node) -> list:
        ret = []
        self._array_from_tree(node, ret)
        return ret
        
    def _array_from_tree(self, node, ret: list):
        if node:
            if node.children:
                if isinstance(node.children, list):
                    for child in node.children:
                        self._array_from_tree(child, ret)
                else:
                    self._array_from_tree(node.children, ret)
            else:
                ret.append(node)

    def _error(self, err_type, node=None):
        sys.stderr.write(f'Error {err_type}: ')
        if err_type == 1:
            sys.stderr.write(f'no main function\n')
            return
        elif err_type == 2:
            sys.stderr.write(f'variable "{node.value}" at {node.lineno}:{node.lexpos} is already declared\n')
        elif err_type == 3:
            sys.stderr.write(f'variable "{node.value}" at {node.lineno}:{node.lexpos} is not defined\n')
        elif err_type == 4:
            sys.stderr.write(f'index error "{node.value}" at {node.lineno}:{node.lexpos}\n')
        elif err_type == 5:
            sys.stderr.write(f'Unknown function call "{node.value}" at {node.lineno}:{node.lexpos}\n')
        elif err_type == 6:
            sys.stderr.write(f'failed to cast variable "{node.value}" at {node.lineno}:{node.lexpos}\n')
        elif err_type == 7:
            sys.stderr.write(f'incompatible value and type: "{node.value}" ar {node.lineno}:{node.lexpos}\n')
