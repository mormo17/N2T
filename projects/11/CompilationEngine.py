from JackGrammar import JackGrammar
from SymbolTable import SymbolTable
from VMWriter import VMWriter
class CompilationEngine:
    
##############################################  Consructor  ############################################

    # Creates a new compilation engine
    # with the given input and output.
    # The next routine calles must be compileClass().
    def __init__(self, inputLines, filePath):
        # input information
        self.lines = inputLines
        self.destFile = filePath
        # Grammar rules
        grammar = JackGrammar()
        self.subroutineDec = grammar.getSubroutineDec()
        self.subs = grammar.getSubs()
        self.varDecs = grammar.getVarDecs()
        self.statements = grammar.getStatements()
        self.terms = grammar.getTerms()
        self.unaryOp = grammar.getUnaryOp()
        self.op = grammar.getOp()
        self.classVarDec = grammar.getClassVarDec()
        # global variables
        self.currentToken = ""
        self.currentTokenType = ""
        self.currentLine = ""
        self.nextToken = ""
        self.nextTokenType = ""
        self.isSubroutine = False
        self.className = ""
        self.currentFuncionName = ""
        self.nArgs = 0
        self.isRight = False
        self.had_else = False
        self.whileLabelIndex = 0
        self.ifLabelIndex = 0
        self.isConstructor = False
        self.isMethod = False
        self.isArray = False
        self.wasRightArray = False
        self.wasArgument = False
        # SymbolTable
        self.symbolTable = SymbolTable()
        # VMWriter
        self.vmwriter = VMWriter(filePath)

##############################################  Compile Class  ##############################################
   
    # Compiles a complete class.
    def CompileClass(self):        
        self.compileClassHelper()

        
    # Grammar:
    # class className {classVarDec* subroutine*}
    def compileClassHelper(self):
        if(len(self.lines) == 0):
            return

        self.manageNextTranslation()
        if self.currentTokenType == "identifier":
            self.className = self.currentToken
            self.compileClassHelper()
        elif self.currentTokenType == "symbol":
            self.compileClassHelper()
        elif self.currentToken in self.classVarDec:
            self.compileClassVarDec()
            self.compileClassHelper()
        elif self.currentToken in self.subroutineDec: 
            self.CompileSubroutineDec()
            self.compileClassHelper()
        elif self.currentToken == "class":
            self.compileClassHelper()

##############################################  Compile ClassVarDec  ##############################################
   
    def compileClassVarDec(self):
        kind = ""
        type = ""
        while(self.currentToken not in self.subroutineDec):
            kind = self.currentToken
            self.manageNextTranslation()
            type = self.currentToken
            self.manageNextTranslation()
            name = self.currentToken
            self.symbolTable.Define(name, type, kind)

            self.manageNextTranslation()

            while self.currentToken != ";":
                self.manageNextTranslation()
                name = self.currentToken
                self.symbolTable.Define(name, type, kind)
                self.manageNextTranslation()
            
            self.manageNextTranslation()
        if self.currentToken == "constructor":
            self.isConstructor = True 
        self.compileSubroutineDecHelper()
        self.isMethod = False
        
        
##############################################  Compile SubroutineDec  ##############################################
    
    # Compiles a static declaration or a field declaration.
    def CompileSubroutineDec(self):
        self.compileSubroutineDecHelper()
        self.isMethod = False
        
    # Grammar:
    # 'constructor', 'function', 'method'
    # ('void' | type) subroutineName (parameterList)
    # subroutineBody
    def compileSubroutineDecHelper(self):
        if(len(self.lines) == 0):
            return

        self.checkNextToken()
        if self.nextToken == "}":
            return
        if self.currentToken == "method":
            self.isMethod = True
        if self.currentToken != ")":
            self.manageNextTranslation()    
        if self.currentToken in self.subroutineDec:
            self.compileSubroutineDecHelper()
        elif self.currentToken in self.subs:
            self.compileSubroutineDecHelper() 
        
        elif self.currentTokenType == "identifier":
            self.currentFuncionName = self.currentToken
            self.symbolTable.startSubroutine()
            self.compileSubroutineDecHelper()
        
        elif self.currentTokenType == "symbol":
            if self.currentToken == "(":
                self.compileParameterList()
                self.compileSubroutineDecHelper()
            elif self.currentToken == ")":
                self.getSubroutineBody()
            elif self.currentToken == ",":
                self.compileSubroutineDecHelper()

