import pytest
from lexer import Lexer

lexer = Lexer()

def test_lorem_ipsum():
    lexer.input('lorem ipsum dolor sit amet')
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'IDENT'
    assert lexer.token() is None

    
def test_empty_string():
    lexer.input('')
    assert lexer.token() is None
    
    
def test_case_insensitivity():
    lexer.input('True fAlse vAR bOoL cElL FINISH box')
    assert lexer.token().type == 'TRUE'
    assert lexer.token().type == 'FALSE'
    assert lexer.token().type == 'VAR'
    assert lexer.token().type == 'BOOL'
    assert lexer.token().type == 'CELL'
    assert lexer.token().type == 'FINISH'
    assert lexer.token().type == 'BOX'
    assert lexer.token() is None
    

def test_lang_mistakes():
    lexer.input('inti iint don doner 4e e4 >> : :=')
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'IDENT'
    assert lexer.token().type == 'UNKNOWN'
    assert lexer.token() is None