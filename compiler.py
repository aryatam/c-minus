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
        self.end = state2
        self.start = state1
        self.moveWith: list[str] = move


class Error:

    def __init__(self, title: str, content: Optional[str], line: int):
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

        self.symbol_table: Dict[str, List[Optional]] = {}
        for keyword in Scanner.keywords:
            self.symbol_table[keyword] = [len(self.symbol_table) + 1]

        self.transitions: list[Transition] = []
        self.state: list[State] = []
        self.current_state: State = None
        self.matchStrings: list[str] = []
        self.inputCode = open("input.txt", mode="r")
        self.file_contents = ""
        self.file_contents = self.inputCode.read()
        self.end_of_file = False
        self.current_char: Optional[str] = None  # End of file = None
        self.pointer = 0
        self.line = 1
        self.errors_dict: Dict[int, List[Error]] = {}

    def createToken(self) -> [Tuple[str, str]]:
        if self.current_state == 8:
            return "NUM", self.matchStrings
        elif self.current_state == 6:
            return None, self.matchStrings
        elif self.current_state == 9:
            if self.matchStrings in self.keywords:
                return "KEYWORD", self.matchStrings
            else:
                return "ID", self.matchStrings
        elif self.current_state == 3:
            return "SYMBOL", self.matchStrings
        elif self.current_state == 10:
            return "SYMBOL", self.matchStrings
        elif self.current_state == 11:
            return "SYMBOL", self.matchStrings
        elif self.current_state == 12:
            return "SYMBOL", self.matchStrings
        elif self.current_state == 15:
            return None, self.matchStrings
        elif self.current_state == 17:
            return "COMMENT", self.matchStrings
        elif self.current_state == 18:
            return "KEYWORD", self.matchStrings

    def get_next_token(self) -> Optional[Tuple[str, str]]:
        if self.end_of_file:
            return None
        else:
            self.matchStrings.clear()
            self.current_state = self.state[0]
        while True:
            if self.current_state.isFinal:
                if self.current_state.isLookAhead:
                    self.pointer = self.pointer - 1
                    self.matchStrings = self.matchStrings[0:self.pointer]
                if self.current_char == '\n':
                    self.line = self.line - 1
                token = self.createToken
                if token[0] is None:
                    self.matchStrings.clear()
                    self.current_state = self.state[0]

                else:
                    return token


            else:
                self.current_char = self.file_contents[self.pointer]

                if self.current_char == '\n':
                    self.line = self.line + 1

                if self.end_of_file:
                    self.current_char = None

                if self.end_of_file and self.current_state == 0:
                    return None

                self.matchStrings.append(self.current_char)

                for transiton in self.current_state.listTransiton:
                    # list transiton is based on prority
                    if self.current_char in transiton.moveWith:
                        self.current_state = transiton.end
                        break

                else:



    def error_handler(self, error_type: int):
        if error_type == 1:
            if self.current_state.id == 7 and self.current_char == '/':
                error = Error("Unmatched comment", None, self.line)

            elif self.current_state.id == 1 and self.current_char in self.letters:
                error = Error("Invalid number", None, self.line)

            else:
                error = Error("Invalid input", None, self.line)
        elif error_type == 2:
            if self.current_state.id == 14 or self.current_state.id == 16:
                # problem is we should give the line that we saw /* So
                self.line = self.line - self.matchStrings.count('\n')
                error = Error("Unclosed comment", self.matchStrings[0:6] + "...", self.line)

    def addSymbol(self):
        pass

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
