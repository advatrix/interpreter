#! /usr/bin/env python


# TODO: error handling refactoring
# map description
# robot loading

from __future__ import annotations
import sys
import parser
from typing import List

class Robot:
    def __init__(self, x, y, z, rot, capacity, map_):
        """ Rotation:
          -1 <-- -->+1
           --------
          /   0    \   
         /5        1\
        /            \ 
        \            /
         \4        2/
          \   3    /
           --------

           Coordinates:
           ^ X  ^ Y
           |   /
           |  /
           | /
           |/
           /\
             \
              V Z


        """ 
        self.x = x
        self.y = y
        self.z = z
        self.rot = rot
        self.capacity = capacity
        self.slots = []
        self.map = map_
        
    def __repr__(self):
        return f'''({self.x}, {self.y}, {self.z}):{self.rot}
Slots: {self.slots}
Capacity: {self.sum()}/{self.capacity}'''
    
    def sum(self):
        return sum([box.weight for box in self.slots if box])
    
    def next(self):
        if rot == 0:
            return self.map[self.y+1][self.x][self.z-1]
        if rot == 1:
            return self.map[self.y][self.x+1][self.z-1]
        if rot == 2:
            return self.map[self.y-1][self.x+1][self.z]
        if rot == 3:
            return self.map[self.y-1][self.x][self.z+1]
        if rot == 4:
            return self.map[self.y][self.x-1][self.z+1]
        if rot == 5:
            return self.map[self.y+1][self.x-1][self.z]
        
    def forward(self, dist): # what if cell = undef??
        for i in range(dist):
            if rot == 0:
                next = self.map[self.y+1][self.x][self.z-1]
                if next.type.type in ['box', 'wall']:
                    return
                self.y += 1
                self.z -= 1
            elif rot == 1:
                next = self.map[self.y][self.x+1][self.z-1]
                if next.type.type in ['box', 'wall']:
                    return
                self.x += 1
                self.z -= 1
            elif rot == 2:
                next = self.map[self.y-1][self.x+1][self.z]
                if next.type.type in ['box', 'wall']:
                    return
                self.x += 1
                self.y -= 1
            elif rot == 3:
                next = self.map[self.y-1][self.x][self.z+1]
                if next.type.type in ['box', 'wall']:
                    return
                self.z += 1
                self.y -= 1
            elif rot == 4:
                next = self.map[self.y][self.x-1][self.z+1]
                if next.type.type in ['box', 'wall']:
                    return
                self.z += 1
                self.x -= 1
            elif rot == 5:
                next = self.map[self.y+1][self.x-1][self.z]
                if next.type.type in ['box', 'wall']:
                    return
                self.y += 1
                self.x -= 1
                    
    def backward(self, dict):
        for i in range(dist):
            if rot == 0:
                next = self.map[self.y-1][self.x][self.z+1]
                if next.type.type in ['box', 'wall']:
                    return
                self.y -= 1
                self.z += 1
            elif rot == 1:
                next = self.map[self.y][self.x-1][self.z+1]
                if next.type.type in ['box', 'wall']:
                    return
                self.x -= 1
                self.z += 1
            elif rot == 2:
                next = self.map[self.y+1][self.x-1][self.z]
                if next.type.type in ['box', 'wall']:
                    return
                self.x -= 1
                self.y += 1
            elif rot == 3:
                next = self.map[self.y+1][self.x][self.z-1]
                if next.type.type in ['box', 'wall']:
                    return
                self.z -= 1
                self.y += 1
            elif rot == 4:
                next = self.map[self.y][self.x+1][self.z-1]
                if next.type.type in ['box', 'wall']:
                    return
                self.z -= 1
                self.x += 1
            elif rot == 5:
                next = self.map[self.y-1][self.x+1][self.z]
                if next.type.type in ['box', 'wall']:
                    return
                self.y -= 1
                self.x += 1
        
    def left(self):
        if self.sum() < self.capacity:
            self.rot = (self.rot + 1) % 6
    
    def right(self):
        if self.sum() < self.capacity:
            self.to = (2 * self.rot - 1) % 6
        
    def load(self, expr):
        if self.next.type.type != 'box':
            return Var('bool', 'undef')
        if expr > len(self.slots):
            self.slots += [None for _ in range(expr-len(self.slots)+1)]
            self.slots[expr] = self.next.type
            return Var('bool', 'true')
        elif self.slots[expr]:
            return Var('bool', 'false')
        
        
    def drop(self, expr):
        if self.next.type.type == 'empty' and self.slots[expr]:
            self.next.type = self.slots[expr]
            self.slots[expr] = None
            return Var('bool', 'true')
        elif self.next.type.type != 'empty':
            return Var('bool', 'false')
        else:
            return Var('bool', 'undef')
        
    def look(self):
        i = 0
        x = self.x
        y = self.y
        z = self.z
        while True:
            i += 1
            if self.map[x][y][z].type.type in ['box', 'wall']:
                return Var('int', i)
            if rot == 0:
                y += 1
                z -= 1
            elif rot == 1:
                x += 1
                z -= 1
            elif rot == 2:
                x += 1
                y -= 1
            elif rot == 3:
                z += 1
                y -= 1
            elif rot == 4:
                z += 1
                x -= 1
            elif rot == 5:
                y += 1
                x -= 1
        
    def test(self):
        i = 0
        x = self.x
        y = self.y
        z = self.z
        while True:
            i += 1
            if self.map[x][y][z].type.type in ['box', 'wall']:
                return Var('cell', self.map[x][y][z].type.type)
            if rot == 0:
                y += 1
                z -= 1
            elif rot == 1:
                x += 1
                z -= 1
            elif rot == 2:
                x += 1
                y -= 1
            elif rot == 3:
                z += 1
                y -= 1
            elif rot == 4:
                z += 1
                x -= 1
            elif rot == 5:
                y += 1
                x -= 1
                
                
                        

