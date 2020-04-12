#! /usr/bin/env python

import sys
import ply.yacc as yacc
from lexer import Lexer
from ply.lex import LexError

class Parser():
    tokens = Lexer.tokens
    
    def __init__(self):
        self._lexer = Lexer()
        self._parser = yacc.yacc(module=self)
        
    def check_string(self, s):
        try:
            res = self._parser.parse(s)
            return res
        except LexError:
            sys.stderr.write(f'Illegal token {s}\n')
            
    def p_declaration(self, p):
        '''declaration: int_decl
        | bool_decl
        | cell_decl
        | var_decl'''
        p[0] = p[1]
        
    def int_decl(self, p):
        'int_decl: INT IDENT'
        p[0] = 