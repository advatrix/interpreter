import ply.lex as lex
import re
import sys

# TODO: wrap every token by \s+

class Lexer():
    states = ()
    
    tokens = (
        'INF', 'MINUS_INF', 'NAN'
    
    )
    
    t_SPACE = r' '
    t_COMMA = r'\s*,\s*'
    
    t_INT = r'(?i)int'
    t_DECIMAL = r'[0-9]*'
    t_HEXADECIMAL = r'(?i)[A-F0-9]*h+'
    t_INF = r'(?i)inf'
    t_MINUS_INF = r'(?i)-inf'
    t_NAN = r'(?i)nan'
    
    t_BOOL = r'(?i)bool'
    t_TRUE = r'(?i)(t|true)'
    t_FALSE = r'(?i)(f|false)'
    t_UNDEF = r'(?i)(u|undef)'
    
    t_CELL = r'(?i)cell'
    t_EMPTY = r'(?i)empty'
    t_WALL = r'(?i)wall'
    t_BOX = r'(?i)box'
    t_EXIT = r'(?i)exit'
    
    t_VAR = r'(?i)var'
    
    t_OBRACKET = r'\('
    t_CBRACKET = r'\)'
    
    t_ASSIGN = r':='
    t_PLUS = r'\+'
    t_MINUS = r'\-'
    t_SHARP = r'#'
    t_XOR = r'^'
    t_LESS = r'<'
    t_GREATER = r'>'
    t_EQUAL = r'='
    
    t_WHILE = r'(?i)while'
    t_DO = r'(?)do'
    t_FINISH = r'(?)finish'
    t_DONE = r'(?)done'
    
    t_IF = r'(?)if'
    t_ELDEF = r'(?i)eldef'
    t_ELUND = r'(?i)elund'
    
    t_FORWARD = r'(?i)forward'
    t_BACKWARD = r'(?i)backward'
    
    t_LEFT = r'(?i)left'
    t_RIGHT = r'(?i)right'
    
    t_LOAD = r'(?i)load'
    t_DROP = r'(?i)drop'
    t_LOOK = r'(?i)look'
    t_TEST = r'(?i)test'
    
    t_FUNCTION = r'(?i)function'
    t_RETURN = r'(?i)return'
    
    
    
    
    
    
    def ___init__(self):
        self.lexer = lex.lex(module=self)
        
    def input(self, data):
        return self.lexer.input(data)
    
    
    