class JackGrammar:
    def __init__(self):
        # self.class = ["class"]
        self.classVarDec = ["static","field"]
        self.type = ["int", "char", "boolean", "identifier"]
        self.subroutineDec = ["constructor", "function", "method", ]
        self.subroutines = ["void"] + self.type
        self.varDec = ["var"] + self.type
        self.statements = ["let", "if", "do", "while", "return"]
        self.keywordConstant = ["true", "false", "null", "this"]
        self.op = ["+", "-", "*", "/", "&amp;", "|", "&lt;", "&gt;", "="] 
        self.unaryOp = ["~", "-"]   
        self.term = ["integerConstant", "stringConstant", "identifier"] + self.keywordConstant + self.unaryOp
    
    def getClassVarDec(self):
        return self.classVarDec

    def getSubroutineDec(self):
        return self.subroutineDec
    
    def getSubs(self):
        return self.subroutines

    def getVarDecs(self):
        return self.varDec

    def getStatements(self):
        return self.statements
    
    def getTerms(self):
        return self.term

    def getUnaryOp(self):
        return self.unaryOp

    def getOp(self):
        return self.op