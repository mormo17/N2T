class SymbolTable:

    # Creates a new empty symbol table.
    #
    # 0th index of inner lists refers to name
    # 1st index of inner lists refers to type
    # 2nd index of inner lists refers to index
    def __init__(self):
        # ClassTable
        self.fieldTable = []
        self.staticTable = []
        self.fieldIndx = 0
        self.staticIndx = 0
        # SubroutineTable
        self.argTable = []
        self.localTable = []
        self.argIndx = 0
        self.localIndx = 0

    # Starts a new subroutine scope
    # (i.e., resets the subroutine's symbol table).    
    def startSubroutine(self):
        self.argTable = []
        self.localTable = []
        self.argIndx = 0
        self.localIndx = 0


    # Defines a new identifier of a given name, type, and kind
    # and assigns it a running index.
    # STATIC and FIELD identifiers have a class scope, while ARG
    # and VAR identifiers have a subroutine scope.
    #
    # name - String
    # type - String
    # kind - STATIC, FIELD, ARG or VAR
    def Define(self, name, type, kind):
        if kind == "field":
            self.fieldTable.append([name, type, self.fieldIndx])
            self.fieldIndx += 1
        elif kind == "static":
            self.staticTable.append([name, type, self.staticIndx])
            self.staticIndx += 1
        elif kind == "var":
            self.localTable.append([name, type, self.localIndx])
            self.localIndx += 1
        else:
            self.argTable.append([name, type, self.argIndx])
            self.argIndx += 1
    
    # Returns the number of variables
    # of the given kind already definied in the current scope.
    #
    # kind - STATIC, FIELD, ARG or VAR
    def VarCount(self, kind):
        if kind == "field":
            return self.fieldIndx
        elif kind == "static":
            return self.staticIndx
        elif kind == "var":
            return self.localIndx
        else:
            return self.argIndx
        
    

    # Returns the kind of the names identifier in the current scope.
    # If the identifier is unknown in the current scope, returns NONE.
    def KindOf(self, name):
        for toFind in self.fieldTable:
            if toFind[0] == name:
                return "field"

        for toFind in self.staticTable:
            if toFind[0] == name:
                return "static"

        for toFind in self.argTable:
            if toFind[0] == name:
                return "argument"

        for toFind in self.localTable:
            if toFind[0] == name:
                return "local" 

        return "none"      

    
    # Returns the type of the names identifier in the current scope.
    def TypeOf(self, name):
        for toFind in self.fieldTable:
            if toFind[0] == name:
                return toFind[1]

        for toFind in self.staticTable:
            if toFind[0] == name:
                return toFind[1]

        for toFind in self.argTable:
            if toFind[0] == name:
                return toFind[1]

        for toFind in self.localTable:
            if toFind[0] == name:
                return toFind[1]
        
        return "none"   
    
    # Returns the index assigned to the named identifier.
    def IndexOf(self, name):
        for toFind in self.fieldTable:
            if toFind[0] == name:
                return toFind[2]

        for toFind in self.staticTable:
            if toFind[0] == name:
                return toFind[2]

        for toFind in self.argTable:
            if toFind[0] == name:
                return toFind[2]

        for toFind in self.localTable:
            if toFind[0] == name:
                return toFind[2] 
        
        return "none"  

    def getArgs(self):
        # print("\n\n\n")
        print("@@@@@")
        print(self.argTable)
        
        print("@@@@@")
        # print("\n\n\n")
    
    def getSize(self):
        return self.localIndx