##############################################  Compile SubroutineBody  ##############################################
    
    def getSubroutineBody(self):
        self.subroutineBodyhelper()

    
    def subroutineBodyhelper(self):
        self.checkNextToken()
            
        if self.nextToken == "}":
            self.manageNextTranslation()
            return
        if self.currentToken == "}" and self.had_else:
            self.had_else = False
            return
        self.manageNextTranslation()

        if self.currentTokenType == "symbol":
            if self.currentToken == "{":
                self.compileVarDec()
                self.checkNextToken()
        
        self.subroutineBodyhelper()



##############################################  Compile VarDec  ##############################################
    
    # Compiles a var declaration.
    def compileVarDec(self):
        self.manageNextTranslation()
        if self.currentToken == "var":
            self.manageNextTranslation()
            type = self.currentToken
            self.varDecHelper(type)
        elif self.currentToken in self.statements:
            self.vmwriter.WriteFunction(self.className + "." + self.currentFuncionName, str(self.symbolTable.getSize()))
            if self.isConstructor:
                count = self.symbolTable.VarCount("field")
                self.vmwriter.writePush("constant", count)
                self.vmwriter.WriteCall("Memory.alloc", 1)
                self.vmwriter.writePop("pointer", 0)
                self.isConstructor = False
            elif self.isMethod:
                self.vmwriter.writePush("argument", 0)
                self.vmwriter.writePop("pointer", 0)
            self.compileStatements()

    def varDecHelper(self, type):
        self.manageNextTranslation()
        if self.currentToken in self.varDecs or self.currentTokenType in self.varDecs:
            self.symbolTable.Define(self.currentToken, type, "var")
            self.varDecHelper(type)
        elif self.currentTokenType == "symbol":
            if self.currentToken == ";":
                self.compileVarDec()
            else:
                self.varDecHelper(type)

    
##############################################  Compile ParameterList  ##############################################

    # Compiles a (possibly empty) parameter list,
    # not including the enclosing "()".
    def compileParameterList(self):
        if self.isMethod:
            self.symbolTable.Define("this", self.className, "argument")
        self.manageNextTranslation()
       
        if self.currentToken != ")":
            self.paramListHelper()

    def paramListHelper(self):   
        if self.currentTokenType == "symbol":
            if self.currentToken == ",":
                self.manageNextTranslation()
                self.paramListHelper()
        
        else:
            type = self.currentToken
            if type != "Array":
                type = self.currentTokenType
            self.manageNextTranslation()
            varName = self.currentToken 
            self.symbolTable.Define(varName, type, "arg")
            self.manageNextTranslation()
            self.checkNextToken()
            self.paramListHelper()


##############################################  Compile Statements  ##############################################

    # Compiles a sequence of statements, not including the enclosing "{}".
    def compileStatements(self):        
        self.compileStatementsHelper()
       
        
    def compileStatementsHelper(self):
        if self.currentToken == "do":
            self.compileDo()
            self.manageNextTranslation()
            self.compileStatementsHelper()
        elif self.currentToken == "let":
            self.compileLet()
            if self.nextToken == ";":
                self.manageNextTranslation()
            self.manageNextTranslation()
            self.compileStatementsHelper()
        elif self.currentToken == "while":
            self.compileWhile()
            self.manageNextTranslation()
            self.compileStatementsHelper()
        elif self.currentToken == "if":
            saved = self.ifLabelIndex 
            self.compileIf()
            self.checkNextToken()
            self.checkNextToken()
            if self.nextToken == "else":
                self.manageNextTranslation()
                self.vmwriter.WriteGoto("IF_END_LABEL"+ str(saved))
                self.vmwriter.WriteLabel("IF_FALSE_LABEL"+ str(saved))
                self.had_else = True
                self.compileIf()
                self.vmwriter.WriteLabel("IF_END_LABEL" + str(saved))
            else:
                self.vmwriter.WriteLabel("IF_FALSE_LABEL"+ str(saved))
            self.checkNextToken()
            if self.currentToken == "{" or self.currentToken == "}":
                self.manageNextTranslation()
            
            self.checkNextToken()
            self.compileStatementsHelper()
        elif self.currentToken == "return":
            self.compileReturn()


