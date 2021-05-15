import os
commands = {
    "add" : "ac", #arithmetic commands
    "sub" : "ac",
    "neg" : "lc", #logical commands
    "eq" : "ac",
    "gt" : "ac",
    "lt" : "ac",
    "and" : "ac",
    "or" : "ac",
    "not" : "lc",
    "pop" : "mac", #memory access commands
    "push" : "mac",
    "label" : "branch",
    "if-goto" : "branch",
    "goto" : "branch",
    "function" : "function",
    "call" : "function",
    "return" : "function"
}

index = 0
currFile = ""
def branchCommand(command, destFile):
    global index
    destFile.write("D=D-M\n")
    destFile.write("@whenBranchTrue" + str(index) + "\n")
    if command == "eq":
        destFile.write("D;JEQ\n")
    elif command == "lt":
        destFile.write("D;JGT\n")
    else:
        destFile.write("D;JLT\n")
    destFile.write("@whenBranchFalse" + str(index) + "\n")
    destFile.write("0;JMP\n")
    destFile.write("(whenBranchTrue" + str(index)+ ")\n")
    destFile.write("@15\n")
    destFile.write("M=-1\n")
    destFile.write("@end" + str(index)+ "\n")
    destFile.write("0;JMP\n")
    destFile.write("(whenBranchFalse"+str(index)+")\n")
    destFile.write("@15\n")
    destFile.write("M=0\n")
    destFile.write("(end" + str(index)+ ")\n")
    pushCommand("", destFile, True, "")
    index += 1

def aCommand(command, destFile):
    popCommand("", destFile, True, 13)
    popCommand("", destFile, True, 14)
    destFile.write("@13\n")
    destFile.write("D=M\n")
    destFile.write("@14\n")
    if command == "add":
        destFile.write("D=D+M\n")
    elif command == "sub":
        destFile.write("D=M-D\n")
    elif command == "eq" or command == "lt" or command == "gt":
        branchCommand(command, destFile)
        return
    elif command == "or":
        destFile.write("D=D|M\n")
        destFile.write("@15\n")
        destFile.write("M=D\n")
        pushCommand("",destFile, True, "")
        return
    elif command == "and":
        destFile.write("D=D&M\n")
        destFile.write("@15\n")
        destFile.write("M=D\n")
        pushCommand("",destFile, True, "")
        return

    destFile.write("@15\n")
    destFile.write("M=D\n")
    pushCommand("", destFile, True, "")


def lCommand(command, destFile):
    popCommand("", destFile, True, 13)
    destFile.write("@13\n")
    if command == "neg":
        destFile.write("D=-M\n")
    elif command == "not":
        destFile.write("D=!M\n")
    destFile.write("@15\n")
    destFile.write("M=D\n")
    pushCommand("", destFile, True, "")

freeSpace = 16

