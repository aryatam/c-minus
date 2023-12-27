non_terminals = [
    "Program",
    "DeclarationList",
    "Declaration",
    "DeclarationInitial",
    "DeclarationPrime",
    "VarDeclarationPrime",
    "FunDeclarationPrime",
    "TypeSpecifier",
    "Params",
    "ParamList",
    "Param",
    "ParamPrime",
    "CompoundStmt",
    "StatementList",
    "Statement",
    "ExpressionStmt",
    "SelectionStmt",
    "IterationStmt",
    "ReturnStmt",
    "ReturnStmtPrime",
    "Expression",
    "B",
    "H",
    "SimpleExpressionZegond",
    "SimpleExpressionPrime",
    "C",
    "Relop",
    "AdditiveExpression",
    "AdditiveExpressionPrime",
    "AdditiveExpressionZegond",
    "D",
    "Addop",
    "Term",
    "TermPrime",
    "TermZegond",
    "G",
    "SignedFactor",
    "SignedFactorPrime",
    "SignedFactorZegond",
    "Factor",
    "VarCallPrime",
    "VarPrime",
    "FactorPrime",
    "FactorZegond",
    "Args",
    "ArgList",
    "ArgListPrime"
]

terminals = [
    "ID",
    ";",
    "[",
    "NUM",
    "]",
    "(",
    ")",
    "int",
    "void",
    ",",
    "{",
    "}",
    "break",
    "if",
    "else",
    "while",
    "return",
    "=",
    "<",
    "==",
    "+",
    "-",
    "*"
]