##############################################  Compile do  ##############################################

    # Compiles a do statement.
    def compileDo(self):
        self.compileDoHelper()
        self.vmwriter.writePop("temp", 0)

    def compileDoHelper(self):
        self.compileTermHelper()
        self.manageNextTranslation()

##############################################  Compile Let  ##############################################

    # Compiles a let statement.
    def compileLet(self):
        self.checkNextToken()
        varName = self.nextToken
        self.isArray = False
        self.wasRightArray = False
        self.isRight = False
        self.compileLetHelper()
        
        type = self.symbolTable.TypeOf(varName)
        
        kind = self.symbolTable.KindOf(varName)
        if self.wasRightArray and type == "Array":
            self.vmwriter.writePop("temp", 0)
            self.vmwriter.writePop("pointer", 1)
            self.vmwriter.writePush("temp", 0)
            self.vmwriter.writePop("that", 0)
            self.isArray = False
        else:
            kind = self.symbolTable.KindOf(varName)
            if kind != "none":
                self.vmwriter.writePop(kind, self.symbolTable.IndexOf(varName))


    def compileLetHelper(self):
        self.manageNextTranslation()
        savedName = self.currentToken
        self.manageNextTranslation()
        if self.currentToken == "[":
            self.CompileExpression()
            kind = self.symbolTable.KindOf(savedName)
            indx = self.symbolTable.IndexOf(savedName)
            if kind != "none":
                self.vmwriter.writePush(kind, indx)
            self.vmwriter.WriteArithmetic("add")
            self.manageNextTranslation()
            self.isArray = True
            self.wasRightArray = True
            self.manageNextTranslation()
        if self.currentToken != "=":
            self.manageNextTranslation()
        self.isRight = True
        self.CompileExpression()

##############################################  Compile While  ##############################################

    # Compiles a while statement.
    def compileWhile(self):
        self.compileWhileHelper()
        

    def compileWhileHelper(self):
        if self.currentTokenType == "keyword":
            self.manageNextTranslation()
            self.compileWhileHelper()
        elif self.currentTokenType == "symbol":
            if self.currentToken == "(":
                self.vmwriter.WriteLabel("WHILE_EXPRESSIONS" + str(self.whileLabelIndex))
                self.CompileExpression()
                self.manageNextTranslation()
                self.vmwriter.WriteArithmetic("not")
                self.vmwriter.WriteIf("WHILE_END" + str(self.whileLabelIndex))
                self.manageNextTranslation()
                self.compileWhileHelper()

            elif self.currentToken == "{":
                saved = self.whileLabelIndex
                self.manageNextTranslation()
                self.whileLabelIndex += 1
                self.compileStatements()
                self.vmwriter.WriteGoto("WHILE_EXPRESSIONS" +  str(saved))
                self.vmwriter.WriteLabel("WHILE_END" + str(saved))

##############################################  Compile return  ##############################################

    # Compiles a return statement.
    def compileReturn(self):
        self.checkNextToken()
        if self.nextToken != ";":
            self.CompileExpression()
        else:
            self.vmwriter.writePush("constant", 0)

        self.vmwriter.writeReturn()
        self.manageNextTranslation()
        