def pushCommand(line, destFile, isAlc, currPath):
    if isAlc:
        destFile.write("@15\n") #@i
        destFile.write("D=M\n")                    
        destFile.write("@0\n") #SP
        destFile.write("A=M\n")
        destFile.write("M=D\n")                   
        destFile.write("@0\n")                   
        destFile.write("M=M+1\n")
        return
    
    segmentType = line[line.find(" ") + 1 : line.find(" ", line.find(" ") + 1)]
    toPush = line[line.find(" ", line.find(" ")+ 1) + 1:]
    if segmentType == "constant":
        destFile.write("@" + toPush+"\n") # @i
        destFile.write("D=A\n")                    
        destFile.write("@0\n") #SP
        destFile.write("A=M\n")
        destFile.write("M=D\n")                   
        destFile.write("@0\n")                   
        destFile.write("M=M+1\n")
    elif segmentType == "pointer":
        if toPush == "0":
            destFile.write("@3\n")
        elif toPush == "1":
            destFile.write("@4\n")
        destFile.write("D=M\n")
        destFile.write("@0\n")
        destFile.write("A=M\n")
        destFile.write("M=D\n")                   
        destFile.write("@0\n")                   
        destFile.write("M=M+1\n") 
    else:
        if toPush.find("\n") == -1:   
            destFile.write("@" + toPush + "\n")
        else:
            destFile.write("@" + toPush)
        destFile.write("D=A\n")
        if segmentType == "local":
            destFile.write("@1\n")
        elif segmentType == "argument":
            destFile.write("@2\n")
        elif segmentType == "this":
            destFile.write("@3\n")
        elif segmentType == "that":
            destFile.write("@4\n")
        elif segmentType == "temp":
            destFile.write("@5\n")
            destFile.write("A=D+A\n")
        elif segmentType == "static":
            destFile.write("@" + currFile + "." + toPush + "\n")
            #destFile.write("D=A\n")
            #destFile.write("A=D\n")
            destFile.write("D=M\n")
            destFile.write("@0\n")
            destFile.write("A=M\n") 
            destFile.write("M=D\n")
            destFile.write("@0\n")                   
            destFile.write("M=M+1\n")  
            return

        if segmentType != "temp":
            destFile.write("A=M+D\n")


        #destFile.write("D=A\n")
        #destFile.write("A=D\n")
        destFile.write("D=M\n")
        destFile.write("@0\n")
        destFile.write("A=M\n") 
        destFile.write("M=D\n")                  
        destFile.write("@0\n")                   
        destFile.write("M=M+1\n")       




def popCommand(segmentType, destFile, isAlc, ptr):
    if isAlc:
        #SP--
        destFile.write("@0\n")                   
        destFile.write("M=M-1\n")                 
        #
        destFile.write("@0\n") #SP
        destFile.write("A=M\n")#*SP
        destFile.write("D=M\n")#*SP
        destFile.write("@"+str(ptr)+"\n")
        destFile.write("M=D\n")
    
    else:
        popCommand("",destFile,True,13)
        #
        destFile.write("@"+ptr.strip()+"\n")
        destFile.write("D=A\n")
        if segmentType == "local":
            destFile.write("@1\n") #local
        elif segmentType == "argument":
            destFile.write("@2\n") #argument
        elif segmentType == "this":
            destFile.write("@3\n") #this
        elif segmentType == "that":
            destFile.write("@4\n") #that
        elif segmentType == "temp":
            destFile.write("@5\n")
            destFile.write("A=D+A\n")
        elif segmentType == "static":
            destFile.write("@13\n")
            destFile.write("D=M\n")
            destFile.write("@" + currFile + "." + ptr.strip() +"\n")
            destFile.write("M=D\n")
            return


        if segmentType != "temp":
            destFile.write("A=M+D\n")
        
        
        destFile.write("D=A\n")
        destFile.write("@14\n")
        destFile.write("M=D\n")
        destFile.write("@13\n")
        destFile.write("D=M\n")
        destFile.write("@14\n")
        destFile.write("A=M\n")
        destFile.write("M=D\n")



def function(destFile, functionName, nArgs):
    global currFile
    currFile = functionName[:functionName.find(".")]

    if functionName.find("\n") != -1:
        functionName = functionName[0:functionName.find("\n")]
    destFile.write("("+functionName+")\n")
    n = int(nArgs)
    i = 0
    while i != n:
        destFile.write("@"+str(i)+"\n")
        destFile.write("D=A\n")
        destFile.write("@0\n")
        destFile.write("D=D+M\n") #saved offset address
        destFile.write("@15\n")
        destFile.write("M=D\n")
        destFile.write("@0\n")
        destFile.write("D=A\n")
        destFile.write("@15\n")
        destFile.write("A=M\n")
        destFile.write("M=D\n")
        destFile.write("@0\n")
        destFile.write("M=M+1\n")
        i += 1

def labelCommand(label, destFile):
    if label.find("\n") != -1:                       
        label = label[0:label.find("\n")]
    
    destFile.write("("+label+")\n")

def gotoCommand(label, destFile):
    if label.find("\n") != -1:
        label = label[0:label.find("\n")]
    destFile.write("@"+label+"\n")
    if label == "retAddr":
        destFile.write("A=M\n")
    destFile.write("0;JMP\n")  

