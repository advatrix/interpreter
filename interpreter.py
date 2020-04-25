#! /usr/bin/env python


# TODO: scopes
# map description
# robot loading

from __future__ import annotations
import sys
import parser
from typing import List

class Robot:
    def __init__(self, x, y, z, rot, capacity, slots_num, map_):
    ''' Rotation:
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
       
       
    '''
        self.x = x
        self.y = y
        self.z = z
        self.rot = rot
        self.capacity = capacity
        self.slots = [None for _ in range(slots_num)]
        self.map = map_
        
    def __repr__(self):
        return f'''({self.x}, {self.y}, {self.z}):{self.rot}
Slots: {self.slots}
Capacity: {self.sum()}/{self.capacity}'''
        
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
        raise NotImplementedError
        
    def left(self):
        raise NotImplementedError
    
    def right(self):
        raise NotImplementedError
        
    def load(self, expr):
        raise NotImplementedError
        
    def drop(self, expr):
        raise NotImplementedError
        
    def look(self):
        raise NotImplementedError
        
    def test(self):
        raise NotImplementedError
                
                
                        
                
            



class Var:
    def __init__(self, symtype, symvalue):
        self.type = symtype
        self.value = symvalue
        
    def __repr__(self):
        return f'{self.type}, {self.value}'
    

class InterpreterNameError(Exception):
    pass


class RedeclarationError(Exception):
    pass


class CastError(Exception):
    pass





class Cell:
    def __init__(self, x, y, z, type_):
        self.x = x
        self.y = y
        self.z = z
        self.type = type_
        
    def __repr__(self):
        return f'{self.x} {self.y} {self.z} : {self.type_}

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
    errors  = {
        'no_main': 1,
        'redeclaration': 2,
        'undeclared': 3,
        'index_error': 4,
        'unknown_func': 5,
        'cast': 6,
        'value': 7
              }
    
    
    
    def __init__(self, parser, caster=CastManager()):
        self.parser = parser
        self.cast = caster
        
    def interpret(self, map_description, program):
        self.map = map_description
        self.program = program
        self.sym_table = dict()
        self.scope = None
        self.display = []
        self.robot: Robot = None #implement it
        try:
            self.tree, self.funcs = self.parser.parse(program)
        except
        if 'main' not in funcs.keys():
            self._error(errors['no_main'])
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
                self.interpret_node(child)
        elif node.type == 'declaration_list':
            vars_type = node.value
            children = node.children.children
            if isinstance(children, list):
                for child in children:
                    self._declaration(child, vars_type)
            else:
                self._declaration(children, vars_type)
        elif node.type == 'variable':
            return node.value
        elif node.type == 'indexing':
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
            if node.value not in self.funcs:
                self._error(errors['unknown_func'], node)
                return
            self.scope = node.value
            return self._interpret_node(self.funcs[node.value])
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
        elif node.type == 'while':
            self._while(node)
        elif node.type == 'if':
            self._if(node)
        elif node.type == 'unnamed_function':
            return self._unnamed_function(node)
        elif node.type == 'function_description':
            pass
        
    def _while(self, node):
        raise NotImplementedError
        
    def _if(self, node):
        raise NotImplementedError
        
    def _unnamed_function(self, node):
        raise NotImplementedError
        
    def _sizeof(self, node):
        expr = self._interpret_node(node)
        if expr not in self.sym_table.keys():
            self._error(errors['value'], node)
            return
        if isinstance(self.sym_table[expr].value, list):
            return Var('int', len(self.sym_table[expr].value))
        else:
            return Var('int', 1)
        
        
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
    
    def _negative(self, node):
        expr = self._interpret_node(node)
        return (-1) * self.cast.cast('int', expr)
    
    def _sum(self, node):
        expr = self._interpret_node(node)
        if isinstance(expr, list):
            return sum[self.cast.cast('int', a) for a in expr]
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
        if name in self.symtable.keys():
            raise RedeclarationError
        self.symtable[name] = Var(_type, None)
                
    def _assign(self, _type, variable, expr: Var):
        if variable not in self.sym_table.keys():
            raise InterpreterNameError
        if _type in [expr.type, 'var']:
            self.sym_table[variable] = expr
        elif not isinstance(expr.value, list):
            casted_value = self.cast.cast(_type, expr)
            self.sym_table[variable] = casted_value
        else:
            self._assign_array(_type, variable, expr)
    
    def _assign_array(_type, variable, arr):
        if _type != 'var':
            cast_arr = [self.cast.cast(_type, a) for a in arr if a.type != _type else a]
            self.sym_table[variable] = cast_arr
        else:
            prob_type = arr[0].type
            cast_arr = [self.cast.cast(prob_type, a) for a in arr]
            self.sym_table[variable] = cast_arr
            
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
    
