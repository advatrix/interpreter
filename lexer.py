#! /usr/bin/env python

import ply.lex as lex
import re
import sys


class Lexer():
    states = (
    )
    
    tokens = (
        'COMMA', 'INT', 'DECIMAL', 'HEXADECIMAL',
        'INF', 'MINUS_INF', 'NAN', 'BOOL', 'TRUE', 'FALSE', 
        'UNDEF', 'CELL', 'EMPTY', 'WALL', 'BOX', 'EXIT', 'VAR',
        'OBRACKET', 'CBRACKET', 'ASSIGN', 'PLUS', 'MINUS', 'SHARP',
        'CARET', 'LESS', 'GREATER', 'EQUAL', 'WHILE', 'DO', 'FINISH',
        'DONE', 'IF', 'ELDEF', 'ELUND', 'FORWARD', 'BACKWARD',
        'LEFT', 'RIGHT', 'LOAD', 'DROP', 'LOOK', 'TEST', 
        'FUNCTION', 'RETURN', 'IDENT', 'NL', 'OSQBRACKET', 'CSQBRACKET', 'SIZEOF'
    )
    
    t_ignore = ' \t'
    
    def __init__(self):
        self.lexer = lex.lex(module=self)
    
      
    def input(self, data):
        return self.lexer.input(data)
    
    def t_COMMA(self, t):
        r'\,'
        return t
    
    def t_DECIMAL(self, t):
        r'[0-9]+(?!\w)'
        return t
    
    def t_HEXADECIMAL(self, t):
        r'[A-F0-9]*h(?!\w)'
        return t
    
    def t_SIZEOF(self, t):
        r'sizeof(?!\w)'
        return t
    
    def t_INF(self, t):
        r'inf(?!\w)'
        return t
    
    def t_MINUS_INF(self, t):
        r'-inf(?!\w)'
        return t
    
    def t_NAN(self, t):
        r'nan(?!\w)'
        return t
    
    def t_BOOL(self, t):
        r'bool(?!\w)'
        return t
    
    def t_FUNCTION(self, t):
        r'function(?!\w)'
        return t
    
    def t_FINISH(self, t):
        r'finish(?!\w)'
        return t
    
    def t_TRUE(self, t):
        r'(true|t)(?!\w)'
        return t
    
    def t_FALSE(self, t):
        r'(false|f)(?!\w)'
        return t
    
    def t_UNDEF(self, t):
        r'(undef|u)(?!\w)'
        return t
    
    def t_CELL(self, t):
        r'cell(?!\w)'
        return t
    
    def t_EMPTY(self, t):
        r'empty(?!\w)'
        return t
    
    def t_WALL(self, t):
        r'wall(?!\w)'
        return t
    
    def t_BOX(self, t):
        r'box(?!\w)'
        return t
    
    def t_EXIT(self, t):
        r'exit(?!\w)'
        return t
    
    def t_VAR(self, t):
        r'var(?!\w)'
        return t
    
    def t_OBRACKET(self, t):
        r'\('
        return t
    
    def t_CBRACKET(self, t):
        r'\)'
        return t
    
    def t_OSQBRACKET(self, t):
        r'\['
        return t
    
    def t_CSQBRACKET(self, t):
        r'\]'
        return t
    
    def t_ASSIGN(self, t):
        r':='
        return t
    
    def t_PLUS(self, t):
        r'\+'
        return t
    
    def t_MINUS(self, t):
        r'\-'
        return t
    
    def t_SHARP(self, t):
        r'\#'
        return t
    
    def t_CARET(self, t):
        r'\^'
        return t
    
    def t_LESS(self, t):
        r'\<'
        return t
    
    def t_GREATER(self, t):
        r'\>'
        return t
    
    def t_EQUAL(self, t):
        r'\='
        return t
    
    def t_WHILE(self, t):
        r'while(?!\w)'
        return t
    
    def t_DONE(self, t):
        r'done(?!\w)'
        return t
    
    def t_DO(self, t):
        r'do(?!\w)'
        return t
    
    def t_IF(self, t):
        r'if(?!\w)'
        return t
    
    def t_ELDEF(self, t):
        r'eldef(?!\w)'
        return t
    
    def t_ELUND(self, t):
        r'elund(?!\w)'
        return t
    
    def t_FORWARD(self, t):
        r'forward(?!\w)'
        return t
    
    def t_BACKWARD(self, t):
        r'backward(?!\w)'
        return t
    
    def t_LEFT(self, t):
        r'left(?!\w)'
        return t
    
    def t_RIGHT(self, t):
        r'right(?!\w)'
        return t
    
    def t_LOAD(self, t):
        r'load(?!\w)'
        return t
    
    def t_DROP(self, t):
        r'drop(?!\w)'
        return t
    
    def t_LOOK(self, t):
        r'look(?!\w)'
        return t
    
    def t_TEST(self, t):
        r'test(?!\w)'
        return t
    
    def t_RETURN(self, t):
        r'return(?!\w)'
        return t
    
    def t_INT(self, t):
        r'int(?!\w)'
        return t      
    
    def t_IDENT(self, t):
        r'[a-z_][a-z0-9_]*'
        return t
         
    def t_NL(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        return t
    
    def t_error(self, t):
        sys.stderr.write(f'Illegal character: "{t.value}" at line {t.lexer.lineno}\n')
        t.lexer.skip(len(t.value))
        t.lexer.begin('INITIAL')
        
    
    def token(self):
        return self.lexer.token()
    

if __name__ == '__main__':
    lexer = Lexer()
    try:
        while True:
            lexer.input(input())
            for tok in lexer.lexer:
                print(tok)
    except EOFError:
        pass
