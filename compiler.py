import json
import string
from typing import List, Optional, Set, Dict, Tuple, Union
from anytree import Node, RenderTree
import grammer

epsilon = "epsilon"


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
            return "$", "$"

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
        self.LineParser = 1
        self.name = " "
        self.root = None
        self.token = None
        self.scanner: Scanner = scanner
        self.LL1Stack = []
        self.grammar = {'first': grammer.first, 'follow': grammer.follow}
        self.ParseErrors = []
        self.CurrentTer = " "

    def create_parse_tree_file(self):
        root = self.root
        with open('parse_tree.txt', 'w', encoding="utf-8") as tree_file:
            for pre, fill, node in RenderTree(root):
                tree_file.write("%s%s\n" % (pre, node.name))

    def create_syntax_error_file(self):
        with open('syntax_errors.txt', 'w') as file:
            if not self.ParseErrors:
                file.write("There is no syntax error.\n")
            else:
                for error in self.ParseErrors:
                    file.write(f"{error}\n")

    def addError(self, error):
        self.ParseErrors.append(error)

    def getLine(self):
        self.LineParser = self.scanner.line
        return self.LineParser

    def PanicError(self, name, method, node):
        if self.CurrentTer in self.grammar["Follow"][name]:
            self.addError(f"#{self.getLine()} : syntax error, missing {name}")
            node.parent = None
        else:
            if self.terminal == '$':
                self.LL1Stack = [('', '')]
                node.parent = None
            else:
                self.addError(f"#{self.getLine()} : syntax error, illegal {self.CurrentTer}")
                self.getToken()
                parent = node.parent
                node.parent = None
                self.LL1Stack.append((method, parent))

    def getToken(self):
        self.token = self.scanner.get_next_token()
        if self.token[0] == "ID" or self.token[0] == "NUM":
            self.CurrentTer = self.token[0]
        else:
            self.CurrentTer = self.token[1]

    def parse(self):
        self.getToken()
        # input first node Program
        self.Program()
        while len(self.LL1Stack):
            pop = self.LL1Stack.pop()
            TerOrNotTer, parent = pop

            if callable(TerOrNotTer):
                TerOrNotTer(parent)

            else:
                if TerOrNotTer == self.CurrentTer:
                    lexeme = '$' if self.CurrentTer == '$' else f"({self.token[0]}, {self.token[1]})"
                    Node(lexeme, parent)
                    self.next_token()
                else:
                    if self.CurrentTer == '$':
                        self.addError(f"#{self.scanner.line} : syntax error, Unexpected EOF")
                        self.LL1Stack.clear()
                    else:
                        self.addError(f"#{self.scanner.line} : syntax error, missing {TerOrNotTer}")

    def Program(self):
        self.name = "Program"
        self.root = Node(self.name)
        if self.CurrentTer in self.grammar['first']['DeclarationList']:
            self.LL1Stack.append(("$", self.root))
            self.LL1Stack.append((self.DeclarationList, self.root))
        elif "epsilon" in self.grammar['first']['DeclarationList']:
            if self.CurrentTer in self.grammar['follow']['Program']:
                self.LL1Stack.append(("$", self.root))
                self.LL1Stack.append((self.DeclarationList, self.root))
        else:
            self.PanicError(self.name, self.Program, self.root)

    def DeclarationList(self, parent):
        self.name = "DeclarationList"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammer["first"]["Declaration"]:
            self.LL1Stack.append((self.DeclarationList, node))
            self.LL1Stack.append((self.Declaration, node))
        # epsilon rule is a terminal
        elif self.CurrentTer in self.grammar["follow"]["DeclarationList"]:
            Node(epsilon, node)
        else:
            self.PanicError(self.name, self.DeclarationList, node)

    def Declaration(self, parent):
        self.name = "Declaration"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["DeclarationInitial"]:
            self.LL1Stack.append((self.DeclarationPrime, node))
            self.LL1Stack.append((self.DeclarationInitial, node))
        else:
            self.PanicError(self.name, self.Declaration, node)

    def DeclarationInitial(self, parent):
        self.name = "DeclarationInitial"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["TypeSpecifier"]:
            self.LL1Stack.append(("ID", node))
            self.LL1Stack.append((self.TypeSpecifier, node))
        else:
            self.PanicError(self.name, self.DeclarationInitial, node)

    def DeclarationPrime(self, parent):
        self.name = "DeclarationPrime"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["FunDeclarationPrime"]:
            self.LL1Stack.append((self.FunDeclarationPrime, node))
        elif self.CurrentTer in self.grammar["first"]["VarDeclarationPrime"]:
            self.LL1Stack.append((self.VarDeclarationPrime, node))

        else:
            self.PanicError(self.name, self.DeclarationPrime, node)

    def VarDeclarationPrime(self, parent):
        self.name = "VarDeclarationPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == ';':
            self.LL1Stack.append((";", node))
        elif self.CurrentTer == '[':
            self.LL1Stack.append((";", node))
            self.LL1Stack.append(("]", node))
            self.LL1Stack.append(("NUM", node))
            self.LL1Stack.append(("[", node))
        else:
            self.PanicError(self.name, self.VarDeclarationPrime, node)

    def FunDeclarationPrime(self, parent):
        self.name = "FunDeclarationPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == '(':
            self.LL1Stack.append((self.CompoundStmt, node))
            self.LL1Stack.append((")", node))
            self.LL1Stack.append((self.Params, node))
            self.LL1Stack.append(("(", node))

        else:
            self.PanicError(self.name, self.FunDeclarationPrime, node)

    def TypeSpecifier(self, parent):
        self.name = "TypeSpecifier"
        node = Node(self.name, parent)
        if self.CurrentTer == "int":
            self.LL1Stack.append(("int", node))
        elif self.CurrentTer == "void":
            self.LL1Stack.append(("void", node))

        else:
            self.PanicError(self.name, self.TypeSpecifier, node)

    def Params(self, parent):
        self.name = "Params"
        node = Node(self.name, parent)
        if self.CurrentTer == "int":
            self.LL1Stack.append((self.ParamList, node))
            self.LL1Stack.append((self.ParamPrime, node))
            self.LL1Stack.append(("ID", node))
            self.LL1Stack.append(("int", node))

        elif self.CurrentTer == "void":
            self.LL1Stack.append(("void", node))

        else:
            self.PanicError(self.name, self.Params, node)

    def ParamList(self, parent):
        self.name = "ParamList"
        node = Node(self.name, parent)
        if self.CurrentTer == ',':
            self.LL1Stack.append((self.ParamList, node))
            self.LL1Stack.append((self.Param, node))
            self.LL1Stack.append((",", node))

        elif self.CurrentTer in self.grammar["follow"]["ParamList"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.ParamList, node)

    def Param(self, parent):
        self.name = "Param"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["DeclarationInitial"]:
            self.LL1Stack.append((self.ParamPrime, node))
            self.LL1Stack.append((self.DeclarationInitial, node))

        else:
            self.PanicError(self.name, self.Param, node)

    def ParamPrime(self, parent):
        self.name = "ParamPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == '[':
            self.LL1Stack.append((']', node))
            self.LL1Stack.append(('[', node))

        elif self.CurrentTer in self.grammar["follow"]["ParamPrime"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.ParamPrime, node)

    def CompoundStmt(self, parent):
        self.name = "CompoundStmt"
        node = Node(self.name, parent)
        if self.CurrentTer == '{':
            self.LL1Stack.append(("}", node))
            self.LL1Stack.append((self.StatementList, node))
            self.LL1Stack.append((self.DeclarationList, node))
            self.LL1Stack.append(("{", node))

        else:
            self.PanicError(self.name, self.CompoundStmt, node)

    def StatementList(self, parent):
        self.name = "StatementList"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["Statement"]:
            self.LL1Stack.append((self.StatementList, node))
            self.LL1Stack.append((self.Statement, node))

        elif self.CurrentTer in self.grammar["follow"]["StatementList"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.StatementList, node)

    def Statement(self, parent):
        self.name = "ExpressionStmt"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["ExpressionStmt"]:
            self.LL1Stack.append((self.ExpressionStmt, node))
        elif self.CurrentTer in self.grammar["first"]["CompoundStmt"]:
            self.LL1Stack.append((self.CompoundStmt, node))
        elif self.CurrentTer in self.grammar["first"]["SelectionStmt"]:
            self.LL1Stack.append((self.SelectionStmt, node))
        elif self.CurrentTer in self.grammar["first"]["IterationStmt"]:
            self.LL1Stack.append((self.IterationStmt, node))
        elif self.CurrentTer in self.grammar["first"]["ReturnStmt"]:
            self.LL1Stack.append((self.ReturnStmt, node))

        else:
            self.PanicError(self.name, self.Statement, node)

    def ExpressionStmt(self, parent):
        self.name = "ExpressionStmt"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["Expression"]:
            self.LL1Stack.append((";", node))
            self.LL1Stack.append((self.Expression, node))

        elif self.CurrentTer == "break":
            self.LL1Stack.append((";", node))
            self.LL1Stack.append(("break", node))

        elif self.CurrentTer == ";":
            self.LL1Stack.append((";", node))

        else:
            self.PanicError(self.name, self.ExpressionStmt, node)

    def SelectionStmt(self, parent):
        self.name = "SelectionStmt"
        node = Node(self.name, parent)
        if self.CurrentTer == "if":
            self.LL1Stack.append((self.Statement, node))
            self.LL1Stack.append(("else", node))
            self.LL1Stack.append((self.Statement, node))
            self.LL1Stack.append((")", node))
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("(", node))
            self.LL1Stack.append(("if", node))

        else:
            self.PanicError(self.name, self.SelectionStmt, node)

    def IterationStmt(self, parent):
        self.name = "IterationStmt"
        node = Node(self.name, parent)
        if self.CurrentTer == "while":
            self.LL1Stack.append((self.Statement, node))
            self.LL1Stack.append((")", node))
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("(", node))
            self.LL1Stack.append(("while", node))
        else:
            self.PanicError(self.name, self.IterationStmt, node)

    def ReturnStmt(self, parent):
        self.name = "ReturnStmt"
        node = Node(self.name, parent)
        if self.CurrentTer == "return":
            self.LL1Stack.append((self.ReturnStmtPrime, node))
            self.LL1Stack.append(("return", node))

        else:
            self.PanicError(self.name, self.ReturnStmt, node)

    def ReturnStmtPrime(self, parent):
        self.name = "ReturnStmtPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == ";":
            self.LL1Stack.append((";", node))

        elif self.CurrentTer in self.grammar["first"]["Expression"]:
            self.LL1Stack.append((";", node))
            self.LL1Stack.append((self.Expression, node))

        else:
            self.PanicError(self.name, self.ReturnStmtPrime, node)

    def Expression(self, parent):
        self.name = "Expression"
        node = Node(self.name, parent)

        if self.CurrentTer in self.grammar["first"]["SimpleExpressionZegond"]:
            self.LL1Stack.append((self.SimpleExpressionZegond, node))

        elif self.CurrentTer == "ID":
            self.LL1Stack.append((self.B, node))
            self.LL1Stack.append(("ID", node))

        else:
            self.PanicError(self.name, self.Expression, node)

    def B(self, parent):

        self.name = "B"
        node = Node(self.name, parent)

        if self.CurrentTer == "=":
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("=", node))

        elif self.CurrentTer == "[":
            self.LL1Stack.append((self.H, node))
            self.LL1Stack.append(("]", node))
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("[", node))

        elif self.CurrentTer in self.grammar["first"]["SimpleExpressionPrime"] or self.CurrentTer in \
                self.grammar["follow"]["B"]:
            self.LL1Stack.append((self.SimpleExpressionPrime, node))

        else:
            self.PanicError(self.name, self.B, node)

    def H(self, parent):
        self.name = "H"
        node = Node(self.name, parent)

        if self.CurrentTer == "=":
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("=", node))

        if self.CurrentTer in self.grammar["first"]["G"] or self.CurrentTer in self.grammar["first"][
            "D"] or self.CurrentTer in self.grammar["first"]["C"] or self.CurrentTer in self.grammar["follow"]["H"]:
            self.LL1Stack.append((self.C, node))
            self.LL1Stack.append((self.D, node))
            self.LL1Stack.append((self.G, node))

        else:
            self.PanicError(self.name, self.H, node)

    def SimpleExpressionZegond(self, parent):
        self.name = "SimpleExpressionZegond"
        node = Node(self.name, parent)

        if self.CurrentTer in self.grammar["first"]["AdditiveExpressionZegond"]:
            self.LL1Stack.append(("C", node))
            self.LL1Stack.append((self.AdditiveExpressionZegond, node))

        else:
            self.PanicError(self.name, self.SimpleExpressionZegond, node)

    def SimpleExpressionPrime(self, parent):
        self.name = "SimpleExpressionPrime"
        node = Node(self.name, parent)

        if self.CurrentTer in self.grammar["first"]["SimpleExpressionPrime"] or self.CurrentTer in \
                self.grammar["follow"]["SimpleExpressionPrime"]:
            self.LL1Stack.append(("C", node))
            self.LL1Stack.append((self.AdditiveExpressionZegond, node))

        else:
            self.PanicError(self.name, self.SimpleExpressionPrime, node)

    def C(self, parent):
        self.name = "C"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["Relop"]:
            self.LL1Stack.append((self.AdditiveExpression, node))
            self.LL1Stack.append((self.Relop, node))

        elif self.CurrentTer in self.grammar["follow"]["C"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.C, node)

    def Relop(self, parent):
        self.name = "Relop"
        node = Node(self.name, parent)
        if self.CurrentTer == "<":
            self.LL1Stack.append(("<", node))
        elif self.CurrentTer == "==":
            self.LL1Stack.append(("==", node))

        else:
            self.PanicError(self.name, self.Relop, node)

    # not done yet
    def AdditiveExpression(self, parent):
        self.name = "AdditiveExpression"
        node = Node(self.name, parent)

        if self.CurrentTer in self.grammar["first"]["Term"]:
            self.LL1Stack.append((self.D, node))
            self.LL1Stack.append((self.Term, node))

        else:
            self.PanicError(self.name, self.AdditiveExpression, node)

    def AdditiveExpressionPrime(self, parent):
        self.name = "AdditiveExpressionPrime"
        node = Node(self.name, parent)

        if self.CurrentTer in self.grammar["first"]["TermPrime"] or self.CurrentTer in self.grammar["first"][
            "D"] or self.CurrentTer in self.grammar["follow"]["AdditiveExpressionPrime"]:
            self.LL1Stack.append((self.D, node))
            self.LL1Stack.append((self.TermPrime, node))

        else:
            self.PanicError(self.name, self.AdditiveExpressionPrime, node)

    def AdditiveExpressionZegond(self, parent):
        self.name = "AdditiveExpressionZegond"
        node = Node(self.name, parent)

        if self.CurrentTer in self.grammar["first"]["TermZegond"]:
            self.LL1Stack.append((self.D, node))
            self.LL1Stack.append((self.TermZegond, node))

        else:
            self.PanicError(self.name, self.AdditiveExpressionZegond, node)

    def D(self, parent):
        self.name = "Addop"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["Addop"]:
            self.LL1Stack.append((self.D, node))
            self.LL1Stack.append((self.Term, node))
            self.LL1Stack.append((self.Addop, node))

        elif self.CurrentTer in self.grammar["follow"]["D"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.D, node)

    def Addop(self, parent):
        self.name = "Addop"
        node = Node(self.name, parent)

        if self.CurrentTer == "+":
            self.LL1Stack.append(("+", node))
        elif self.CurrentTer == "-":
            self.LL1Stack.append(("-", node))
        else:
            self.PanicError(self.name, self.Addop, node)

    def Term(self, parent):
        self.name = "Term"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["SignedFactor"]:
            self.LL1Stack.append((self.G, node))
            self.LL1Stack.append((self.SignedFactor, node))
        else:
            self.PanicError(self.name, self.Term, node)

    def TermPrime(self, parent):
        self.name = "TermPrime"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["SignedFactorPrime"] or self.CurrentTer in self.grammar["first"][
            "G"] or self.CurrentTer in self.grammar["follow"]["TermPrime"]:
            self.LL1Stack.append((self.G, node))
            self.LL1Stack.append((self.SignedFactorPrime, node))
        else:
            self.PanicError(self.name, self.TermPrime, node)

    def TermZegond(self, parent):
        self.name = "TermZegond"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["SignedFactorZegond"]:
            self.LL1Stack.append((self.G, node))
            self.LL1Stack.append((self.SignedFactorZegond, node))
        else:
            self.PanicError(self.name, self.TermZegond, node)

    def G(self, parent):
        self.name = "G"
        node = Node(self.name, parent)
        if self.CurrentTer == "*":
            self.LL1Stack.append((self.G, node))
            self.LL1Stack.append((self.SignedFactor, node))
            self.LL1Stack.append(("*", node))

        elif self.CurrentTer in self.grammar["follow"]["G"]:
            Node(epsilon, node)
        else:
            self.PanicError(self.name, self.G, node)

    def SignedFactor(self, parent):
        self.name = "SignedFactor"
        node = Node(self.name, parent)
        if self.CurrentTer == "+":
            self.LL1Stack.append((self.Factor, node))
            self.LL1Stack.append(("+", node))

        elif self.CurrentTer == "-":
            self.LL1Stack.append((self.Factor, node))
            self.LL1Stack.append(("-", node))

        elif self.CurrentTer in self.grammar["first"]["Factor"]:
            self.LL1Stack.append((self.Factor, node))
        else:
            self.PanicError(self.name, self.SignedFactor, node)

    def SignedFactorPrime(self, parent):
        self.name = "SignedFactorPrime"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["FactorPrime"] or self.CurrentTer in self.grammar["follow"][
            "SignedFactorPrime"]:
            self.LL1Stack.append((self.FactorPrime, node))

        else:
            self.PanicError(self.name, self.SignedFactorPrime, node)

    def SignedFactorZegond(self, parent):
        self.name = "SignedFactorZegond"
        node = Node(self.name, parent)
        if self.CurrentTer == "+":
            self.LL1Stack.append((self.Factor, node))
            self.LL1Stack.append(("+", node))

        elif self.CurrentTer == "-":
            self.LL1Stack.append((self.Factor, node))
            self.LL1Stack.append(("-", node))

        elif self.CurrentTer in self.grammar["first"]["FactorZegond"]:
            self.LL1Stack.append((self.FactorZegond, node))
        else:
            self.PanicError(self.name, self.SignedFactorZegond, node)

    def Factor(self, parent):
        self.name = "Factor"
        node = Node(self.name, parent)
        if self.CurrentTer == "(":
            self.LL1Stack.append((")", node))
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("(", node))

        elif self.CurrentTer == "ID":
            self.LL1Stack.append((self.VarCallPrime, node))
            self.LL1Stack.append(("ID", node))

        elif self.CurrentTer == "NUM":
            self.LL1Stack.append(("NUM", node))
        else:
            self.PanicError(self.name, self.Factor, node)

    def VarCallPrime(self, parent):
        self.name = "VarCallPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == "(":
            self.LL1Stack.append((")", node))
            self.LL1Stack.append((self.Args, node))
            self.LL1Stack.append(("(", node))

        elif self.CurrentTer in self.grammar["first"]["VarPrime"] or self.CurrentTer in self.grammar["follow"][
            "VarCallPrime"]:
            self.LL1Stack.append((self.VarPrime, node))

        else:
            self.PanicError(self.name, self.VarCallPrime, node)

    def VarPrime(self, parent):
        self.name = "VarPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == "[":
            self.LL1Stack.append(("]", node))
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("[", node))

        elif self.CurrentTer in self.grammar["follow"]["VarPrime"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.VarPrime, node)

    def FactorPrime(self, parent):
        self.name = "FactorPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == "(":
            self.LL1Stack.append((")", node))
            self.LL1Stack.append((self.Args, node))
            self.LL1Stack.append(("(", node))

        elif self.CurrentTer in self.grammar["follow"]["FactorPrime"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.FactorPrime, node)

    def FactorZegond(self, parent):
        self.name = "FactorZegond"
        node = Node(self.name, parent)
        if self.CurrentTer == "(":
            self.LL1Stack.append((")", node))
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append(("(", node))

        elif self.CurrentTer == "NUM":
            self.LL1Stack.append(("NUM", node))

        else:
            self.PanicError(self.name, self.FactorZegond, node)

    def Args(self, parent):
        self.name = "Args"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["ArgList"]:
            self.LL1Stack.append((self.ArgList, node))

        elif self.CurrentTer in self.grammar["follow"]["Args"]:
            Node(epsilon, node)
        else:
            self.PanicError(self.name, self.Args, node)

    def ArgList(self, parent):
        self.name = "ArgList"
        node = Node(self.name, parent)
        if self.CurrentTer in self.grammar["first"]["Expression"]:
            self.LL1Stack.append((self.ArgListPrime, node))
            self.LL1Stack.append((self.Expression, node))

        else:
            self.PanicError(self.name, self.ArgList, node)

    def ArgListPrime(self, parent):
        self.name = "ArgListPrime"
        node = Node(self.name, parent)
        if self.CurrentTer == ',':
            self.LL1Stack.append((self.ArgListPrime, node))
            self.LL1Stack.append((self.Expression, node))
            self.LL1Stack.append((",", node))

        elif self.CurrentTer in self.grammar["follow"]["ArgListPrime"]:
            Node(epsilon, node)

        else:
            self.PanicError(self.name, self.ArgListPrime, node)


class Compiler:
    def __init__(self):
        self.scanner = Scanner()
        self.parser = Parser(self.scanner)
        self.parser.parse()
        self.parser.create_parse_tree_file()
        self.parser.create_syntax_error_file()


if __name__ == '__main__':
    compiler = Compiler()