class Var:
    def __init__(self, symtype='var', symvalue=None):
        self.type = symtype
        self.value = symvalue
        
    def __repr__(self):
        return f'{self.type}, {self.value}'


class RedeclarationError(Exception):
    """Exception for redeclared variables"""
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





class Cell:
    def __init__(self, x, y, z, type_):
        self.x = x
        self.y = y
        self.z = z
        self.type = type_
        
    def __repr__(self):
        return f'{self.x} {self.y} {self.z} : {self.type_}'

class CellType:
    type = 'cell'
    
    def __init__(self):
        pass
    
    def __repr__(self):
        return self.type

class Empty(CellType):
    type = 'empty'

    
class Wall(CellType):
    type = 'wall'


        
class Undef(CellType):
    type = 'undef'
    
    def __init__(self):
        pass
    
class Box:
    type = 'box'
    
    def __init__(self, weight):
        self.weight = weight
        
    def __repr__(self):
        return f'box, weight: {self.weight}'
    
class Exit:
    type = 'exit'
    
    def __init__(self):
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
                return int_to_bool(var)
            if var.type == 'cell':
                return cell_to_bool(var)
        if type_ == 'int':
            if var.type == 'bool':
                return bool_to_int(var)
            if var.type == 'cell':
                return cell_to_int(var)
        if type_ == 'cell':
            if var.type == 'bool':
                return bool_to_cell(var)
            if var.type == 'int':
                return int_to_cell(var)
        else:
            raise ValueError('wrong type')
    
    @staticmethod # TODO: return Var (SymTableItem) instance
    def bool_to_int(value):
        if value.value == 'true':
            return Var('int', 1)
        elif value.value == 'false':
            return Var('int', 0)
        elif value.value == 'undef':
            return Var('int', 'undef')
        raise ValueError
        
    @staticmethod
    def int_to_bool(value):
        if value.value == '0':
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
            return Var('cell', Undef())
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
        raise InterpretValueError
            
    @staticmethod
    def int_to_cell(value):
        if value.value == 0:
            return Var('cell', Empty())
        elif value.value == 'inf':
            return Var('cell', Wall())
        elif value == '-inf':
            return Var('cell', Exit())
        elif value == 'nan':
            return Var('cell', Undef())
        elif isinstance(value.value, int):
            return Var('cell', Box(value))
        raise ValueError


