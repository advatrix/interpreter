import pytest
import sys
from parser import Parser

parser = Parser()

def test_good():
    with open('test_parser_good.txt', 'r') as f:
        assert parser.check_program(f.read())


def test_bad():
    with open('test_parser_bad.txt', 'r') as f:
        assert not parser.check_program(f.read())
