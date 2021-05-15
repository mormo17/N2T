from JackGrammar import JackGrammar
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
        self.tabsCount = 0
        self.isSubroutine = False

##############################################  Compile Class  ##############################################
    
    def ClassStartingLabel(self):
        self.destFile.write("<class>\n")

    def ClassEndingLabel(self):
        self.destFile.write("</class>")
    
    # Compiles a complete class.
    def CompileClass(self):
        self.ClassStartingLabel()
        self.tabsCount += 1

        self.compileClassHelper()

        self.ClassEndingLabel()
        
    # Grammar:
    # class className {classVarDec* subroutine*}
    def compileClassHelper(self):
        if(len(self.lines) == 0):
            self.destFile.write(self.currentLine)
            return

        self.manageNextTranslation()
        self.writeTabs()
        
        if self.currentTokenType == "identifier":
            self.destFile.write(self.currentLine)   
            self.compileClassHelper()
        elif self.currentTokenType == "symbol":
            if self.currentToken != "}":
                self.destFile.write(self.currentLine)
            self.compileClassHelper()
        elif self.currentToken in self.classVarDec:
            self.compileClassVarDec()
            self.compileClassHelper()
        elif self.currentToken in self.subroutineDec:
            self.CompileSubroutineDec()
            self.compileClassHelper()
        elif self.currentToken == "class":
            self.destFile.write(self.currentLine)
            self.compileClassHelper()

##############################################  Compile ClassVarDec  ##############################################
   
    def ClassVarDecStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<classVarDec>\n")
    
    def ClassVarDecEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</classVarDec>\n")

    def compileClassVarDec(self):
        saved = self.tabsCount
        self.tabsCount -= 1
        self.ClassVarDecStartingLabel()
        self.tabsCount += 2
        self.writeCurrentLine()

        self.compileSubroutineDecHelper()
        
        self.tabsCount = saved
        self.ClassVarDecEndingLabel()
        
##############################################  Compile SubroutineDec  ##############################################
    
    def SubroutineDecStartingLabel(self):
        self.destFile.write("<subroutineDec>\n")
    
    def SubroutineDecEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</subroutineDec>\n")

    # Compiles a static declaration or a field declaration.
    def CompileSubroutineDec(self):
        self.SubroutineDecStartingLabel()
        saved = self.tabsCount
        
        self.tabsCount += 1
        self.writeCurrentLine()

        self.compileSubroutineDecHelper()
        
        self.tabsCount = saved
        self.SubroutineDecEndingLabel()

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
        if self.currentToken != ")":
            self.manageNextTranslation()
       
        self.writeTabs()   
        if self.currentToken in self.subroutineDec:
            self.destFile.write(self.currentLine)
            self.compileSubroutineDecHelper()
        elif self.currentToken in self.subs:
            self.destFile.write(self.currentLine)
            self.compileSubroutineDecHelper() 
        elif self.currentTokenType == "identifier":
            self.destFile.write(self.currentLine)
            self.compileSubroutineDecHelper()
        elif self.currentTokenType == "symbol":
            self.destFile.write(self.currentLine)
            if self.currentToken == "(":
                self.compileParameterList()
                self.compileSubroutineDecHelper()
            elif self.currentToken == ")":
                self.getSubroutineBody()
            elif self.currentToken == ",":
                self.compileSubroutineDecHelper()

##############################################  Compile SubroutineBody  ##############################################
    
    def SubroutineBodyStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<subroutineBody>\n")

    def SubroutineEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</subroutineBody>\n")

    def getSubroutineBody(self):
        saved = self.tabsCount
        self.SubroutineBodyStartingLabel()
        self.tabsCount += 1

        self.subroutineBodyhelper()

        self.tabsCount = saved
        self.SubroutineEndingLabel()

    
    def subroutineBodyhelper(self):
        self.checkNextToken()
            
        if self.nextToken == "}":
            self.manageNextTranslation()
            self.writeCurrentLine()
            return
        
        self.manageNextTranslation()
        if self.currentTokenType == "symbol":
            self.writeCurrentLine()
            if self.currentToken == "{":
                self.compileVarDec()
           
       
        self.subroutineBodyhelper()



##############################################  Compile VarDec  ##############################################
    
    def VarDecStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<varDec>\n")

    def VarDecEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</varDec>\n")

    # Compiles a var declaration.
    def compileVarDec(self):
        self.manageNextTranslation()
        if self.currentToken == "var":
            self.VarDecStartingLabel()
            self.tabsCount += 1
            self.writeCurrentLine()
            self.varDecHelper()
        elif self.currentToken in self.statements:
            self.compileStatements()

    def varDecHelper(self):
        self.manageNextTranslation()
        if self.currentToken in self.varDecs or self.currentTokenType in self.varDecs:
            self.writeCurrentLine()
            self.varDecHelper()
        elif self.currentTokenType == "symbol":
            self.writeCurrentLine()
            if self.currentToken == ";":
                self.tabsCount -= 1
                self.VarDecEndingLabel()
                self.compileVarDec()
            else:
                self.varDecHelper()

    
