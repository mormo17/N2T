import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine

filePath = ""
tokenizerDestFilePath = ""
finalPath = ""

def compile():
    fileDest = open(tokenizerDestFilePath, "w")
    tokens = JackTokenizer(filePath)

    lines = []
    fileDest.write("<tokens>\n")
    while(tokens.hasMoreTokens()):
        tokens.advance()
        curType = tokens.tokenType()
        if curType == "stringConstant":
            curToken = tokens.stringVal()
        elif curType == "symbol":
            curToken = tokens.symbol()
        else:
            curToken = tokens.getCurrentToken()
                
        toWrite = "<" + curType + ">" + " " + curToken + " " + "</" + curType + ">\n"
        lines.append(toWrite)
        fileDest.write(toWrite)
    fileDest.write("</tokens>")
    fileDest.close()

    finalDestFile = open(finalPath, "w")
    engine = CompilationEngine(lines, finalDestFile)

    engine.CompileClass()
    finalDestFile.close()

for directory in os.walk(os.getcwd()):
    for fileName in directory[2]:
        if fileName.find(".jack") != -1:
            filePath = directory[0] + "/" + fileName
            tokenizerDestFilePath = directory[0]+"/My" + fileName[0:fileName.find(".jack")]+"T.xml"
            finalPath = directory[0]+"/My" + fileName[0:fileName.find(".jack")]+".xml"
            compile()
