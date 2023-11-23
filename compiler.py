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
    end: Set[str] = symbols.union(whitespaces, {EOF})

    def __init__(self):
        self.symbol_table = {}
        self.transitions: list[Transition] = []
        self.state: list[State] = []
        self.tokens: list[str] = []
        self.inputCode = open("input.txt", mode="r")
        self.file_contents = ""
        self.file_contents = self.inputCode.read()

        self.pointer = 0
        self.line = 1
        self.errors_dict: Dict[int, List[Error]] = {}

    def addSymbol(self):


    def nextChar(self):
        if self.pointer >= len(self.file_contents):
            return None
        else:
            char = self.file_contents[self.pointer]
            self.pointer = self.pointer + 1
            return char

    def symbolTable(self):
        self.symbol_table: Dict[str, List[Optional]] = {}
        for keyword in Scanner.keywords:
            self.symbol_table[keyword] = [len(self.symbol_table) + 1]

    def createStates(self):
        self.state = []
        for i in range(19):
            self.state.append(State(i))

    def generateTransitons(self):
        # start state 0 Start
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[1], list(self.digits)))
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[2], list(self.letters)))
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[3],
                                                      list(self.symbols - {'/', '=', '*'})))
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[4], list('=')))
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[5], list('/')))
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[6], list(self.whitespaces)))
        self.state[0].listTransiton.append(Transition(self.state[0], self.state[7], list('*')))

        # state 1 NUM
        self.state[1].listTransiton.append(Transition(self.state[1], self.state[1], list(self.digits)))
        self.state[1].listTransiton.append(Transition(self.state[1], self.state[8], list(self.end)))

        # state 2 ID
        self.state[2].listTransiton.append(Transition(self.state[2], self.state[2], list(self.alphanumerics)))
        self.state[2].listTransiton.append(Transition(self.state[2], self.state[9], list(self.end)))

        # state 3 symbol - lookahead

        # state 4 = , ==
        self.state[4].listTransiton.append(Transition(self.state[4], self.state[10], list('=')))
        self.state[4].listTransiton.append(Transition(self.state[4], self.state[11],
                                                      list(self.valid_chars.union(self.EOF - '='))))
        # state 5 / /* //
        self.state[5].listTransiton.append(Transition(self.state[5], self.state[12],
                                                      list(self.valid_chars.union(self.EOF - '*', '/'))))
        self.state[5].listTransiton.append(Transition(self.state[5], self.state[13], list('/')))
        self.state[5].listTransiton.append(Transition(self.state[5], self.state[14], list('*')))

        # state 13 //
        self.state[13].listTransiton.append(Transition(self.state[13], self.state[13], list(self.all_chars - '\n')))
        self.state[13].listTransiton.append(Transition(self.state[13], self.state[15], list("/n" + self.EOF)))

        # state 14 /*
        self.state[14].listTransiton.append(Transition(self.state[14], self.state[14], list(self.all_chars - '*')))
        self.state[14].listTransiton.append(Transition(self.state[14], self.state[16], list('*')))

        # state 16 */
        self.state[16].listTransiton.append(Transition(self.state[16], self.state[17], list('/')))
        self.state[16].listTransiton.append(Transition(self.state[14], self.state[16], list(self.all_chars - '/')))

        # state 7 * the only problem is /* without /*
        self.state[7].listTransiton.append(Transition(self.state[7], self.state[18], list(self.all_chars - '/')))

    def setFinal_lookahead(self):
        # final stages of DFA

        self.state[6].isFinal = True
        self.state[8].isFinal = True
        self.state[9].isFinal = True
        self.state[3].isFinal = True
        self.state[11].isFinal = True
        self.state[10].isFinal = True
        self.state[12].isFinal = True
        self.state[15].isFinal = True
        self.state[17].isFinal = True
        self.state[18].isFinal = True

        # read the input but don't use it its look ahead
        self.state[8].isLookAhead = True
        self.state[9].isLookAhead = True
        self.state[11].isLookAhead = True
        self.state[12].isLookAhead = True
        self.state[15].isLookAhead = True
        self.state[18].isLookAhead = True

    def initialize_symbol_table(self):
        pass


class Compiler:
    # we run the compiler to give us token by token, and we write it on token file
    def execute(self):
        pass

    def __init__(self):
        self.scanner = Scanner()


if __name__ == '__main__':
    compiler = Compiler()
    compiler.execute()
