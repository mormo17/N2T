class VMWriter:
    # Creates a new file and prepares it for writing.
    def __init__(self, destFilePath):
        self.destFile = destFilePath
    
    # Writes a VM push command.
    #
    # segment - CONST, ARG, LOCAL, STATIC, 
    #           THIS, THAT, POINTER, TEMP
    # index   - int
    def writePush(self, segment, index):
        if segment == "field":
            segment = "this"
        
        toWrite = "push " + segment + " " + str(index) + "\n"
            
        self.destFile.write(toWrite)
    
    # Writes a VM pop command.
    #
    # segment - CONST, ARG, LOCAL, STATIC, 
    #           THIS, THAT, POINTER, TEMP
    # index   - int
    def writePop(self, segment, index):
        if segment == "field":
            segment = "this"
        toWrite = "pop " + segment + " " + str(index) + "\n"
        self.destFile.write(toWrite)
    
    # Writes a VM arithmetic command.
    #
    # command - ADD, SUB, NEG, EQ, GT, LT, AND, OR, NOT
    def WriteArithmetic(self, command):
        toWrite = command + "\n"
        self.destFile.write(toWrite)
    
    # Writes a VM label command.
    #
    # label - String
    def WriteLabel(self, label):
        toWrite = "label " + label + "\n"
        self.destFile.write(toWrite)

    # Writes a VM goto command.
    #
    # label - String
    def WriteGoto(self, label):
        toWrite = "goto " + label + "\n"
        self.destFile.write(toWrite)

    # Writes a VM If-goto command.
    #
    # label - String
    def WriteIf(self, label):
        toWrite = "if-goto " + label + "\n"
        self.destFile.write(toWrite)

    # Writes a VM call command.
    #
    # name - String
    # nArgs - int
    def WriteCall(self, name, nArgs):
        toWrite = "call " + name + " " + str(nArgs) + "\n"
        self.destFile.write(toWrite)
    
    # Writes a VM function command.
    #
    # name - String
    # nArgs - int
    def WriteFunction(self, name, nLocals):
        toWrite = "function " + name + " " + str(nLocals) + "\n"
        self.destFile.write(toWrite)
    
    # Writes a VM return command.
    def writeReturn(self):
        toWrite = "return\n"
        self.destFile.write(toWrite)
    
    # Closes the output file
    def close(self):
        self.destFile.close()



    

