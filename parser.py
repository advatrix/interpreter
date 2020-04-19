#! /usr/bin/env python

from __future__ import annotations
import ply.yacc as yacc
from lexer import Lexer
from ply.lex import LexError
import sys
from typing import List, Dict


class SyntaxTreeNode():  # возможно эффективнее будет хранить типы узлов в статических полях-числах
    def __init__(self, type_='const', value=None, children: Optional[List[SyntaxTreeNode]] = None):
        self.type = type_
        self.value = value
        self.children = children
        self.acc = None
        
    def __repr__(self):
        return f'''{self.type} {self.value}'''
    
    def print(self, level: int = 0):
        print(' '*level, ' ', self)
        if self.children is not None:
            if isinstance(self.children, SyntaxTreeNode):
                self.children.print(level + 1)
            elif isinstance(self.children, str):
                print(' ' * (level + 1), self.children)
            elif isinstance(self.children, list):
                for i in range(len(self.children)):
                    if isinstance(self.children[i], str):
                        print(' ' * (level + 1), self.children[i])
                    else:    
                        self.children[i].print(level + 1)
            elif isinstance(self.children, dict):
                for key, value in self.children.items():
                    print(' '*(level + 1), key)
                    if isinstance(value, str):
                        print(' '*(level + 2), value)
                    elif isinstance(value, SyntaxTreeNode):
                        value.print(level + 2)


class Parser():
    tokens = Lexer.tokens
    
    
    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
        self._functions: Dict[str, SyntaxTreeNode] = dict()
        
    def parse(self, s) -> List:
        try:
            res = self.parser.parse(s)
            return res, self._functions
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n', s)
            
    def check_program(self, prog: str) -> bool:
        self.acc = True
        self.parser.parse(prog)
        return self.acc            
            
    def p_program(self, p):
        'program : stmt_list'
        p[0] = SyntaxTreeNode('program', children=p[1])
        
    def p_empty(self, p):
        'empty : '
        pass
        
    def p_stmt_list(self, p):
        '''stmt_list : stmt_list statement
        | statement'''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('stmt_list', children=p[1])
        else:
            p[0] = SyntaxTreeNode('stmt_list', children=[p[1], p[2]])
        
    def p_statement(self, p):
        '''statement : declaration_list NL
        | assignment NL
        | while NL
        | if NL
        | operator NL
        | function NL
        | function_call NL
        | RETURN NL
        | empty NL
        '''
        p[0] = p[1]
        
    def p_declaration_list(self, p):
        'declaration_list : type vars_list'
        p[0] = SyntaxTreeNode('declaration_list', value=p[1], children=p[2])
        
    def p_type(self, p):
        '''type : INT
        | CELL
        | BOOL
        | VAR
        '''
        p[0] = p[1]
        
    def p_vars_list(self, p):
        '''vars_list : IDENT COMMA vars_list
        | assignment COMMA vars_list
        | IDENT
        | assignment'''
        if len(p) == 4:
            p[0] = SyntaxTreeNode('vars_list', children=[p[1], p[3]])
        else:
            p[0] = SyntaxTreeNode('vars_list', children=p[1])
        
    def p_assignment(self, p):
        '''assignment : variable ASSIGN expression'''
        p[0] = SyntaxTreeNode('assignment', children=[p[1], p[3]])
        
    def p_variable(self, p):
        '''variable : IDENT OBRACKET expression CBRACKET
        | IDENT'''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('variable', p[1])
        else:
            p[0] = SyntaxTreeNode('indexing', p[1], children=p[3])
        
    def p_expression(self, p): # al_expression stands for Arithmetical-Logical
        '''expression : variable
        | const
        | al_expression
        | function_call
        | operator'''
        p[0] = p[1]
        
    def p_const(self, p):
        '''const : INF
        | MINUS_INF
        | NAN
        | TRUE
        | FALSE
        | UNDEF
        | EMPTY
        | WALL
        | BOX
        | EXIT
        | DECIMAL
        | HEXADECIMAL'''
        p[0] = SyntaxTreeNode('const', value=p[1])
        
    def p_al_expression(self, p):
        '''al_expression : expression PLUS expression
        | expression MINUS expression
        | MINUS expression
        | SHARP expression
        | expression CARET expression
        | expression GREATER expression
        | expression LESS expression
        | expression EQUAL expression'''
        if len(p) == 3:
            p[0] = SyntaxTreeNode('un_op', p[1], children=p[2])
        else:
            p[0] = SyntaxTreeNode('bin_op', p[2], children=[p[1], p[3]])
        
    def p_function_call(self, p):
        'function_call : IDENT OBRACKET variable CBRACKET'
        p[0] = SyntaxTreeNode('function_call', p[1], children=p[3])
        
    def p_operator(self, p):
        '''operator : FORWARD expression
        | BACKWARD expression
        | LEFT
        | RIGHT
        | LOAD expression
        | DROP expression
        | LOOK
        | TEST'''
        if len(p) == 2:
            p[0] = SyntaxTreeNode('operator', p[1])
        else:
            p[0] = SyntaxTreeNode('operator', p[1], children=p[2])
        
    def p_while(self, p):
        '''while : WHILE expression DO stmt_list DONE
        | WHILE expression DO stmt_list FINISH stmt_list DONE'''
        if len(p) == 6:
            p[0] = SyntaxTreeNode('while', children=[p[2], p[4]])
        else:
            p[0] = SyntaxTreeNode('while', children=[p[2], p[4], p[6]])
        
    def p_if(self, p):
        '''if : IF expression DO stmt_list DONE 
        | IF expression DO stmt_list DONE NL ELDEF DO stmt_list DONE
        | IF expression DO stmt_list DONE NL ELDEF DO stmt_list DONE NL ELUND DO stmt_list DONE
        | IF expression DO stmt_list DONE NL ELUND DO stmt_list DONE'''
        if len(p) == 6:
            p[0] = SyntaxTreeNode('if', children={'condition': p[2], 'body': p[4], 'eldef': None, 'elund': None})
        elif len(p) == 11:
            if p[7].lower() == 'eldef':
                p[0] = SyntaxTreeNode('if', children={'condition': p[2], 'body': p[4], 'eldef': p[9], 'elund': None})
            else:
                p[0] = SyntaxTreeNode('if', children={'condition': p[2], 'body': p[4], 'eldef': None, 'elund': p[9]})
        else:
            p[0] = SyntaxTreeNode('if', children={'condition': p[2], 'body': p[4], 'eldef': p[9], 'elund': p[14]})
                                  
        
    def p_function(self, p):
        '''function : FUNCTION OBRACKET IDENT CBRACKET DO stmt_list DONE 
        | FUNCTION IDENT OBRACKET IDENT CBRACKET DO NL stmt_list DONE'''
        if len(p) == 8:
            p[0] = SyntaxTreeNode('unnamed_function', children={'param': p[3], 'body': p[6]})
        else:
            self._functions[p[2]] = SyntaxTreeNode('function', children={'param': p[4], 'body': p[8]})
            p[0] = SyntaxTreeNode('function_description', value=p[2])
            
            
    def p_error(self, p):
        print(f'Syntax error at {p}')
        self.acc = False
        
        

        
        
if __name__ == '__main__':
    parser = Parser()
    txt = sys.stdin.read()
    print(f'INPUT: {txt}')
    tree, func_table = parser.parse(txt)
    # tree = parser.parser.parse(txt, debug=True)
    tree.print()
    # print(funcs)

        
    