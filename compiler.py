import string
from enum import Enum
from typing import List, Optional, Set, Dict, Tuple


class State:
    def __int__(self):
        pass


class Transition:
    def __init__(self):
        pass


class Error:

    def __init__(self):
        pass


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

    def __init__(self, buffer_size=1024):
        self._input_file = open("input.txt", mode="r")
        self._buffer_size = buffer_size
        self._buffer: List[Optional[str]] = []
        self._token_buffer: List[str] = []


class Compiler:

    def __init__(self):
        scanner = Scanner()


if __name__ == '__main__':
    compiler = Compiler()