##############################################  Compile If  ##############################################
    
    # Compiles an if statement, posibly with a trailing else clause.
    def compileIf(self):
        self.compileIfHelper()
       

    def compileIfHelper(self):
        self.manageNextTranslation()      
        if self.currentTokenType in "symbol":
            if self.currentToken == "(":
                self.CompileExpression() 
                self.vmwriter.WriteIf("IF_TRUE_LABEL"+ str(self.ifLabelIndex))
                self.vmwriter.WriteGoto("IF_FALSE_LABEL"+ str(self.ifLabelIndex))
                self.vmwriter.WriteLabel("IF_TRUE_LABEL"+ str(self.ifLabelIndex))
                self.manageNextTranslation()
                self.compileIfHelper()
            elif self.currentToken == "{":
                self.ifLabelIndex += 1
                self.manageNextTranslation()
                self.compileStatements()
                if self.currentToken == ";":
                    self.manageNextTranslation()   

##############################################  Compile Expression  ##############################################
    
    # Compiles an expression.
    def CompileExpression(self):
        self.compileExpressionHelper()
        

    def compileExpressionHelper(self):        
        self.CompileTerm()
    
        self.checkNextToken()
        if self.nextToken in self.op:
            self.manageNextTranslation()
            saved = self.currentToken
            self.compileExpressionHelper()
            if saved == "&lt;":
                self.vmwriter.WriteArithmetic("lt")
            elif saved == "&gt;":
                self.vmwriter.WriteArithmetic("gt")
            elif saved == "+":
                self.vmwriter.WriteArithmetic("add")
            elif saved == "-":
                self.vmwriter.WriteArithmetic("sub")
            elif saved == "*":
                self.vmwriter.WriteCall("Math.multiply", 2)    
            elif saved == "/":
                self.vmwriter.WriteCall("Math.divide", 2)
            elif saved == "=":
                self.vmwriter.WriteArithmetic("eq")
            elif saved == "|":
                self.vmwriter.WriteArithmetic("or")
            elif saved == "&amp;":
                self.vmwriter.WriteArithmetic("and")
                
            
        elif self.nextToken == ",":
            self.manageNextTranslation()
        
        
