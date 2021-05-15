symbols = {
    "R0" : 0,
    "R1" : 1,
    "R2" : 2,
    "R3" : 3,
    "R4" : 4,
    "R5" : 5,
    "R6" : 6,
    "R7" : 7,
    "R8" : 8,
    "R9" : 9,
    "R11" : 11,
    "R12" : 12,
    "R13" : 13,
    "R14" : 14,
    "R15" : 15,
    "SP" : 0,
    "LCL" : 1,
    "ARG" : 2,
    "THIS" : 3,
    "THAT" : 4,
    "SCREEN" : 16384,
    "KBD" : 24576    
}

dest = {
    "" : "000",
    "M" : "001",
    "D" : "010",
    "MD" : "011",
    "A" : "100",
    "AM" : "101",
    "AD" : "110",
    "AMD" : "111"
}

jump = {
    "" : "000",
    "JGT" : "001",
    "JEQ" : "010",
    "JGE" : "011",
    "JLT" : "100",
    "JNE" : "101",
    "JLE" : "110",
    "JMP" : "111"
}

# a == 0
comp = {
    "0" : "101010",
    "1" : "111111",
    "-1" : "111010",
    "D" : "001100",
    "A" : "110000",
    "!D" : "001101",
    "!A" : "110001",
    "-D" : "001111",
    "-A" : "110011",
    "D+1" : "011111",
    "A+1" : "110111",
    "D-1" : "001110",
    "A-1" : "110010",
    "D+A" : "000010",
    "D-A" : "010011",
    "A-D" : "000111",
    "D&A" : "000000",
    "D|A" : "010101"
}

#a == 1
compA = {
    "M" : comp["A"],
    "!M" : comp["!A"],
    "-M" : comp["-A"],
    "M+1" : comp["A+1"],
    "M-1" : comp["A-1"],
    "D+M" : comp["D+A"],
    "D-M" : comp["D-A"],
    "M-D" : comp["A-D"],
    "D&M" : comp["D&A"],
    "D|M" : comp["D|A"]    
}


def getFile():
    file = open("rect/RectL.asm", "r")
    counter = -1
    for line in file:
        if line != "":
            spaceFree = line.strip().replace(" ","")
            if spaceFree.find("//") != -1:
                spaceFree = spaceFree[0:spaceFree.find("//")]
            if spaceFree != "":
                counter+=1
                if spaceFree[0] == '(':
                    symbols[spaceFree[1:-1]] = counter
                    counter -= 1
    file.close()


def writeFile():
    freeSpace = 16
    file = open("rect/RectL.asm", "r")
    fileDest = open("rect/RectL.hack", "w")

    for line in file:
        if line != "":
            spaceFree = line.strip().replace(" ","")
            if spaceFree.find("//") != -1:
                spaceFree = spaceFree[0:spaceFree.find("//")]
            if spaceFree != "" and spaceFree[0] != '(':
                if spaceFree[0] == '@':
                    if spaceFree[1:] in symbols:
                        toConvert = symbols[spaceFree[1:]]
                        converted = bin(toConvert)[2:]
                        fileDest.write(((16-len(converted)) * '0' + converted) + "\n")
                    elif spaceFree[1:].isnumeric():
                        toConvert = int(spaceFree[1:])
                        symbols[spaceFree[1:]] = toConvert
                        converted = bin(toConvert)[2:]
                        fileDest.write(((16-len(converted)) * '0' + converted) + "\n")
                    else:
                        symbols[spaceFree[1:]] = freeSpace
                        converted = bin(freeSpace)[2:]
                        fileDest.write(((16-len(converted)) * '0' + converted) + "\n")
                        freeSpace+=1
                else:
                    res  = "111"
                    destRes = ""
                    compRes = ""
                    jmpRes = ""
                    equalsIndx = spaceFree.find("=")
                    
                    if equalsIndx != -1:
                        destVar = spaceFree[0:equalsIndx]
                        compVar = spaceFree[equalsIndx+1:]    
                    else:
                        destVar = ""
                        compVar = spaceFree
                    
                    if destVar in dest:
                        destRes = dest[destVar]
                    if ";" in compVar:
                        jmpVar = compVar[compVar.find(";")+1:]
                        compVar = compVar[0:compVar.find(";")]
                        jmpRes = jump[jmpVar]
                    else:
                        jmpRes = jump[jmpRes]
                        
                    if compVar in comp:
                            compRes = "0" + comp[compVar]
                    elif compVar in compA:
                        compRes = "1" + compA[compVar]
                    res += compRes + destRes + jmpRes
                    fileDest.write(res+"\n")
                    
    file.close()
    fileDest.close()


getFile()
writeFile()
