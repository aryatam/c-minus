import json
import string
from typing import List, Optional, Set, Dict, Tuple, Union
from anytree import Node, RenderTree
import grammer


class State:
    def __init__(self, name: id):
        self.id = name
        self.listTransiton: List[Transition] = []
        self.isFinal = False
        self.isLookAhead = False
        self.hasTransition = False


class Transition:
    def __init__(self, state1: State, state2: State, move: Set[str]):
        self.start = state1
        self.end = state2
        self.moveWith: Set[str] = move


class Error:

    def __init__(self, title: str, content: Optional[str], line: int):
        self.title = title
        self.line = line
        self.content = content


class Scanner:
    # states
    EOF = "None"
    all_chars: Set[str] = set(chr(i) for i in range(128))
    digits: Set[str] = set(string.digits)
    letters: Set[str] = set(string.ascii_letters)
    symbols: Set[str] = {';', ':', ',', '[', ']', '(', ')', '{', '}', '+', '-', '*', '/', '=', '<', '=='}
    whitespaces: Set[str] = {' ', '\n', '\r', '\t', '\v', '\f'}
    valid_chars: Set[str] = digits.union(letters, symbols, whitespaces)
    keywords = {"if", "else", "void", "int", "while", "break", "return"}
    end: Set[str] = symbols.union(whitespaces, {EOF})
    alphanumerics: Set[str] = digits.union(letters)
    for keyword in keywords:
        valid_chars.update(keyword)

    def __init__(self):
        self.symbol_table: Dict[str, List[Optional]] = {}

        for keyword in Scanner.keywords:
            self.symbol_table[keyword] = [len(self.symbol_table) + 1]

        self.transitions: list[Transition] = []
        self.state: list[State] = []
        self.current_state: State = None
        self.matchStrings: list[str] = []
        self.inputCode = open("input.txt", mode="r", encoding="utf-8")
        self.file_contents = ""
        self.file_contents = self.inputCode.read()
        self.end_of_file = False

        self.current_char: Optional[str] = 'None'  # End of file = None
        self.pointer = 0
        self.line = 1

        self.errors_dict: Dict[int, List[Error]] = {}
        self.createStates()
        self.current_state: State = self.state[0]
        self.generateTransitons()
        self.setFinal_lookahead()

    def createToken(self) -> [Tuple[str, str]]:
        if self.current_state.id == 8:
            return "NUM", self.matchStrings
        elif self.current_state.id == 6:
            return "WHITESPACE", self.matchStrings
        elif self.current_state.id == 9:
            matchString = ''.join(self.matchStrings)
            if matchString in self.keywords:
                return "KEYWORD", self.matchStrings
            else:
                matchString = ''.join(self.matchStrings)
                token: str = matchString
                if token not in self.symbol_table:
                    self.symbol_table[token] = [len(self.symbol_table) + 1]
                return "ID", self.matchStrings
        elif self.current_state.id == 3:
            return "SYMBOL", self.matchStrings
        elif self.current_state.id == 10:
            return "SYMBOL", self.matchStrings
        elif self.current_state.id == 11:
            return "SYMBOL", self.matchStrings
        elif self.current_state.id == 12:
            return "SYMBOL", self.matchStrings
        elif self.current_state.id == 15:
            return "COMMENT", self.matchStrings
        elif self.current_state.id == 17:
            return "COMMENT", self.matchStrings
        elif self.current_state.id == 18:
            return "SYMBOL", self.matchStrings

    def get_next_token(self) -> Optional[Tuple[str, str]]:
        if self.end_of_file:
            return "EOF", "$"

        self.matchStrings.clear()
        self.current_state = self.state[0]
        while True:

            if self.current_state.isFinal:
                if self.current_state.isLookAhead:
                    self.matchStrings.pop()
                    self.pointer = self.pointer - 1
                    if self.current_char == '\n':
                        self.line = self.line - 1
                token = self.createToken()
                if token[0] in ["WHITESPACE", "COMMENT"]:
                    self.matchStrings.clear()
                    self.current_state = self.state[0]
                else:
                    return token

            self.current_char = self.nextChar()

            if self.current_char == '\n':
                self.line = self.line + 1

            if self.current_char == self.EOF:
                self.end_of_file = True
            else:
                self.end_of_file = False

            if self.end_of_file and self.current_state.id == 0:
                return 'None'

            self.matchStrings.append(self.current_char)

            for transiton in self.current_state.listTransiton:

                # list transiton is based on prority

                if self.current_char in transiton.moveWith:
                    self.current_state = transiton.end
                    break
            else:
                if not self.end_of_file:
                    self.error_handler(1)
                    self.matchStrings.clear()
                    self.current_state = self.state[0]
                else:
                    self.error_handler(2)
                    return 'None'

    def add_error(self, error: Error):
        if error.line in self.errors_dict:
            self.errors_dict[error.line].append(error)
        else:
            self.errors_dict[error.line] = [error]

    def error_handler(self, error_type: int):

        matchStringsCopy = self.matchStrings.copy()

        if error_type == 1:
            if self.current_state.id == 7 and self.current_char == '/':
                error = Error("Unmatched comment", matchStringsCopy, self.line)
                self.add_error(error)
            elif self.current_state.id == 1 and self.current_char in self.letters:
                error = Error("Invalid number", matchStringsCopy, self.line)
                self.add_error(error)
            else:
                error = Error("Invalid input", matchStringsCopy, self.line)
                self.add_error(error)

        elif error_type == 2:
            if self.current_state.id == 14 or self.current_state.id == 16:
                self.line = self.line - self.matchStrings.count('\n')
                error = Error("Unclosed comment", f"{''.join(self.matchStrings[0:7])}...", self.line)
                self.add_error(error)

    def write_error(self):
        with open("lexical_errors.txt", "w") as error_file:
            if len(self.errors_dict) == 0:
                error_file.write("There is no lexical error.")
            else:
                for line_num in sorted(self.errors_dict.keys()):
                    line = ''.join(
                        [f"({''.join(error.content)}, {error.title}) " for error in self.errors_dict[line_num]])
                    error_file.write(f"{line_num}.\t{line}\n")

    def save_symbols(self):
        with open("symbol_table.txt", mode="w") as symbol_table_file:
            for key, value in self.symbol_table.items():
                symbol_table_file.write(f"{value[0]}.\t{key}\n")

    def nextChar(self):
        if self.pointer >= len(self.file_contents):
            self.end_of_file = True
            return 'None'
        else:
            char = self.file_contents[self.pointer]
            self.pointer = self.pointer + 1
            return char

    def createStates(self):
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
        self.state[2].listTransiton.append(Transition(self.state[2], self.state[9],
                                                      list(self.symbols.union(self.whitespaces, {self.EOF}))))

        # state 3 symbol - lookahead

        # state 4 = , ==
        self.state[4].listTransiton.append(Transition(self.state[4], self.state[10], '='))
        self.state[4].listTransiton.append(Transition(self.state[4], self.state[11],
                                                      (self.valid_chars.union({self.EOF} - {'='}))))
        # state 5 / /*
        self.state[5].listTransiton.append(Transition(self.state[5], self.state[12],
                                                      (self.valid_chars.union({self.EOF}) - {'*'})))
        self.state[5].listTransiton.append(Transition(self.state[5], self.state[14], '*'))

        # state 13 // use less code d`ont need to handle it!
        self.state[13].listTransiton.append(Transition(self.state[13], self.state[13], self.all_chars - {'\n'}))
        self.state[13].listTransiton.append(Transition(self.state[13], self.state[15], {"/n", self.EOF}))

        # state 14 /*
        self.state[14].listTransiton.append(Transition(self.state[14], self.state[14], self.all_chars - {'*'}))
        self.state[14].listTransiton.append(Transition(self.state[14], self.state[16], '*'))

        # state 16 */
        self.state[16].listTransiton.append(Transition(self.state[16], self.state[17], '/'))
        self.state[16].listTransiton.append(Transition(self.state[16], self.state[14], self.valid_chars - {'/'}))

        # state 7 * the only problem is /* without /*
        self.state[7].listTransiton.append(Transition(self.state[7], self.state[18], self.valid_chars - {'/'}))

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


class Parser:
    def __init__(self, scanner: Scanner):
        self.token = None
        self.scanner: Scanner = scanner
        self.LL1Stack = []
        self.grammar = {'First': grammer.first, 'Follow': grammer.follow}
        self.ParseErrors = []
        self.CurrentTer = " "

    def getToken(self):
        self.token = self.scanner.get_next_token()
        if self.token[0] == "ID" or self.token == "NUM":
            self.CurrentTer = self.token[0]
        else:
            self.CurrentTer = self.token[1]

    def add_error(self):
        self.ParseErrors.append(f"#{self.scanner.lineno} : syntax error, {error}")

    def write_errors(self):
        print(self.ParseErrors)

    def run(self):
        self.getToken()
        self.Program()

    def Program(self):
        pass


class Compiler:
    def __init__(self):
        self.scanner = Scanner()
        self.parser = Parser(self.scanner)
        self.parser.run()


if __name__ == '__main__':
    compiler = Compiler()
