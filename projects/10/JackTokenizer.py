from LexicalElements import LexicalElements
class JackTokenizer:
    
    # Opens the input file/stream and gets ready to tokenize it
    def __init__(self, inputFilePath):
        self.lines = self.getLines(inputFilePath)
        lexicalElement = LexicalElements()
        self.keywords = lexicalElement.getKeywords()
        self.symbols = lexicalElement.getSymbols()
        self.currentToken = ""

    def getLines(self, filePath):
        file = open(filePath, "r")
        lines = []
        for line in file:
            line = line.strip()
            if line != "" and line[0] != "/"and line[0] != "*":
                endIndx = line.find("//") 
                if endIndx != -1:
                    line = line[0:endIndx].strip()
                lines.append(line)
        return lines


    # Do we have more tokens in input?
    def hasMoreTokens(self):
        return len(self.lines) != 0
    
    # Gets the next token from the input and makes
    # it the current token. This method should only
    # be called if hasMoreTokens() is true.
    # Initially there is no current token.
    def advance(self):
        currentLine = self.lines.pop(0)
        currentToBe = ""
        indx = 0
        for ch in currentLine:
            indx += 1
            if(ch.isalpha()):
                currentToBe += ch
            else:
                break
        if indx == 1:
            if currentLine[0] in self.symbols:
                if currentLine[1:] != "":
                    self.lines.insert(0,currentLine[1:])
                self.currentToken = currentLine[0]
            elif currentLine[0] == "\"":
                currentToBe = currentLine[0:currentLine.find("\"", 1)+1]
                indx = len(currentToBe)
                self.lines.insert(0, currentLine[indx:])
                self.currentToken = currentToBe
            elif currentLine[0].isdigit():
                length = 0
                for i in currentLine:
                    if not i.isdigit():
                        break
                    length += 1
                self.currentToken = currentLine[0:length]
                self.lines.insert(0,currentLine[length:])
            else:
                self.lines.insert(0,currentLine[1:])
                self.advance()
        else:
            currentLine = currentLine[indx-1:]
            self.lines.insert(0,currentLine)
            self.currentToken = currentToBe
        
        
    
    # Returns the type of current token.
    def tokenType(self):
        if self.currentToken in self.keywords:
            return "keyword"
        elif self.currentToken in self.symbols:
            return "symbol"
        elif self.currentToken.isdigit():
            return "integerConstant"
        elif self.currentToken[0] == "\"":
            return "stringConstant"
        else:
            return "identifier"
        
    def getCurrentToken(self):
        return self.currentToken
    
    # Returns the keyword which is the current token.
    # Should be called only when tokenType() is KEYWORD.
    def keyWord(self):
        return self.currentToken
    
    # Returns the character which is the current token.
    # Should be called only when tokenType() is SYMBOL.
    def symbol(self):
        if self.currentToken == "<":
            self.currentToken = "&lt;"
        elif self.currentToken == ">":
            self.currentToken = "&gt;"
        elif self.currentToken == "\"":
            self.currentToken = "&quot;"
        elif self.currentToken == "&":
            self.currentToken = "&amp;"
        return self.currentToken

    # Returns the identifier which is the current token.
    # Should be called only when tokenType() is IDENTIFIER.
    def identifier(self):
        return self.currentToken

    # Returns the integer value of the current token.
    # Should be called only when tokenType() is INT_CONST.
    def intVal(self):
        return self.currentToken
    
    # Returns the string value of the current token,
    # without the double quotes. 
    # Should be called only when tokenType() is STRING_CONST.
    def stringVal(self):
        return self.currentToken[1:-1]





