#! /usr/bin/env python

from __future__ import annotations
import sys
from typing import List, Dict
import ply.yacc as yacc
from lexer import Lexer
from ply.lex import LexError

class SyntaxTreeNode():  # возможно эффективнее будет хранить типы узлов в статических полях-числах
    def __init__(self, type_='const', value=None, children: Optional[List[SyntaxTreeNode]] = None):
        self.type = type_
        self.value = value
        self.children = children
        



class Parser():
    tokens = Lexer.tokens
    
    def __init__(self):
        self.lexer = Lexer()
        self.parser = yacc.yacc(module=self)
        self._functions: Dict[str, SyntaxTreeNode] = dict()
        
    def check_string(self, s) -> List:
        try:
            res = self.parser.parse(s)
            return res
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n', s)
            
            
    def p_program(self, p):
        'program : stmt_list'
        p[0] = p[1]
        
    def p_stmt_list(self, p):
        '''stmt_list : statement
        | statement NL stmt_list
        | NL'''
        if len(p) == 2:
            p[0] = [p[1]]
        else:
            p[0] = [p[1]] + p[3]
        
    def p_statement(self, p):
        '''statement : declaration
        | assignment
        | while
        | if
        | operator
        | function
        | function_call'''
        p[0] = p[1]
            
    def p_declaration(self, p):
        '''declaration : int_decl
        | bool_decl
        | cell_decl
        | var_decl'''
        p[0] = p[1]
        
    def p_int_decl(self, p):
        'int_decl : INT IDENT'
        p[0] = SyntaxTreeNode('int_decl', p[2])
        
    def p_bool_decl(self, p):
        'bool_decl : BOOL IDENT'
        p[0] = SyntaxTreeNode('bool_decl', p[2])
        
    def p_cell_decl(self, p):
        'cell_decl : CELL IDENT'
        p[0] = SyntaxTreeNode('cell_decl', p[2])
        
    def p_var_decl(self, p):
        'var_decl : VAR IDENT'
        p[0] = SyntaxTreeNode('var_decl', p[2])
        
    def p_assignment(self, p):
        '''assignment : variable ASSIGN expression
        | declaration ASSIGN expression'''
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
        | UNDEF
        | DECIMAL
        | HEXADECIMAL'''
        p[0] = p[1]
        
    def p_al_expression(self, p):
        '''al_expression : expression PLUS expression
        | expression MINUS expression
        | MINUS expression
        | SHARP expression
        | expression CARET expression
        | expression GREATER expression
        | expression LESS expression
        | expression EQUAL expression'''
        if len(p) == 2:
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
        | IF expression DO stmt_list DONE ELDEF DO stmt_list DONE
        | IF expression DO stmt_list DONE ELDEF DO stmt_list DONE ELUND DO stmt_list DONE
        | ID expression DO stmt_list DONE ELUND DO stmt_list DONE'''
        if len(p) == 6:
            p[0] = SyntaxTreeNode('if', children={'condition': p[2], 'body': p[4], 'eldef': None, 'elund': None})
        elif len(p) == 10:
            if p[6].lower() == 'eldef':
                p[0] = SyntaxTreeNode('if', children={'condition': p[2], 'body': p[4], 'eldef': p[8], 'elund': None})
            else:
                p[0] = SyntaxTreeNode('if', children={'condition': p[2], 'body': p[4], 'eldef': None, 'elund': p[8]})
        else:
            p[0] = SyntaxTreeNode('if', children-{'condition': p[2], 'body': p[4], 'eldef': p[8], 'elund': p[12]})
                                  
        
    def p_function(self, p):
        '''function : FUNCTION OBRACKET IDENT CBRACKET DO stmt_list RETURN stmt_list DONE 
        | FUNCTION IDENT OBRACKET IDENT CBRACKET DO stmt_list RETURN stmt_list DONE
        | FUNCTION OBRACKET IDENT CBRACKET DO stmt_list DONE
        | FUNCTION IDENT OBRACKET IDENT CBRACKET DO stmt_list DONE'''
        
        
        
        
        
    