##############################################  Compile term  ##############################################

    def CompileTerm(self):  
        self.compileTermHelper()
        
        if self.currentToken in self.unaryOp:
            saved = self.currentToken
            self.CompileTerm()
            if saved == "-":
                self.vmwriter.WriteArithmetic("neg")
            else:
                self.vmwriter.WriteArithmetic("not")
        
        self.isSubroutine = False
    
    # subName className varName
    def compileTermHelper(self): 
        self.manageNextTranslation()
        
        if self.currentToken in self.terms or self.currentTokenType in self.terms:
            if self.currentTokenType == "integerConstant":
                self.vmwriter.writePush("constant", self.currentToken)
            elif self.currentTokenType == "stringConstant":
                self.vmwriter.writePush("constant", len(self.currentToken))
                self.vmwriter.WriteCall("String.new", 1)
                for ch in self.currentToken:
                    self.vmwriter.writePush("constant", ord(ch))
                    self.vmwriter.WriteCall("String.appendChar", 2) 
            elif self.currentTokenType == "keyword":
                if self.currentToken == "null":
                    self.vmwriter.writePush("constant", 0) 
                elif self.currentToken == "true":
                    self.vmwriter.writePush("constant", 0) 
                    self.vmwriter.WriteArithmetic("not")
                elif self.currentToken == "false":
                    self.vmwriter.writePush("constant", 0)
                elif self.currentToken == "this":
                    self.vmwriter.writePush("pointer", 0)
            elif self.currentTokenType == "identifier":

                if self.isSubroutine:
                    varName = self.currentToken
                    kind = self.symbolTable.KindOf(varName)
                else:
                    self.checkNextToken()
                    if self.nextToken == ";":
                        kind = self.symbolTable.KindOf(self.currentToken)
                        indx = self.symbolTable.IndexOf(self.currentToken)
                        self.vmwriter.writePush(kind, indx)
                        return
                    if self.nextTokenType == "symbol" and self.nextToken != ".":
                        varName = self.currentToken
                        kind = self.symbolTable.KindOf(varName)
                        if kind == "none":
                            self.vmwriter.writePush("pointer", 0)
                            self.isSubroutine = True
                            self.compileTermHelper()
                            self.vmwriter.WriteCall(self.className + "." + varName, self.nArgs + 1)
                            return
                            

                self.currentFuncionName = self.currentToken
                self.isSubroutine = True
                self.checkNextToken()
                savedName = self.currentToken
                savednxt = self.nextToken
                self.checkNextToken()
                if savednxt not in self.op and self.nextToken != ")" and self.nextToken != "]" and self.nextToken != "(":
                    self.manageNextTranslation()
                if self.currentToken == "[":
                    self.CompileExpression()
                    if not self.isRight:
                        self.wasRightArray = True
                    self.isArray = True
                    self.manageNextTranslation()
                if self.symbolTable.KindOf(savedName) != "none":
                    self.vmwriter.writePush(self.symbolTable.KindOf(savedName), self.symbolTable.IndexOf(savedName))
                kind = self.symbolTable.KindOf(self.currentToken)
                if kind == "argument":
                    self.wasArgument = True
                if self.isArray and not self.wasArgument and not self.isSubroutine:
                    if self.isRight:
                        self.isArray = False
                    self.vmwriter.WriteArithmetic("add")
                    self.vmwriter.writePop("pointer", 1)
                    self.vmwriter.writePush("that", 0)
                if self.currentToken == ".":
                    saved = savedName
                    self.manageNextTranslation()
                    
                    toWrite = self.currentFuncionName + "." + self.currentToken
                    savedCurrent = self.currentToken
                    self.compileTermHelper()
                    type = self.symbolTable.TypeOf(savedCurrent)
                    if type == "none":
                        type = self.symbolTable.TypeOf(saved)

                    if type == "none": # function
                        self.vmwriter.WriteCall(toWrite, self.nArgs)
                    else:
                        kind = self.symbolTable.TypeOf(savedCurrent)
                        indx = self.symbolTable.IndexOf(savedCurrent)
                        if kind != "none":
                            self.vmwriter.writePush(kind, indx)
                        self.currentFuncionName = type
                        saved = self.symbolTable.TypeOf(saved)
                        toWrite = saved + "." + savedCurrent
                        self.nArgs += 1
                        self.vmwriter.WriteCall(toWrite, self.nArgs)

                if self.nextToken not in ["[", "(", "."]:
                    return

                self.compileTermHelper()
         
        if self.currentTokenType == "symbol":

            if self.currentToken == "(":
                if self.isSubroutine == True:
                    self.nArgs = 0
                    self.CompileExpressionList()
                    self.isSubroutine = False
                else:
                    self.CompileExpression()

                self.manageNextTranslation()
                    
                            
        
##############################################  Compile ExpressionList  ##############################################

    # Compiles a (possibly empty) comma-separated
    # list of expressions.
    def CompileExpressionList(self):
        self.checkNextToken()

        if self.nextToken in self.unaryOp:
            self.CompileExpression()
            return

        self.checkNextToken()
        
        while self.nextToken != ")":
            self.nArgs += 1
            self.CompileExpression()
        

##############################################  Some Helper Functions  ##############################################
    
    # updates next token (token itself and its type)
    # without removing from general list
    def checkNextToken(self):
        toCheck = self.lines[0]
        type = toCheck[1:toCheck.find(">")]
        startIndx = toCheck.find(">") + 2
        endIndx = toCheck.find("<", startIndx) - 1
        token = toCheck[startIndx:endIndx]
        self.nextToken = token
        self.nextTokenType = type

    # removes next token from general list
    # and updates information about current token
    def manageNextTranslation(self):
        toTranslate = self.lines.pop(0)
        self.currentLine = toTranslate
        type = toTranslate[1:toTranslate.find(">")]
        startIndx = toTranslate.find(">") + 2
        endIndx = toTranslate.find("<", startIndx) - 1
        token = toTranslate[startIndx:endIndx]
        self.currentToken = token
        self.currentTokenType = type