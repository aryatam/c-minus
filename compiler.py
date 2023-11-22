import string
from enum import Enum
from typing import List, Optional, Set, Dict, Tuple


class State:
    def __init__(self, name: id):
        self.id = name
        self.listTransiton: List[Transition] = []
        self.isFinal = False
        self.isLookAhead = False
        self.hasTransition = False


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
    EOF = None
    all_chars: Set[str] = set(chr(i) for i in range(128))
    digits: Set[str] = set(string.digits)
    letters: Set[str] = set(string.ascii_letters)
    alphanumerics: Set[str] = digits.union(letters)
    symbols: Set[str] = {';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<', '=='}
    whitespaces: Set[str] = {' ', '\n', '\r', '\t', '\v', '\f'}
    valid_chars: Set[str] = alphanumerics.union(symbols, whitespaces)
    keywords = {"if", "else", "void", "int", "while", "break", "return"}

    def __init__(self):
        self.transitions: list[Transition] = []
        self.state: list[State] = []

    def createStates(self):
        self.state = []
        for i in range(19):
            self.state.append(State(i))

    def generateTransitons(self):
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[1], list(self.digits)))
        self.state[1].listTransiton.append(Transition(self.state[1], self.state[1], list(self.digits)))
        self.state[1].isFinal = True

    def createTransitons(self):
        pass


class Compiler:

    def __init__(self):
        scanner = Scanner()


if __name__ == '__main__':
    compiler = Compiler()