##############################################  Compile ParameterList  ##############################################

    def ParameterListStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<parameterList>\n")

    def ParameterListEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</parameterList>\n")

    # Compiles a (possibly empty) parameter list,
    # not including the enclosing "()".
    def compileParameterList(self):
        self.ParameterListStartingLabel()
        self.tabsCount += 1
        self.writeTabs
        self.manageNextTranslation()
        if self.currentToken != ")":
            self.paramListHelper()
        self.tabsCount -= 1
        self.ParameterListEndingLabel()

    def paramListHelper(self):
        if self.currentTokenType == "symbol":
            if self.currentToken == ",":
                self.writeCurrentLine()
                self.manageNextTranslation()
                self.paramListHelper()
        
        else:
            self.writeCurrentLine()
            self.manageNextTranslation()
            self.checkNextToken()
            self.paramListHelper()


##############################################  Compile Statements  ##############################################

    def StatementsStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<statements>\n")

    def StatementsEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</statements>\n")

    # Compiles a sequence of statements, not including the enclosing "{}".
    def compileStatements(self):
        saved = self.tabsCount
        self.StatementsStartingLabel()  
        self.tabsCount += 1     
        
        self.compileStatementsHelper()
       
        self.tabsCount = saved
        self.StatementsEndingLabel()
        
    def compileStatementsHelper(self):
        if self.currentToken == "do":
            self.compileDo()
            self.manageNextTranslation()
            self.compileStatementsHelper()
        elif self.currentToken == "let":
            self.compileLet()
            self.manageNextTranslation()
            self.compileStatementsHelper()
        elif self.currentToken == "while":
            self.compileWhile()
            self.manageNextTranslation()
            self.compileStatementsHelper()
        elif self.currentToken == "if":
            self.compileIf()
            self.manageNextTranslation()
            self.compileStatementsHelper()
        elif self.currentToken == "return":
            self.compileReturn()


##############################################  Compile do  ##############################################

    def DoStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<doStatement>\n")

    
    def DoEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</doStatement>\n")

    # Compiles a do statement.
    def compileDo(self):
        saved = self.tabsCount
        self.DoStartingLabel()
        self.tabsCount += 1

        self.compileDoHelper()

        self.tabsCount = saved
        self.DoEndingLabel()

    def compileDoHelper(self):
        self.writeCurrentLine()

        self.compileTermHelper()
        
        self.manageNextTranslation()
        
        self.writeCurrentLine()

##############################################  Compile Let  ##############################################

    def LetStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<letStatement>\n")
    
    def LetEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</letStatement>\n")

    # Compiles a let statement.
    def compileLet(self):
        self.LetStartingLabel()
        self.tabsCount += 1

        self.writeCurrentLine()
        
        self.compileLetHelper()
    
    def compileLetHelper(self):
        self.manageNextTranslation()

        if self.currentTokenType == "identifier":
            self.writeCurrentLine()
            self.compileLetHelper()
        elif self.currentTokenType == "symbol":
            self.writeCurrentLine()
            if self.currentToken == ";":
                self.tabsCount -= 1
                self.LetEndingLabel()
            elif self.currentToken == "]":
                self.compileLetHelper()
            else:
                self.CompileExpression()
                self.compileLetHelper()

##############################################  Compile While  ##############################################

    def WhileStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<whileStatement>\n")
    
    def WhileEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</whileStatement>\n")

    # Compiles a while statement.
    def compileWhile(self):
        saved = self.tabsCount
        self.WhileStartingLabel()
        self.tabsCount += 1

        self.compileWhileHelper()
        
        self.tabsCount = saved
        self.WhileEndingLabel()

    def compileWhileHelper(self):
        if self.currentTokenType == "keyword":
            self.writeCurrentLine()
            self.manageNextTranslation()
            self.compileWhileHelper()
        elif self.currentTokenType == "symbol":
            self.writeCurrentLine()
            if self.currentToken == "(":
                self.CompileExpression()
                self.manageNextTranslation()
                self.writeCurrentLine()
                self.manageNextTranslation()
                self.compileWhileHelper()
            elif self.currentToken == "{":
                self.manageNextTranslation()
                self.compileStatements()
                self.writeCurrentLine()

##############################################  Compile return  ##############################################

    def ReturnStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<returnStatement>\n")
    
    def ReturnEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</returnStatement>\n")

    # Compiles a return statement.
    def compileReturn(self):
        self.ReturnStartingLabel()
        self.tabsCount += 1

        self.writeCurrentLine()

        self.checkNextToken()
        if self.nextToken != ";":
            self.CompileExpression()

        self.manageNextTranslation()

        self.writeCurrentLine()

        self.tabsCount -= 1
        self.ReturnEndingLabel()
        

