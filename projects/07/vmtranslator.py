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
    "push" : "mac"
}

index = 0

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
    pushCommand("",destFile,True)
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
        pushCommand("",destFile, True)
        return
    elif command == "and":
        destFile.write("D=D&M\n")
        destFile.write("@15\n")
        destFile.write("M=D\n")
        pushCommand("",destFile, True)
        return

    destFile.write("@15\n")
    destFile.write("M=D\n")
    pushCommand("", destFile, True)


def lCommand(command, destFile):
    popCommand("", destFile, True, 13)
    destFile.write("@13\n")
    if command == "neg":
        destFile.write("D=-M\n")
    elif command == "not":
        destFile.write("D=!M\n")
    destFile.write("@15\n")
    destFile.write("M=D\n")
    pushCommand("", destFile, True)

freeSpace = 16

def pushCommand(line, destFile, isAlc):
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
        destFile.write("@" + toPush) # @i
        destFile.write("D=A\n")                    
        destFile.write("@0\n") #SP
        destFile.write("A=M\n")
        destFile.write("M=D\n")                   
        destFile.write("@0\n")                   
        destFile.write("M=M+1\n")
    elif segmentType == "pointer":
        if toPush == "0\n":
            destFile.write("@3\n")
        elif toPush == "1\n":
            destFile.write("@4\n")
        destFile.write("D=M\n")
        destFile.write("@0\n")
        destFile.write("A=M\n")
        destFile.write("M=D\n")                   
        destFile.write("@0\n")                   
        destFile.write("M=M+1\n") 
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
            global freeSpace
            destFile.write("@" + str(freeSpace)+ "\n")

        if segmentType != "temp":
            destFile.write("A=M+D\n")


        destFile.write("D=A\n")
        destFile.write("A=D\n")
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
        destFile.write("@"+ptr)
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
            global freeSpace
            destFile.write("@"+str(freeSpace)+"\n")


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




def openFile():
    file = open("MemoryAccess/BasicTest/BasicTest.vm")
    destFile = open("MemoryAccess/BasicTest/BasicTest.asm", "w")
    for line in file:
        if line != "" and line.find("//") == -1:
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
                   pushCommand(line, destFile, False)
                elif command == "pop":
                    segmentType = line[line.find(" ")+1 : line.find(" ", line.find(" ") + 1)]
                    toPop = line[line.find(" ", line.find(" ")+1) + 1:]
                    if segmentType == "pointer":
                        if toPop == "0\n":
                            popCommand(segmentType, destFile, True, 3)
                        elif toPop == "1\n":
                            popCommand(segmentType, destFile, True, 4)
                    else:
                        popCommand(segmentType, destFile, False, toPop)
                


                    
    file.close()

openFile()