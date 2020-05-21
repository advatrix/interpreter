from __future__ import annotations
import sys
import parser
import random
from typing import List, Optional, Union
import robot
import cell


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


class StopExecution(Exception):
    """Exception for RETURN keyword inside a function (like StopIteration in generators)"""
    pass


class CastManager:
    def __init__(self):
        pass
    
    def __repr__(self):
        return "Cast Manager"
    
    @staticmethod
    def cast(type_: str, var: Var):
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
    def bool_to_int(value: Var) -> Var:
        if value.value == 'true':
            return Var('int', 1)
        elif value.value == 'false':
            return Var('int', 0)
        elif value.value == 'undef':
            return Var('int', 'nan')
        raise ValueError
        
    @staticmethod
    def int_to_bool(value: Var) -> Var:
        if value.value == 0:
            return Var('bool', 'false')
        elif isinstance(value.value, int):
            return Var('bool', 'true')
        raise ValueError
    
    @staticmethod
    def cell_to_bool(value: Var) -> Var:
        if value.value.type in ['empty', 'exit']:
            return Var('bool', 'true')
        elif value.value.type in ['box', 'wall']:
            return Var('bool', 'false')
        return value
    
    @staticmethod
    def bool_to_cell(value: Var) -> Var:
        if value.value == 'undef':
            return Var('cell', robot.Undef())
        raise CastError
        
    @staticmethod
    def cell_to_int(value: Var) -> Var:
        if value.value.type == 'empty':
            return Var('int', 0)
        elif value.value.type == 'wall':
            return Var('int', 'inf')
        elif value.value.type == 'box':
            return Var('int', value.value.weight)
        elif value.value.type == 'exit':
            return Var('int', '-inf')
        elif value.value.type == 'undef':
            return Var('int', 'nan')
        raise ValueError
            
    @staticmethod
    def int_to_cell(value: Var) -> Var:
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
       
    def __init__(self):
        """
        Object fields:
        self.sym_table -- scoped symbol table: array of symbol tables,
            first index -- scope depth (used in function calls since functions are isolated scopes), 0 by default
            second index -- symbol name as a key in 'symbol table' dict
        """
        self.parser = parser.Parser()
        self.cast = CastManager()
        self.map = None
        self.program = None
        self.sym_table = [dict()]
        self.scope = 0
        self.robot = self.tree = self.funcs = self.argv = None
        self._rval = False  # rvalue flag
        self.errors = []
        
    def interpret(self, program: str, map_description: Optional[dict] = None, robot_description: Optional[dict] = None,
                  robot_mode: bool = False, argv: list = None):
        """
        Interpret a program

        Parameters:
            program(str): program text
            map_description(dict): a two-dimensional dict of cells
            robot_description(dict): initial conditions for robot (position, rotation etc)
            robot_mode(bool): if True, interpret a program for robot, otherwise interpret abstract code
            argv(list[int]): console params vector
        """
        self.map = map_description
        if robot_mode:
            self.robot = robot.Robot(robot_description['x'],
                                     robot_description['y'],
                                     robot_description['rotation'],
                                     robot_description['capacity'],
                                     map_description)
        self.program = program  # Program code
        self.tree, self.funcs = self.parser.parse(program)
        self.argv = argv
        self._interpret_node(self.tree)
        if 'main' not in self.sym_table[0].keys():
            self._error('nomain')
        else:
            try:
                self._main(self.sym_table[0]['main'])
            except StopExecution:
                pass
            except RecursionError:
                pass
        for err in self.errors:
            sys.stderr.write(err)

    def _interpret_node(self, node: parser.SyntaxTreeNode) -> Optional[Var]:
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
                return self._backward(node.children)
            elif node.value.lower() == 'left':
                return self._left()
            elif node.value.lower() == 'right':
                return self._right()
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
            self._function_description(node)
        elif node.type == 'assignment':
            self._assignment(node)
        elif node.type == 'return':
            raise StopExecution
        elif node.type == 'array':
            ret = []
            self._array_from_tree(node, ret)
            expr_array = [self._interpret_node(expr) for expr in ret]
            return Var(expr_array[0].type, expr_array)

    def _function_description(self, node: parser.SyntaxTreeNode):
        if node.value not in self.sym_table[self.scope].keys():
            self.sym_table[self.scope][node.value] = node
        else:
            self._error('redecl', node)

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
        if var is None:
            self._error('undecl', node.children[0])
        else:
            var.type = expr.type
            var.value = expr.value

    def _variable(self, node: parser.SyntaxTreeNode):
        var = node.value
        return self._find_var(var)

    def _indexing(self, node: parser.SyntaxTreeNode) -> Var:
        index = self.cast.cast('int', self._interpret_node(node.children))
        if self._rval:  # return only value
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
        
    def _function_call(self, node: parser.SyntaxTreeNode):
        if self.scope == 1000:
            self._error('recursion', node)
            raise RecursionError
        param = self._interpret_node(node.children[0]) if isinstance(node.children, list) \
            else self._interpret_node(node.children)
        func_name = node.value
        if func_name not in self.sym_table[self.scope].keys():
            self._error('unfunc', node)
            return
        self.scope += 1
        self.sym_table.append(dict())
        func_subtree = self.funcs[func_name] if func_name in self.funcs.keys() \
            else self.sym_table[self.scope-1][func_name]
        self.sym_table[self.scope][func_subtree.children['param'].value] = param
        self.sym_table[self.scope][func_name] = func_subtree
        try:
            self._interpret_node(func_subtree.children['body'])
        except StopExecution:
            pass
        self.scope -= 1
        self.sym_table.pop()
        
    def _while(self, node: parser.SyntaxTreeNode):
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
                
    def _if(self, node: parser.SyntaxTreeNode):
        condition = self.cast.cast('bool', self._interpret_node(node.children['condition'])).value
        if condition == 'true':
            self._interpret_node(node.children['body'])
        elif condition == 'false':
            self._interpret_node(node.children['eldef'])
        else:
            self._interpret_node(node.children['elund'])
        
    def _unnamed_function(self, node: parser.SyntaxTreeNode):
        param = self._interpret_node(node.children['param'])
        self.scope += 1
        self.sym_table.append(dict())
        self.sym_table[self.scope][node.children['param'].value] = param
        self._interpret_node(node.children['body'])
        self.scope -= 1
        self.sym_table.pop()

    def _find_var(self, expr: str) -> Var:
        if expr in self.sym_table[0].keys():
            return self.sym_table[0][expr]
        if expr in self.sym_table[self.scope].keys():
            return self.sym_table[self.scope][expr]
        
    def _sizeof(self, node) -> Var:
        expr = self._interpret_node(node)
        var = self._find_var(expr.value)
        if var:
            return Var('int', len(var.value)) if isinstance(var.value, list) else Var('int', 1)
        return Var('int', 'nan')

    # ROBOT OPERATORS #
    
    def _forward(self, node) -> Var:
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return Var('bool', self.robot.forward(expr.value))
        except CastError:
            self._error('cast', node)
    
    def _backward(self, node) -> Var:
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return Var('bool', self.robot.backward(expr.value))
        except CastError:
            self._error('cast', node)
            
    def _left(self) -> Var:
        return Var('bool', self.robot.left())
        
    def _right(self) -> Var:
        return Var('bool', self.robot.right())
        
    def _load(self, node: parser.SyntaxTreeNode) -> Var:
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return Var('bool', self.robot.load(expr.value))
        except CastError:
            self._error('cast', node)
        
    def _drop(self, node: parser.SyntaxTreeNode) -> Var:
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return Var('bool', self.robot.drop(expr.value))
        except CastError:
            self._error('cast', node)
            
    def _look(self) -> Var:
        return Var('int', self.robot.look())
    
    def _test(self) -> Var:
        return Var('cell', self.robot.test())
    
    # ARITHMETICAL AND LOGICAL OPERATORS #
    
    def _negative(self, node: parser.SyntaxTreeNode) -> Var:
        expr = self._interpret_node(node)
        try:
            casted_expr = self.cast.cast('int', expr)
            return Var('int', casted_expr.value * (-1))
        except CastError:
            self._error('cast', node)
    
    def _sum(self, node: parser.SyntaxTreeNode) -> Var:
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
        if expr1.type == 'cell':
            return Var('bool', 'true') if expr1.value.type == expr2.value.type else Var('bool', 'false')
        if expr1.value == 'nan' or expr2.value == 'nan':
            return Var('bool', 'undef')
        return Var('bool', 'true') if expr1.value == expr2.value else Var('bool', 'false')
    
    # VARIABLES STATEMENTS #
        
    def _const(self, value: Union[int, str]) -> Var:
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
                
    def _create_new_var(self, _type: str, name: str):
        """Create new variable in symbol table

        Raises:
            RedeclarationError: if entity (function or variable) with this name already exists at this scope
        """
        if name in self.sym_table[self.scope].keys():
            raise RedeclarationError
        self.sym_table[self.scope][name] = Var(_type, None)
                
    def _assign(self, _type: str, variable: str, expr: Var, casting=True) -> None:
        """Assign variable value to expression

        Parameters:
            casting (bool): flag of variable necessity to be casted to expr type
                for example, if the variable is assigned just after being declared, casting is not needed

        Raises:
            CastError -- if expr casting to variable type was unsuccessful
        """
        var = self._find_var(variable)
        if var:
            if expr is None:
                var.value = self.cast.cast(var.type, Var('bool', 'undef')).value
            elif isinstance(expr.value, list):
                self._assign_array(_type, variable, expr.value, casting)
            else:
                if var.type in ['var', expr.type] or casting:
                    var.value = expr.value
                    var.type = expr.type
                else:
                    var.value = self.cast.cast(var.type, expr).value

    def _assign_array(self, _type: str, variable: str, arr: List[Var], casting=True):
        """Assign variable value to array

        Parameters:
            casting (bool): flag of variable necessity to be casted to expr type
                for example, if the variable is assigned just after being declared, casting is not needed

        Raises:
            CastError -- if expr casting to variable type was unsuccessful
        """
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
            
    def _array(self, node: parser.SyntaxTreeNode) -> list:
        """Return a list of expressions from a node of array type"""
        ret = []
        self._array_from_tree(node, ret)
        return ret
        
    def _array_from_tree(self, node: parser.SyntaxTreeNode, ret: list):
        if node:
            if node.children:
                if isinstance(node.children, list):
                    for child in node.children:
                        self._array_from_tree(child, ret)
                else:
                    self._array_from_tree(node.children, ret)
            else:
                ret.append(node)

    def _error(self, err_type: str, node=None):
        if err_type == 'nomain':
            self.errors.append('Error: no main function')
        elif err_type == 'redecl':
            self.errors.append(
                f'RedeclError: variable "{node.value}" at {node.lineno}:{node.lexpos} is already declared\n')
        elif err_type == 'undecl':
            self.errors.append(f'UndeclError: variable "{node.value}" at {node.lineno}:{node.lexpos} is not defined\n')
        elif err_type == 'unfunc':
            self.errors.append(
                f'UnknownFuncError: Unknown function call "{node.value}" at {node.lineno}:{node.lexpos}\n')
        elif err_type == 'cast':
            self.errors.append(f'CastError: failed to cast variable "{node.value}" at {node.lineno}:{node.lexpos}\n')
        elif err_type == 'value':
            self.errors.append(
                f'ValueError: incompatible value and type: "{node.value}" ar {node.lineno}:{node.lexpos}\n')
        elif err_type == 'recursion':
            self.errors.append(
                f'RecursionError: maximum recursion depth exceeded: "{node.value} at {node.lineno}:{node.lexpos}')