##############################################  Compile If  ##############################################

    def IfStartingStatement(self):
        self.writeTabs()
        self.destFile.write("<ifStatement>\n")
    
    def IfEndingStatement(self):
        self.writeTabs()
        self.destFile.write("</ifStatement>\n")
    
    # Compiles an if statement, posibly with a trailing else clause.
    def compileIf(self):
        saved = self.tabsCount
        self.IfStartingStatement()

        self.tabsCount += 1
        
        self.writeCurrentLine()

        self.compileIfHelper()
        
        self.tabsCount = saved
        self.IfEndingStatement()
        
        self.compileStatementsHelper()

    def compileIfHelper(self):
        self.manageNextTranslation()
        
        if self.currentTokenType in "symbol":
            self.writeCurrentLine()
            if self.currentToken == "(":
                self.CompileExpression()
                self.manageNextTranslation()
                self.writeCurrentLine()
                self.compileIfHelper()
            elif self.currentToken == "{":
                self.manageNextTranslation()
                self.compileStatements()
                self.writeCurrentLine()
                self.checkNextToken()
                if self.nextToken == "else":
                    self.manageNextTranslation()
                    self.writeCurrentLine()
                    self.compileIfHelper()
                

##############################################  Compile Expression  ##############################################
    
    def ExpressionStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<expression>\n")

    def ExpressionEndingLabel(self):        
        self.writeTabs()
        self.destFile.write("</expression>\n")


    # Compiles an expression.
    def CompileExpression(self):
        saved  = self.tabsCount
        self.ExpressionStartingLabel()
        self.tabsCount += 1
        
        self.compileExpressionHelper()
        
        self.tabsCount = saved
        self.ExpressionEndingLabel()
        
        if self.currentToken ==  ",":
            self.writeCurrentLine()


    def compileExpressionHelper(self):
        self.CompileTerm()
        self.checkNextToken()

        if self.nextToken in self.op:
            self.manageNextTranslation()
            self.writeCurrentLine()
            self.compileExpressionHelper()
        elif self.nextToken == ",":
            self.manageNextTranslation()
        
        
##############################################  Compile term  ##############################################

    def TermStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<term>\n")

    def TermEndingLabel(self):      
        self.writeTabs()
        self.destFile.write("</term>\n")


    def CompileTerm(self):
        saved = self.tabsCount
        self.TermStartingLabel()
        self.tabsCount += 1
        
        self.compileTermHelper()
        
        if self.currentToken in self.unaryOp:
            self.CompileTerm()
        
        self.isSubroutine = False
        self.tabsCount = saved
        self.TermEndingLabel()
    
    # subName className varName
    def compileTermHelper(self): 
        self.manageNextTranslation()
        
        if self.currentToken in self.terms or self.currentTokenType in self.terms:
            self.writeCurrentLine()
            if self.currentTokenType == "identifier":
                self.isSubroutine = True
                self.checkNextToken()
                if self.nextToken == "[":
                    self.manageNextTranslation()
                    self.writeCurrentLine()
                    self.CompileExpression()                  
                    self.manageNextTranslation()
                    self.writeCurrentLine()
                    return
                if self.nextToken not in ["[", "(", "."]:
                    return

                self.compileTermHelper()
            
        elif self.currentTokenType == "symbol":
            self.writeCurrentLine()
            if self.currentToken == "(":
                if self.isSubroutine == True:
                    self.isSubroutine = False
                    self.CompileExpressionList()
                else:
                    self.CompileExpression()

                self.manageNextTranslation()
                self.writeCurrentLine()

            elif self.currentToken == ".":
                self.compileTermHelper()
                            
        
##############################################  Compile ExpressionList  ##############################################

    def ExpressionListStartingLabel(self):
        self.writeTabs()
        self.destFile.write("<expressionList>\n")
    
    def ExpressionListEndingLabel(self):
        self.writeTabs()
        self.destFile.write("</expressionList>\n")

    # Compiles a (possibly empty) comma-separated
    # list of expressions.
    def CompileExpressionList(self):
        saved = self.tabsCount
        self.checkNextToken()
        if self.nextToken in self.unaryOp:
            self.CompileExpression()
            return
        
        self.ExpressionListStartingLabel()
        self.tabsCount += 1
        
        self.checkNextToken()
        
        while self.nextToken != ")":
                self.CompileExpression()
        
        self.tabsCount = saved
        self.ExpressionListEndingLabel()

##############################################  Some Helper Functions  ##############################################
    
    # writes N tabs in destination file
    # N: variable updated in functions
    def writeTabs(self):
        for i in range(0, self.tabsCount):
            self.destFile.write("\t")

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

    # writes current line (not only token, but with type)
    # in the destination file
    def writeCurrentLine(self):
        self.writeTabs()
        self.destFile.write(self.currentLine)