import string
from enum import Enum
from typing import List, Optional, Set, Dict, Tuple


class State:
    def __int__(self, name: int):
        self.id = name
        self.listTransiton: List[Transition] = []
        self.isFinal = False
        self.isLookAhead = False


class Transition:
    def __init__(self, state1: State, state2: State, move: list[str]):
        self.start = state1
        self.end = state2
        self.moveWith: list[str] = move


class Error:
    def __init__(self, TYPE: Enum, title: str, content: str, line: int):
        self.TYPE = TYPE
        self.title = title
        self.line = line
        self.content = content


class Scanner:
    # states
    _EOF = None
    _all_chars: Set[str] = set(chr(i) for i in range(128))
    _digits: Set[str] = set(string.digits)
    _letters: Set[str] = set(string.ascii_letters)
    _alphanumerics: Set[str] = _digits.union(_letters)
    _symbols: Set[str] = {';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<'}
    _whitespaces: Set[str] = {' ', '\n', '\r', '\t', '\v', '\f'}
    _valid_chars: Set[str] = _alphanumerics.union(_symbols, _whitespaces)
    _keywords = {"if", "else", "void", "int", "while", "break", "switch", "default", "case", "return", "endif"}
    # symbol table keywords
    NUM: str = "NUM"
    ID: str = "ID"
    KEYWORD: str = "KEYWORD"
    SYMBOL: str = "SYMBOL"
    COMMENT: str = "COMMENT"
    WHITESPACE: str = "WHITESPACE"

    def __init__(self):
        pass


class Compiler:

    def __init__(self):
        scanner = Scanner()


if __name__ == '__main__':
    compiler = Compiler()