first = {
    "Program": [
        "int", "void", "epsilon"
    ],
    "DeclarationList": [
        "int", "void", "epsilon"
    ],
    "Declaration": [
        "int", "void"
    ],
    "DeclarationInitial": [
        "int", "void"
    ],
    "Declaration-prime": [
        ";", "[", "("
    ],
    "VarDeclarationPrime": [
        ";", "["
    ],
    "FunDeclarationPrime": ["("],
    "TypeSpecifier": [
        "int", "void"
    ],
    "Params": [
        "int", "void"
    ],
    "ParamList": [
        ",", "epsilon"
    ],
    "Param": [
        "int", "void"
    ],
    "ParamPrime": [
        "[", "epsilon"
    ],
    "CompoundStmt": ["{"],
    "StatementList": [
        "ID",
        ";",
        "NUM",
        "(",
        "{",
        "break",
        "if",
        "while",
        "return",
        "+",
        "-",
        "epsilon"
    ],
    "Statement": [
        "ID",
        ";",
        "NUM",
        "(",
        "{",
        "break",
        "if",
        "while",
        "+",
        "-",
        "return"
    ],
    "ExpressionStmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "break"
        "+",
        "-"
    ],
    "SelectionStmt": ["if"],
    "IterationStmt": ["while"],
    "ReturnStmt": ["return"],
    "ReturnStmtPrime": [
        "ID", ";", "NUM", "(", "+", "-"
    ],
    "Expression": [
        "ID", "NUM", "(", "+", "-"
    ],
    "B": [
        "(",
        "[",
        "=",
        "<",
        "==",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "H": [
        "=",
        "<",
        "==",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "SimpleExpressionZegond": [
        "NUM", "(", "+", "-"
    ],
    "SimpleExpressionPrime": [
        "(",
        "<",
        "==",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "C": [
        "<", "==", "epsilon"
    ],
    "Relop": [
        "<", "=="
    ],
    "AdditiveExpression": [
        "ID", "NUM", "(", "+", "-"
    ],
    "AdditiveExpressionPrime": [
        "(",
        "+",
        "-",
        "*",
        "epsilon"
    ],
    "AdditiveExpressionZegond": [
        "NUM", "(", "+", "-"
    ],
    "D": [
        "+", "-", "epsilon"
    ],
    "Addop": [
        "+", "-"
    ],
    "Term": [
        "ID", "NUM", "(", "+", "-"
    ],
    "TermPrime": [
        "(", "*", "epsilon"
    ],
    "TermZegond": [
        "NUM", "(", "+", "-"
    ],
    "G": [
        "*", "epsilon"
    ],
    "SignedFactor": [
        "ID", "NUM", "(", "+", "-"
    ],
    "SignedFactorPrime": [
        "(", "epsilon"
    ],
    "SignedFactorZegond": [
        "NUM", "(", "+", "-"
    ],
    "Factor": [
        "ID", "NUM", "("
    ],
    "VarCallPrime": [
        "[", "(", "epsilon"
    ],
    "VarPrime": [
        "[", "epsilon"
    ],
    "FactorPrime": [
        "(", "epsilon"
    ],
    "FactorZegond": [
        "NUM", "("
    ],
    "Args": [
        "ID", "NUM", "(", "epsilon", "+", "-"
    ],
    "ArgList": [
        "ID", "NUM", "(", "+", "-"
    ],
    "ArgListPrime": [",", "epsilon"]
}

follow = {
    "Program": ["$"],
    "DeclarationList": [
        "ID",
        ";",
        "NUM",
        "(",
        "{",
        "}",
        "break",
        "if",
        "while",
        "return",
        "+",
        "-",
        "$"
    ],
    "Declaration": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "while",
        "return",
        "+",
        "-",
        "$"
    ],
    "DeclarationInitial": [
        ";",
        "[",
        "(",
        ")",
        ","
    ],
    "DeclarationPrime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "while",
        "return",
        "+",
        "-",
        "$"
    ],
    "VarDeclarationPrime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "while",
        "return",
        "+",
        "-",
        "$"
    ],
    "FunDeclarationPrime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "while",
        "return",
        "+",
        "-",
        "$"
    ],
    "TypeSpecifier": ["ID"],
    "Params": [")"],
    "ParamList": [")"],
    "Param": [
        ")", ","
    ],
    "ParamPrime": [
        ")", ","
    ],
    "CompoundStmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "while",
        "return",
        "+",
        "-",
        "$"
    ],
    "StatementList": ["}"],
    "Statement": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "while",
        "return"
        "+",
        "-"
    ],
    "ExpressionStmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "while",
        "return",
        "+",
        "-"
    ],
    "SelectionStmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "while",
        "return"
        "+",
        "-"
    ],
    "IterationStmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "while",
        "return",
        "+",
        "-"
    ],
    "ReturnStmt": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "while",
        "return",
        "+",
        "-"
    ],
    "ReturnStmtPrime": [
        "ID",
        ";",
        "NUM",
        "(",
        "int",
        "void",
        "{",
        "}",
        "break",
        "if",
        "else",
        "while",
        "return"
        "+",
        "-"
    ],
    "Expression": [
        ";", "]", ")", ","
    ],
    "B": [
        ";", "]", ")", ","
    ],
    "H": [
        ";", "]", ")", ","
    ],
    "SimpleExpressionZegond": [
        ";", "]", ")", ","
    ],
    "SimpleExpressionPrime": [
        ";", "]", ")", ","
    ],
    "C": [
        ";", "]", ")", ","
    ],
    "Relop": [
        "ID", "NUM", "(", "+", "-"
    ],
    "AdditiveExpression": [
        ";", "]", ")", ","
    ],
    "AdditiveExpressionPrime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "=="
    ],
    "AdditiveExpressionZegond": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "=="
    ],
    "D": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "=="
    ],
    "Addop": [
        "ID", "NUM", "(", "+", "-"
    ],
    "Term": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "TermPrime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "TermZegond": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "G": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-"
    ],
    "SignedFactor": [
        ";",
        "]",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "SignedFactorPrime": [
        ";",
        "]",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "SignedFactorZegond": [
        ";",
        "]",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "Factor": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "VarCallPrime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "VarPrime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "FactorPrime": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "FactorZegond": [
        ";",
        "]",
        ")",
        ",",
        "<",
        "==",
        "+",
        "-",
        "*"
    ],
    "Args": [")"],
    "ArgList": [")"],
    "ArgListPrime": [")"]
}