def pushCallArgument(segmentType, destFile):
    if segmentType == "LCL":
        destFile.write("@1\n")
    elif segmentType == "ARG":
        destFile.write("@2\n")
    elif segmentType == "THIS":
        destFile.write("@3\n")
    elif segmentType == "THAT":
        destFile.write("@4\n")
    
    destFile.write("D=M\n")
    destFile.write("@15\n")
    destFile.write("M=D\n")
    pushCommand("", destFile, True, "")

indx = 0

def call(destFile, functionName, nArgs):
    global indx
    # push returnAddress
    #pushCallArgument("returnAddr", destFile)
    destFile.write("@" + functionName + "returnAddr" + str(indx)+ "\n")
    destFile.write("D=A\n")
    destFile.write("@15\n")
    destFile.write("M=D\n")
    pushCommand("", destFile, True, "")
    # push LCL
    pushCallArgument("LCL", destFile)
    # push ARG
    pushCallArgument("ARG", destFile)
    # push THIS
    pushCallArgument("THIS", destFile)
    # push THAT
    pushCallArgument("THAT", destFile)
    # ARG = SP - 5 - nArgs
    destFile.write("@0\n")
    destFile.write("D=M\n")
    destFile.write("@5\n")
    destFile.write("D=D-A\n")
    destFile.write("@"+nArgs+"\n")
    destFile.write("D=D-A\n")
    destFile.write("@2\n")
    destFile.write("M=D\n")
    # LCL = SP
    destFile.write("@0\n")
    destFile.write("D=M\n")
    destFile.write("@1\n")
    destFile.write("M=D\n") 
    # goto functionName
    gotoCommand(functionName, destFile)
    # (returnAddr)
    labelCommand(functionName + "returnAddr" + str(indx), destFile)
    indx += 1
    


def returnCommand(destFile):
    #endFrame = LCL
    destFile.write("@1\n")
    destFile.write("D=M\n")
    destFile.write("@endFrame\n")
    destFile.write("M=D\n")
    #retAddr = *(endFrame-5)
    destFile.write("@5\n")
    destFile.write("D=A\n")
    destFile.write("@endFrame\n")
    destFile.write("A=M\n")
    destFile.write("D=A-D\n") #endFrame-5
    destFile.write("A=D\n")   #*(endFrame-5)
    destFile.write("D=M\n")
    destFile.write("@retAddr\n")
    destFile.write("M=D\n")
    #*ARG=pop()
    popCommand("",destFile, True, 13)
    destFile.write("@13\n")
    destFile.write("D=M\n")
    destFile.write("@2\n")
    destFile.write("A=M\n")
    destFile.write("M=D\n")
    #SP = ARG + 1
    destFile.write("@2\n")
    destFile.write("D=M+1\n")
    destFile.write("@0\n")
    destFile.write("M=D\n")
    #THAT = *(endFrame-1)
    destFile.write("@endFrame\n")
    destFile.write("A=M\n")
    destFile.write("D=A-1\n") #endFrame-1
    destFile.write("A=D\n")   #*(endFrame-1)
    destFile.write("D=M\n")
    destFile.write("@4\n")
    destFile.write("M=D\n")
    #THIS = *(endFrame-2)
    destFile.write("@endFrame\n")
    destFile.write("A=M\n")
    destFile.write("D=A\n")
    destFile.write("@2\n")
    destFile.write("D=D-A\n") #endFrame-2
    destFile.write("A=D\n")   #*(endFrame-2)
    destFile.write("D=M\n")
    destFile.write("@3\n")
    destFile.write("M=D\n")
    #ARG = *(endFrame-3)
    destFile.write("@endFrame\n")
    destFile.write("A=M\n")
    destFile.write("D=A\n")
    destFile.write("@3\n")
    destFile.write("D=D-A\n") #endFrame-3
    destFile.write("A=D\n")   #*(endFrame-3)
    destFile.write("D=M\n")
    destFile.write("@2\n")
    destFile.write("M=D\n")
    #LCL = *(endFrame-4)
    destFile.write("@endFrame\n")
    destFile.write("A=M\n")
    destFile.write("D=A\n")
    destFile.write("@4\n")
    destFile.write("D=D-A\n") #endFrame-4
    destFile.write("A=D\n")   #*(endFrame-4)
    destFile.write("D=M\n")
    destFile.write("@1\n")
    destFile.write("M=D\n")
    #goto retAddr

    gotoCommand("retAddr", destFile)