class Interpreter:
    """
    
    ERRORS:
    (1) - 'nomain' - no main function (no entry point in code)
    (2) - 'redecl' - redeclaration of a variable
    (3) - 'undecl' - undeclared variable usage
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
        self.Robot = None
        
    def interpret(self, map_description, program):
        self.map = map_description  # Three-dimensional array of Cell objects
        self.program = program  # Program code
        self.robot: Robot = None  #implement it
        try:
            self.tree, self.funcs = self.parser.parse(program)
        except:
            self._error('gen')
            return
        if 'main' not in funcs.keys():
            self._error('nomain')
            return
        self._interpret_tree(tree)
        self._interpret_tree(funcs['main'])
        
    def _interpret_tree(self, tree):
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
            expr = self._interpret_node(node.children)
            try:
                ret = self.sym_table[node.value][expr]
                return ret
            except KeyError:
                self._error(self.errors['undeclared'], node)
            except IndexError:
                self._error(self.error['index_error'], node)
            return
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
                self.right()
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
            elif node.value.lower() == 'return':
                self._return(node)
        elif node.type == 'while':
            self._while(node)
        elif node.type == 'if':
            self._if(node)
        elif node.type == 'unnamed_function':
            return self._unnamed_function(node)
        elif node.type == 'function_description':
            pass
        
    def _return(self, node):
        if not self.scope_depth:
            self._error('return', node)
        else:
            raise StopExecution
            
        
    def _variable(self, node):
        var = node.value
        if var not in self.sym_table[self.scope].keys():
            self._error('name', node)
            return
        return self.sym_table[self.scope][var]
    
    def _indexing(self, node):
        try:
            var = node.value
            index = self.cast.cast('int', self._interpret_node(node.children))
            if index == len(self.sym_table[self.scope][var]):
                self.sym_table[self.scope][var].append(Var())
            elif index > len(self.sym_table[self.scope][var]):
                self._error('index', node)
                return
            return self.sym_table[self.scope][var][index]
        except ValueError:
            self._error('value', node)
        except CastError:
            self._error('cast', node)
        except NameError:
            self._error('name', node)  
        
    def _function_call(self, node):
        param = self._interpret_node(node.children)
        func = node.value
        if func not in self.funcs.keys() and func not in self.sym_table[self.scope].keys():
            self._error('name', node)
            return
        self.scope += 1
        self.sym_table.append(dict())
        func_subtree = self.funcs[func] or self.sym_table[self.scope-1][func]
        self.sym_table[self.scope][func_subtree.children['param'].value] = param
        self._interpret_tree(func_subtree.children['body'])
        self.scope -= 1
        self.sym_table.pop()
        
    def _while(self, node):
        try:
            while self.cast.cast('bool', node.children['condition']).value == 'true':
                self._interpret_node(node.children['body'])
            if node.children['finish']:
                self._interpret_node(node.children['finish'])
        except CastError:
            self._error('cast', node)
        except ValueError:
            self._error('value', node)
        except NameError:
            self._error('name', node)
                
    def _if(self, node):
        condition = self.cast.cast('bool', node.children['condition']).value
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
        
        
    def _sizeof(self, node):
        expr = self._interpret_node(node)
        if expr not in self.sym_table.keys():
            self._error(errors['value'], node)
            return
        if isinstance(self.sym_table[expr].value, list):
            return Var('int', len(self.sym_table[expr].value))
        else:
            return Var('int', 1)
        
    ### ROBOT OPERATORS ###
    
    def _forward(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            self.robot.forward(expr)
        except CastError:
            self._error(errors['cast'], node)
    
    def _backward(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            self.robot.backward(expr)
        except CastError:
            self._error(errors['cast'], node)
            
    def _left(self):
        self.robot.left()
        
    def _right(self):
        self.robot.right()
        
    def _load(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return self.robot.load(expr)
        except CastError:
            self._error(errors['cast'], node)
        
    def _drop(self, node):
        try:
            expr = self.cast.cast('int', self._interpret_node(node))
            return self.robot.drop(expr)
        except CastError:
            self._error(errors['cast'], node)  
            
    def _look(self):
        return self.robot.look()
    
    def _test(self):
        return self.robot.test()
    
    ### ARITHMETICAL AND LOGICAL OPERATORS ###
    
    def _negative(self, node):
        expr = self._interpret_node(node)
        return (-1) * self.cast.cast('int', expr)
    
    def _sum(self, node):
        expr = self._interpret_node(node)
        if isinstance(expr, list):
            return sum([self.cast.cast('int', a) for a in expr])
        return self.cast.cast('int', expr)
    
    def _plus(self, op1, op2):
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        return Var('int', expr1.value + expr2.value)
    
    def _minus(self, op1, op2):
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        return Var('int', expr1.value - expr2.value)
    
    def _xor(self, op1, op2):
        expr1 = self.cast.cast('bool', self._interpret_node(op1))
        expr2 = self.cast.cast('bool', self._interpret_node(op2))
        if expr1.value in ['true', 'false'] and expr2.value in ['true', 'false'] and expr1.value != expr2.value:
            return Var('bool', 'true')
        return Var('bool', 'false')
    
    def _gr(self, op1, op2):
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        return Var('bool', 'true') if expr1.value > expr2.value else Var('bool', 'false')
    
    def _ls(self, op1, op2):
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        return Var('bool', 'true') if expr1.value < expr2.value else Var('bool', 'false')
    
    def _eq(self, op1, op2):
        expr1 = self.cast.cast('int', self._interpret_node(op1))
        expr2 = self.cast.cast('int', self._interpret_node(op2))
        return Var('bool', 'true') if expr1.value < expr2.value else Var('bool', 'false')
    
    ### VARIABLES STATEMENTS ###
        
    def _const(self, value):
        if value.isdigit():
            return Var('int', int(value))
        else:
            return Var('int', int(value, 16))
                                
    def _declaration(self, node, _type):
        if node.type == 'vars_list':
            for child in node.children:
                self._declaration(child, _type)
        else:
            try:
                self._create_new_var(node.type, node.value)
            except RedeclarationError:
                self._error(errors['redeclaration'], node)
        if node.type == 'assignment':
            # self._create_new_var(_type, node.value)
            variable = node.children[0]
            if node.children[1].type != 'array':
                expr = self._interpret_node(node.children[1])
                try:
                    self._assign(_type, variable, expr)
                except CastError:
                    self._error(errors['cast'], node)
                except ValueError:
                    self._error(errors['value'], node)
            else:
                nodearr = self._array(node.chilren[1])
                arr = [self._interpret_node(i) for i in nodearr]
                self._assign_array(_type, variable, arr)
                
    def _create_new_var(self, _type, name):
        if name in self.sym_table[self.scope].keys():
            raise RedeclarationError
        self.sym_table[self.scope][name] = Var(_type, None)
                
    def _assign(self, _type, variable, expr: Var):
        if variable not in self.sym_table[self.scope].keys():
            raise NameError
        if _type in [expr.type, 'var']:
            self.sym_table[self.scope][variable] = expr
        elif not isinstance(expr.value, list):
            casted_value = self.cast.cast(_type, expr)
            self.sym_table[self.scope][variable] = casted_value
        else:
            self._assign_array(_type, variable, expr)
    
    def _assign_array(_type, variable, arr):
        if _type != 'var':
            cast_arr = [self.cast.cast(_type, a) for a in arr]
            self.sym_table[self.scope][variable] = cast_arr
        else:
            prob_type = arr[0].type
            cast_arr = [self.cast.cast(prob_type, a) for a in arr]
            self.sym_table[self.scope][variable] = cast_arr
            
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
                    self._array_from_tree(child, ret)
            else:
                ret.append(node)
            
            
            
        
    def _error(self, err_type, node):
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
    
