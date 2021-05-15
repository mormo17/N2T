class LexicalElements:
    def __init__(self):
        self.keywords = ["class",
                        "constructor",
                        "function",
                        "method",
                        "field",
                        "static",
                        "var",
                        "int",
                        "char",
                        "boolean",
                        "void",
                        "true",
                        "false",
                        "null",
                        "this",
                        "let",
                        "do",
                        "if",
                        "else",
                        "while",
                        "return"]
        self.symbols = ["{",
                        "}",
                        "(",
                        ")",
                        "[",
                        "]",
                        ".",
                        ",",
                        ";",
                        "+",
                        "-",
                        "*",
                        "/",
                        "&",
                        "|",
                        "<",
                        ">",
                        "=",
                        "~"]

    def getKeywords(self):
        return self.keywords
    
    def getSymbols(self):
        return self.symbols