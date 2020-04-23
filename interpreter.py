# usr/bin/env python

from __future__ import annotations
import sys
import parser
from typing import List

class SymTableItem:
    def __init__(self, symtype, symvalue):
        self.type = symtype
        self.value = symvalue
        
    def __repr__(self):
        return f'{self.type}, {self.value}'


class Interpreter:
    errors  = {
        'no_main': 1,
        'redeclaration': 2,
        'undeclared': 3,
        'index_error': 4,
        'unknown_func': 5
              }
    
    
    def __init__(self, parser):
        self.parser = parser
        
    def interpret(self, map_description, program):
        self.map = map_description
        self.program = program
        self.sym_table = dict()
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
            return node.value
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
            return self._interpret_node(self.funcs[node.value])
        elif node.type == 'operator':
            if node.value.lower() == 'forward':
                return self._forward(self._interpret_node(node.children))
            elif node.value.lower() == 'backward':
                return self._backward(self._interpret_node(node.childen))
            elif node.value.lower() == 'left':
                self._left()
            elif node.value.lower() == 'right':
                self.right()
            elif node.value.lower() == 'load':
                return self._load(self._interpret_node(node.children))
            elif node.value.lower() == 'drop':
                return self._drop(self._interpret_node(node.children))
            elif node.value.lower() == 'look':
                return self._look()
            elif node.value.lower() == 'test':
                return self._test()
            elif node.value.lower() == 'sizeof':
                return self._sizeof(self._interpret_node(node.children))
        elif node.type == 'while':
            self._while(node)
        elif node.type == 'if':
            self._if(node)
        elif node.type == 'unnamed_function':
            return self._unnamed_function(node)
        elif node.type == 'function_description':
            pass
        
                                
    def _declaration(self, node, _type):
        if node.type == 'vars_list':
            for child in node.children:
                self._declaration(child, _type)
        elif node.type == 'ident':
            if node.value in self.sym_table.keys():
                self._error(errors['redeclaration'], node)
            else:
                self.sym_table[node.value] = SymTableItem(type, None)
        elif node.type == 'assignment':
            variable = node.children[0]
            if node.children[1].type != 'array':
                expr = self._interpret_node(node.children[1])
                self._assign(_type, variable, expr)
            else:
                arr = self._array(node.chilren[1])
                self._assign(_type, variable, arr)
                
    def _assign(self, _type, variable, expr: SymTableItem):
        # TODO: приведение типов
        if _type == expr.type:

        
    def _error(self, err_type, node):
        sys.stderr.write(f'Error {err_type}: ')
        if err_type == 1:
            sys.stderr.write(f'no main function\n')
            return
        elif err_type == 2:
            sys.stderr.write(f'variable "{node.value}" at {node.lineno}:{node.lexpos} is already declared\n')
        elif err_type == 3:
            sys.stderr.write(f'variable "{node.value}" at {node.lineno}:{node.lexpos} is used before declaration\n')
        elif err_type == 4:
            sys.stderr.write(f'index error "{node.value}" at {node.lineno}:{node.lexpos}\n')
        elif err_type == 5:
            sys.stderr.write(f'Unknown function call "{node.value}" at {node.lineno}:{node.lexpos}\n')
    