def openFile(sourcePath, destFilePath, counter, fileName):
    file = open(sourcePath, "r")
    destFile = open(destFilePath, "w")
    if counter > 1:
        destFile.write("@256\n")
        destFile.write("D=A\n")
        destFile.write("@0\n")
        destFile.write("M=D\n")

        call(destFile, "Sys.init", "0")
    for line in file:
        if line != "" and line[0] != '/':
            if line.find("//") != -1:
                line = line[0:line.find("//")]
            command = line[0:line.find(" ")]
            if command != "":
                #arithmetic command
                if commands[command] == "ac":
                    aCommand(command, destFile)
                #logical command
                elif commands[command] == "lc":
                    lCommand(command, destFile)
                #memory access commands
                elif command == "push":
                    pushCommand(line.strip(), destFile, False, fileName)
                elif command == "pop":
                    segmentType = line[line.find(" ")+1 : line.find(" ", line.find(" ") + 1)]
                    toPop = line[line.find(" ", line.find(" ")+1) + 1:].strip()

                    if segmentType == "pointer":
                        if toPop == "0":
                            popCommand(segmentType, destFile, True, 3)
                        elif toPop == "1":
                            popCommand(segmentType, destFile, True, 4)
                    else:
                        popCommand(segmentType, destFile, False, toPop)
                elif command == "label":
                    label = line[line.find(" ")+1:]
                    labelCommand(label.strip(), destFile)
                elif command == "if-goto":
                    label = line[line.find(" ")+1:]
                    if label.find("\n"):                       
                        label = label[0:label.find("\n")]
                    popCommand("", destFile, True, 13)
                    destFile.write("@13\n")
                    destFile.write("D=M\n")
                    destFile.write("@"+label+"\n")
                    destFile.write("D;JNE\n")
                elif command == "goto":
                    label = line[line.find(" ")+1:]
                    gotoCommand(label.strip(), destFile)
                elif command == "function":
                    functionName = line[line.find(" ")+1 : line.find(" ", line.find(" ") + 1)]
                    nArgs = line[line.find(" ", line.find(" ")+1) + 1:].strip()
                    
                    function(destFile, functionName, nArgs) 
                elif command == "call":
                    functionName = line[line.find(" ")+1 : line.find(" ", line.find(" ") + 1)]
                    nArgs = line[line.find(" ", line.find(" ")+1) + 1:].strip()
                    
                    call(destFile, functionName, nArgs)
                elif command == "return":
                    returnCommand(destFile)
    file.close()
    destFile.close()

        

def tmp():
    for folder in os.walk(os.getcwd()):
        merged = ""
        fileName = ""
        filePath = ""
        counter = 0
        for file in folder[2]:
            path = ""
            if folder[0].find("FunctionCalls") != -1:    
                path = folder[0][folder[0].find("08")+3:]
                fileName = path[path.find("\\")+1:]
                filePath = path
            elif folder[0].find("ProgramFlow") != -1:    
                path = folder[0][folder[0].find("08")+3:]
                fileName = path[path.find("\\")+1:]
                filePath = path
           
            if file[len(file)-2:] == "vm":
                opened = open(path + "\\" + file, 'r')
                data = opened.read()
                #merged += "\n"
                merged += data
                opened.close()
                counter += 1
        
        if fileName != "" and filePath != "":
            fileName += ".vm"
            sourcePath = filePath + "\\" + fileName
            destPath = filePath + "\\" + fileName[0:-3]+".asm"
            #sourcePath = "\\" + fileName
            #destPath = "\\" + fileName[0:-3]+".asm"
            mergedVM = open(sourcePath, "w")
            
            mergedVM.write(merged)            
            mergedVM.close()
            openFile(sourcePath, destPath, counter, fileName)

                

tmp()   
