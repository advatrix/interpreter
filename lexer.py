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
        'FUNCTION', 'RETURN', 'IDENT', 'NL'
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
        r'(?i)[A-F0-9]*h+(?!\w)'
        return t
    
    def t_INF(self, t):
        r'(?i)inf(?!\w)'
        return t
    
    def t_MINUS_INF(self, t):
        r'(?i)-inf(?!\w)'
        return t
    
    def t_NAN(self, t):
        r'(?i)nan(?!\w)'
        return t
    
    def t_BOOL(self, t):
        r'(?i)bool(?!\w)'
        return t
    
    def t_FUNCTION(self, t):
        r'(?i)function(?!\w)'
        return t
    
    def t_FINISH(self, t):
        r'(?i)finish(?!\w)'
        return t
    
    def t_TRUE(self, t):
        r'(?i)(true|t)(?!\w)'
        return t
    
    def t_FALSE(self, t):
        r'(?i)(false|f)(?!\w)'
        return t
    
    def t_UNDEF(self, t):
        r'(?i)(undef|u)(?!\w)'
        return t
    
    def t_CELL(self, t):
        r'(?i)cell(?!\w)'
        return t
    
    def t_EMPTY(self, t):
        r'(?i)empty(?!\w)'
        return t
    
    def t_WALL(self, t):
        r'(?i)wall(?!\w)'
        return t
    
    def t_BOX(self, t):
        r'(?i)box(?!\w)'
        return t
    
    def t_EXIT(self, t):
        r'(?i)exit(?!\w)'
        return t
    
    def t_VAR(self, t):
        r'(?i)var(?!\w)'
        return t
    
    def t_OBRACKET(self, t):
        r'\('
        return t
    
    def t_CBRACKET(self, t):
        r'\)'
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
        r'(?i)while(?!\w)'
        return t
    
    def t_DONE(self, t):
        r'(?i)done(?!\w)'
        return t
    
    def t_DO(self, t):
        r'(?i)do(?!\w)'
        return t
    
    def t_IF(self, t):
        r'(?i)if(?!\w)'
        return t
    
    def t_ELDEF(self, t):
        r'(?i)eldef(?!\w)'
        return t
    
    def t_ELUND(self, t):
        r'(?i)elund(?!\w)'
        return t
    
    def t_FORWARD(self, t):
        r'(?i)forward(?!\w)'
        return t
    
    def t_BACKWARD(self, t):
        r'(?i)backward(?!\w)'
        return t
    
    def t_LEFT(self, t):
        r'(?i)left(?!\w)'
        return t
    
    def t_RIGHT(self, t):
        r'(?i)right(?!\w)'
        return t
    
    def t_LOAD(self, t):
        r'(?i)load(?!\w)'
        return t
    
    def t_DROP(self, t):
        r'(?i)drop(?!\w)'
        return t
    
    def t_LOOK(self, t):
        r'(?i)look(?!\w)'
        return t
    
    def t_TEST(self, t):
        r'(?i)test(?!\w)'
        return t
    
    def t_RETURN(self, t):
        r'(?i)return(?!\w)'
        return t
    
    def t_INT(self, t):
        r'(?i)int(?!\w)'
        return t      
    
    def t_IDENT(self, t):
        r'(?i)[a-z_][a-z0-9_]*'
        return t
         
    def t_NL(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count('\n')
        return t
    
    def t_error(self, t):
        sys.stderr.write(f'Illegal character: {t.value[0]} at line {t.lexer.lineno}\n')
        t.lexer.skip(1)
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

    
    
    