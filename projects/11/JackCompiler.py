import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

filePath = ""
tokenList = []

def getTokens():
    tokens = JackTokenizer(filePath)
    # tokenFile = open(tokenFilePath, "w")
    while(tokens.hasMoreTokens()):
        tokens.advance()
        curType = tokens.tokenType()
        if curType == "stringConstant":
            curToken = tokens.stringVal()
        elif curType == "symbol":
            curToken = tokens.symbol()
        else:
            curToken = tokens.getCurrentToken()
        
        currentLine = "<" + curType + "> " + curToken + " </" + curType + ">\n"
        tokenList.append(currentLine)
        # tokenFile.write(currentLine)
    # tokenFile.close()
    

def compile(outputFilePath):
    destFile = open(outputFilePath, "w")
    engine = CompilationEngine(tokenList, destFile)
    engine.CompileClass()
    # tokenList = []
    destFile.close()


for directory in os.walk(os.getcwd()):
    for fileName in directory[2]:
        if fileName.find(".jack") != -1:
            filePath = directory[0] + "/" + fileName
            destFile = directory[0] + "/" + fileName[0:fileName.find(".jack")] + ".vm"
            # tokenFile = directory[0] + "/" + fileName[0:fileName.find(".jack")] + "T.vm"
            getTokens()
            compile(destFile)
            tokenList = []