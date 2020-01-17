import string
f = open('test.asm', 'r')
f1P = open('Symbol_table_in_assembler.txt','a')
AtoZ = string.ascii_uppercase
line_filter = AtoZ + '\t'
l = 0 # 全部行
l2P = 0 # 全部行
effcL = 1 # 有效行
location = 0
nextLine = 0 # 換行
error = 0
progStartLoc = 0
progEndLoc = 0
progLeng = 0
operand = 0
objectProg = ''
find = 0
objectProgALine = ''
bodyLengALine = 0
findNotEndLoc = 0
endErrorLine = 0
lineNo = 0
canWrite = 0
objectProgHead = ''
tmpObjectProg = ''
aObjectProgInALine = ''
objectProgALineLeng = 0
objectProgALineLengDec = 0
newLineStartLoc = 0
hexNewLineStartLoc = ''
aaa = 0 # 如果RESW和RESB接著出現 只取最後一個進行印出新行開始位置
operandFoundInSymbolTable = 0 # 找不到得到symbol
opcodeFoundInOpcodeTable = 0
decLoc = 0
endError = 0
errorLine = 0
endLoc = 0
# PASS 1
'''lastLine = line[-1] # 找最後一行用來算長度
    if line == lastLine:
        print(operand)
        progEndLoc = operand
        progLeng = (int)(progEndLoc) - (int)(progStartLoc)
        print(progEndLoc)'''
f = open('test.asm', 'r')
for line in f:
    if line[0] not in line_filter:
        l += 1
    elif line[0] in line_filter:
        effcL += 1
        l += 1
        s = ''
        for c in line:
            if c != '.' and c != '\n':
                s += c
            else:
                break
        symbol, mnemonic, operand = s.split('\t', 2) # 切2次變成3欄
        # print(s)
        f1P_Test = open('Symbol_table_in_assembler.txt','r')
        if location == 0: # 處理開頭
            hexs = '0123456789ABCDEF'
            location = operand
            progStartLoc = operand # 算長度用
            for c in location.strip():
                if c not in hexs:
                    error = 1
            if error == 0:
                decLoc = int('0x' + location, 16)
            # print(location)
            dict = {symbol: str(location).lstrip('0x')}
            # print(dict[symbol])
            if symbol != '':
                f1P.close()
                f1P_Test = open('Symbol_table_in_assembler.txt','r')
                for line in f1P_Test:
                    symbolInTable, operandInTable = line.split('\t', 1)
                    if symbol != symbolInTable: 
                        canWrite = 0
                    else:
                        canWrite = 1
                        break
                if canWrite == 0:
                    fOpC = open('opCode.txt', 'r')
                    for line in fOpC:
                        mnemonicInTable, opCodeInTable = line.split('\t', 1)
                        if symbol != mnemonicInTable:
                            canWriteOpC = 0
                        else:
                            canWriteOpC = 1
                            break
                if canWrite == 0 and canWriteOpC == 0:
                    f1P = open('Symbol_table_in_assembler.txt','a')
                    f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                    f1P.close()
                elif canWrite == 1:
                    print('第' + str(l) + '行有誤，LABEL不能重複定義')
                    error = 1
                elif canWriteOpC == 1:
                    print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                    error = 1
            if mnemonic != 'START':
                error = 1
                print('第' + str(l) + '行有誤，首行必須是START')
        elif effcL == 2: # START後的第一行地址同START
            # print(location)
            dict = {symbol: str(location.lstrip('0x'))}
            if symbol != '':
                f1P.close()
                f1P_Test = open('Symbol_table_in_assembler.txt','r')
                for line in f1P_Test:
                    symbolInTable, operandInTable = line.split('\t', 1)
                    if symbol != symbolInTable:  
                        canWrite = 0
                    else:
                        canWrite = 1
                        break
                if canWrite == 0:
                    fOpC = open('opCode.txt', 'r')
                    for line in fOpC:
                        mnemonicInTable, opCodeInTable = line.split('\t', 1)
                        if symbol != mnemonicInTable:
                            canWriteOpC = 0
                        else:
                            canWriteOpC = 1
                            break
                if canWrite == 0 and canWriteOpC == 0:
                    f1P = open('Symbol_table_in_assembler.txt','a')
                    f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                    f1P.close()
                elif canWrite == 1:
                    print('第' + str(l) + '行有誤，LABEL不能重複定義')
                    error = 1
                elif canWriteOpC == 1:
                    print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                    error = 1
            decLoc += 3
            if mnemonic == 'START':
                error = 1
                print('第' + str(l) + '行有誤，START不能在第一行之外')
            if mnemonic == 'END':
                error = 1
                print('第' + str(l) + '行有誤，END不能在最末行之外')
        elif location != 0 and mnemonic == 'BYTE': # 處理BYTE
            if operand.startswith('C'): # C
                location = hex(decLoc)
                # print(location.lstrip('0x'))
                dict = {symbol: str(location).lstrip('0x')}
                if symbol != '':
                    f1P.close()
                    f1P_Test = open('Symbol_table_in_assembler.txt','r')
                    for line in f1P_Test:
                        symbolInTable, operandInTable = line.split('\t', 1)
                        if symbol != symbolInTable:
                            canWrite = 0
                        else:
                            canWrite = 1
                            break
                    if canWrite == 0:
                        for line in fOpC:
                            mnemonicInTable, opCodeInTable = line.split('\t', 1)
                            if symbol != mnemonicInTable:
                                canWriteOpC = 0
                            else:
                                canWriteOpC = 1
                                break
                    if canWrite == 0 and canWriteOpC == 0:
                        f1P = open('Symbol_table_in_assembler.txt','a')
                        f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                        f1P.close()
                    elif canWrite == 1:
                        print('第' + str(l) + '行有誤，LABEL不能重複定義')
                        error = 1
                    elif canWriteOpC == 1:
                        print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                        error = 1
                decLoc += len(operand.strip("C'" + "'"))
            elif operand.startswith('X'): # X
                location = hex(decLoc)
                # print(location.lstrip('0x'))
                dict = {symbol: str(location).lstrip('0x')}
                hexs = '0123456789ABCDEF'
                if symbol != '':
                    f1P.close()
                    f1P_Test = open('Symbol_table_in_assembler.txt','r')
                    for line in f1P_Test:
                        symbolInTable, operandInTable = line.split('\t', 1)
                        if symbol != symbolInTable:
                            canWrite = 0
                        else:
                            canWrite = 1
                            break
                    if canWrite == 0:
                        for line in fOpC:
                            mnemonicInTable, opCodeInTable = line.split('\t', 1)
                            if symbol != mnemonicInTable:
                                canWriteOpC = 0
                            else:
                                canWriteOpC = 1
                                break
                    if canWrite == 0 and canWriteOpC == 0:
                        f1P = open('Symbol_table_in_assembler.txt','a')
                        f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                        f1P.close()
                    elif canWrite == 1:
                        print('第' + str(l) + '行有誤，LABEL不能重複定義')
                        error = 1
                    elif canWriteOpC == 1:
                        print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                        error = 1
                if (int)(len(operand.strip("X'" + "'"))) % 2 == 0: # ''內需為偶數個
                    decLoc += (int)(0.5 * len(operand.strip("X'" + "'")))
                elif (int)(len(operand.strip("X'" + "'"))) % 2 != 0:
                    decLoc += (int)(0.5 * len(operand.strip("X'" + "'")))
                    error = 1
                    print('第' + str(l) + "行有誤，X''裡須為偶數個")
                for c in operand.strip("X'" + "'"): # 如果''內不為16進制數
                    if c not in hexs:
                        error = 1
                        print('第' + str(l) + "行有誤，X''裡須為16進制")
                        break
        elif location != 0 and mnemonic == 'RESB': # 處理RESB
            location = hex(decLoc)
            # print(location.lstrip('0x'))
            dict = {symbol: str(location).lstrip('0x')}
            if symbol != '':
                f1P.close()
                f1P_Test = open('Symbol_table_in_assembler.txt','r')
                for line in f1P_Test:
                    symbolInTable, operandInTable = line.split('\t', 1)
                    if symbol != symbolInTable:
                        
                        canWrite = 0
                    else:
                        canWrite = 1
                        break
                fOpC = open('opCode.txt', 'r')
                if canWrite == 0:
                    for line in fOpC:
                        mnemonicInTable, opCodeInTable = line.split('\t', 1)
                        if symbol != mnemonicInTable:
                            canWriteOpC = 0
                        else:
                            canWriteOpC = 1
                            break
                if canWrite == 0 and canWriteOpC == 0:
                    f1P = open('Symbol_table_in_assembler.txt','a')
                    f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                    f1P.close()
                elif canWrite == 1:
                    print('第' + str(l) + '行有誤，LABEL不能重複定義')
                    error = 1
                elif canWriteOpC == 1:
                    print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                    error = 1
            decLoc += int(operand)
        elif location != 0 and mnemonic == 'RESW': # 處理RESW
            location = hex(decLoc)
            dict = {symbol: str(location).lstrip('0x')}
            if symbol != '':
                f1P.close()
                f1P_Test = open('Symbol_table_in_assembler.txt','r')
                for line in f1P_Test:
                    symbolInTable, operandInTable = line.split('\t', 1)
                    if symbol != symbolInTable:
                        canWrite = 0
                    else:
                        canWrite = 1
                        break
                fOpC = open('opCode.txt', 'r')
                if canWrite == 0:
                    for line in fOpC:
                        mnemonicInTable, opCodeInTable = line.split('\t', 1)
                        if symbol != mnemonicInTable:
                            canWriteOpC = 0
                        else:
                            canWriteOpC = 1
                            break
                if canWrite == 0 and canWriteOpC == 0:
                    f1P = open('Symbol_table_in_assembler.txt','a')
                    f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                    f1P.close()
                elif canWrite == 1:
                    print('第' + str(l) + '行有誤，LABEL不能重複定義')
                    error = 1
                elif canWriteOpC == 1:
                    print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                    error = 1
            decLoc += (int(operand) * 3)
        elif location != 0 and mnemonic == 'RSUB': # 處理RSUB
            location = hex(decLoc)
            dict = {symbol: str(location).lstrip('0x')}
            if operand != '':
                error = 1
                print('第' + str(l) + "行有誤，RSUB不得有Operand")
            elif symbol != '':
                f1P.close()
                f1P_Test = open('Symbol_table_in_assembler.txt','r')
                for line in f1P_Test:
                    symbolInTable, operandInTable = line.split('\t', 1)
                    if symbol != symbolInTable:
                        
                        canWrite = 0
                    else:
                        canWrite = 1
                        break
                fOpC = open('opCode.txt', 'r')
                if canWrite == 0:
                    for line in fOpC:
                        mnemonicInTable, opCodeInTable = line.split('\t', 1)
                        if symbol != mnemonicInTable:
                            canWriteOpC = 0
                        else:
                            canWriteOpC = 1
                            break
                if canWrite == 0 and canWriteOpC == 0:
                    f1P = open('Symbol_table_in_assembler.txt','a')
                    f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                    f1P.close()
                elif canWrite == 1:
                    print('第' + str(l) + '行有誤，LABEL不能重複定義')
                    error = 1
                elif canWriteOpC == 1:
                    print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                    error = 1
            
            decLoc += 3
        else:
            location = hex(decLoc)
            # print(location.lstrip('0x'))
            dict = {symbol: str(location).lstrip('0x')}
            if symbol != '':
                f1P.close()
                f1P_Test = open('Symbol_table_in_assembler.txt','r')
                for line in f1P_Test:
                    # print(line)
                    symbolInTable, operandInTable = line.split('\t', 1)
                    if symbol != symbolInTable:
                        canWrite = 0
                    else:
                        canWrite = 1
                        break
                fOpC = open('opCode.txt', 'r')
                if canWrite == 0:
                    for line in fOpC:
                        mnemonicInTable, opCodeInTable = line.split('\t', 1)
                        if symbol != mnemonicInTable:
                            canWriteOpC = 0
                        else:
                            canWriteOpC = 1
                            break
                if canWrite == 0 and canWriteOpC == 0:
                    f1P = open('Symbol_table_in_assembler.txt','a')
                    f1P.write(symbol + "\t" + dict[symbol].upper() + "\n")
                    f1P.close()
                elif canWrite == 1:
                    print('第' + str(l) + '行有誤，LABEL不能重複定義')
                    error = 1
                elif canWriteOpC == 1:
                    print('第' + str(l) + '行有誤，LABEL不能和mnemonic同名')
                    error = 1
            decLoc += 3
            if mnemonic == 'START':
                error = 1
                print('第' + str(l) + "行有誤，START不能在第一行之外")
f1P.close()
# 算長度
f = open('test.asm', 'r') 
lines = f.readlines()
lastLine = lines[-1]
for line in lines:
    if line is lastLine:
        progEndLoc = decLoc - 3
        # print(progEndLoc)
        if error == 0:
            progLeng = int(progEndLoc) - int('0x' + progStartLoc, 16)
# print(progEndLoc)
# print(findNotEndLoc)
        # print(hex(progLeng))
# END必須在最末行

# if no error
f = open('test.asm', 'r')
fOpC = open('opCode.txt', 'r')
for line in f:
    l2P += 1
    if line[0] in line_filter:
        lineNo += 1
        s = ''
        for c in line:
            if c != '.' and c != '\n':    
                s += c
            else:
                break
        symbol, mnemonic, operand = s.split('\t', 2)
        operand = operand.strip()
        # print(operand)
        # print(lineNo)
        if mnemonic == 'START' and lineNo == 1:
            progName = symbol
            if len(progName) < 6:
                addZero = 6 - len(progName)
            for number in range(1, addZero):
                progName += ' '
            hexs = '0123456789ABCDEF'
            for c in operand.strip(''):
                if c not in hexs:
                    error = 1
                    print('第' + str(l2P) + "行有誤，起始位址須為16進制")
                    break
            if error == 0:
                progStartLoc = int(operand)
                objectProgHead += 'H ' + progName + '  %06d' %(int)(progStartLoc) + ' ' + (hex)(progLeng).lstrip('0x').upper().zfill(6) + '\n'
                newLineStartLoc = progStartLoc
                hexNewLineStartLoc = progStartLoc
                tmpObjectProg += 'T '
                tmpObjectProg += str(newLineStartLoc).zfill(6)
                tmpObjectProg += ' '
                # print('H ' + progName.strip(), '%06d' %(int)(progStartLoc), (hex)(progLeng).lstrip('0x').upper().zfill(6))
                # print(objectProg)
        elif operand != '' and mnemonic != 'END' and not operand.startswith("X'") and not operand.startswith("C'") and not mnemonic == 'RSUB' and not mnemonic == 'WORD' and not ',' in operand and not mnemonic == 'RESB' and not mnemonic == 'RESW' and effcL - 1 != lineNo:
            fOpC = open('opCode.txt', 'r')
            linesss = fOpC.readlines()
            finallLine = linesss[-1]
            for line in linesss:
                opcodeFoundInOpcodeTable = 0
                mnemonicInTable, opCodeInTable = line.split('\t', 1)
                if mnemonic == mnemonicInTable:
                    # print(opCodeInTable.strip(), end = '')
                    aObjectProgInALine = opCodeInTable.strip()
                    opcodeFoundInOpcodeTable = 1
                    break
                if line is finallLine:
                    if opcodeFoundInOpcodeTable == 0:
                        error = 1
                        print('第' + str(l2P) + "行有誤，opcode找不到")
            f1PRead = open('Symbol_table_in_assembler.txt','r')
            liness = f1PRead.readlines()
            finalLine = liness[-1]

            operandFoundInSymbolTable = 0
            for line in liness:
                
                # print(line)
                symbolInTable, locationInTable = line.split('\t', 1)
                if '\t' in line:
                    # print(symbolInTable)
                    if operand == symbolInTable:
                        if aaa == 1:
                            tmpObjectProg += 'T '
                            tmpObjectProg += str(hexNewLineStartLoc.zfill(6))
                            tmpObjectProg += ' '
                            aaa = 0
                        # print(locationInTable.strip(), end = ' ')
                        aObjectProgInALine += locationInTable.strip()
                        aObjectProgInALine += ' '
                        operandFoundInSymbolTable = 1
                        if error == 0:
                            if len(objectProgALine.replace(' ', '')) + len(aObjectProgInALine.replace(' ', '')) <= 60:
                                objectProgALine += aObjectProgInALine
                            else:
                                objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                                objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                                tmpObjectProg += str(objectProgALineLeng)
                                tmpObjectProg += ' '
                                tmpObjectProg += objectProgALine
                                tmpObjectProg += '\n'
                                hexNewLineStartLoc = str(hexNewLineStartLoc)
                                newLineStartLoc = int('0x' + hexNewLineStartLoc, 16)
                                newLineStartLoc += objectProgALineLengDec
                                hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
                                tmpObjectProg += 'T '
                                tmpObjectProg += str(hexNewLineStartLoc).zfill(6)
                                tmpObjectProg += ' '
                                objectProgALine = ''
                                objectProgALine += aObjectProgInALine
                        # print(objectProg)  
                        break
            if operandFoundInSymbolTable == 0:
                error = 1
                print('第' + str(l2P) + "行有誤，找不到symbol")
        elif operand != '' and operand.startswith("X'"):
            aObjectProgInALine = ''
            if mnemonic != 'BYTE':
                error = 1
                print('第' + str(l2P) + "行有誤，應該要是BYTE")
            # print(operand.lstrip("X'").rstrip("'"), end = ' ')
            if operand.lstrip("X'").rstrip("'") == '':
                print('第' + str(l2P) + "行有誤，X''裡不能為空")
                error = 1
            aObjectProgInALine += operand.lstrip("X'").rstrip("'")
            aObjectProgInALine += ' '
            if aaa == 1:
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc.zfill(6))
                tmpObjectProg += ' '
                aaa = 0
            if len(objectProgALine.replace(' ', '')) + len(aObjectProgInALine.replace(' ', '')) <= 60:
                objectProgALine += aObjectProgInALine
            else:
                objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                tmpObjectProg += str(objectProgALineLeng)
                tmpObjectProg += ' '
                tmpObjectProg += objectProgALine
                tmpObjectProg += '\n'
                hexNewLineStartLoc = str(hexNewLineStartLoc)
                newLineStartLoc = int('0x' + hexNewLineStartLoc, 16)
                newLineStartLoc += objectProgALineLengDec
                hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc).zfill(6)
                tmpObjectProg += ' '
                objectProgALine = ''
                objectProgALine += aObjectProgInALine
        elif operand != '' and operand.startswith("C'"):
            aObjectProgInALine = ''
            if mnemonic != 'BYTE':
                error = 1
                print('第' + str(l2P) + "行有誤，應該要是BYTE")
            output = []
            if operand.lstrip("C'").rstrip("'") == '':
                print('第' + str(l2P) + "行有誤，C''裡不能為空")
                error = 1
            for c in operand.lstrip("C'").rstrip("'"):
                cc = ord(c) # 轉成ASCII
                ccc = hex(cc) # 10轉16
                output += ccc.lstrip('0x')
            # print("".join(str(i) for i in output).upper(), end = ' ') # list改用str輸出
            # print(ord(operand.lstrip("C'").rstrip("'")) + '\n')
            for c in output:
                aObjectProgInALine += c.upper()
            aObjectProgInALine += ' '
            if aaa == 1:
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc.zfill(6))
                tmpObjectProg += ' '
                aaa = 0
            if len(objectProgALine.replace(' ', '')) + len(aObjectProgInALine.replace(' ', '')) <= 60:
                objectProgALine += aObjectProgInALine
            else:
                objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                tmpObjectProg += str(objectProgALineLeng)
                tmpObjectProg += ' '
                tmpObjectProg += objectProgALine
                tmpObjectProg += '\n'
                hexNewLineStartLoc = str(hexNewLineStartLoc)
                newLineStartLoc = int('0x' + hexNewLineStartLoc, 16)
                newLineStartLoc += objectProgALineLengDec
                hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc).zfill(6)
                tmpObjectProg += ' '
                objectProgALine = ''
                objectProgALine += aObjectProgInALine
        elif mnemonic == 'RSUB':
            fOpC = open('opCode.txt', 'r')
            linesss = fOpC.readlines()
            finallLine = linesss[-1]
            for line in linesss:
                mnemonicInTable, opCodeInTable = line.split('\t', 1)
                if mnemonic == mnemonicInTable:
                    # print(opCodeInTable.strip(), end = '')
                    aObjectProgInALine = opCodeInTable.strip()
                    break
                if line is finallLine:
                    if opcodeFoundInOpcodeTable == 0:
                        error = 1
                        print('第' + str(l2P) + "行有誤，opcode找不到")
            # print('0000', end = ' ')
            aObjectProgInALine += '0000'
            aObjectProgInALine += ' '
            if aaa == 1:
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc.zfill(6))
                tmpObjectProg += ' '
                aaa = 0
            if len(objectProgALine.replace(' ', '')) + len(aObjectProgInALine.replace(' ', '')) <= 60:
                objectProgALine += aObjectProgInALine
            else:
                objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                tmpObjectProg += str(objectProgALineLeng)
                tmpObjectProg += ' '
                tmpObjectProg += objectProgALine
                tmpObjectProg += '\n'
                hexNewLineStartLoc = str(hexNewLineStartLoc)
                newLineStartLoc = int('0x' + hexNewLineStartLoc, 16)
                newLineStartLoc += objectProgALineLengDec
                hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc).zfill(6)
                tmpObjectProg += ' '
                objectProgALine = ''
                objectProgALine += aObjectProgInALine
        elif mnemonic == 'WORD':
            output = (int)(operand)
            # print(hex(output).lstrip('0x').zfill(6), end = ' ')
            aObjectProgInALine = hex(output).lstrip('0x').zfill(6)
            aObjectProgInALine += ' '
            if aaa == 1:
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc.zfill(6))
                tmpObjectProg += ' '
                aaa = 0
            if len(objectProgALine.replace(' ', '')) + len(aObjectProgInALine.replace(' ', '')) <= 60:
                objectProgALine += aObjectProgInALine
            else:
                objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                tmpObjectProg += str(objectProgALineLeng)
                tmpObjectProg += ' '
                tmpObjectProg += objectProgALine
                tmpObjectProg += '\n'
                hexNewLineStartLoc = str(hexNewLineStartLoc)
                newLineStartLoc = int('0x' + hexNewLineStartLoc, 16)
                newLineStartLoc += objectProgALineLengDec
                hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
                tmpObjectProg += 'T '
                tmpObjectProg += str(hexNewLineStartLoc).zfill(6)
                tmpObjectProg += ' '
                objectProgALine = ''
                objectProgALine += aObjectProgInALine
        elif ',' in operand:
            fOpC = open('opCode.txt', 'r')
            linesss = fOpC.readlines()
            finallLine = linesss[-1]
            for line in linesss:
                mnemonicInTable, opCodeInTable = line.split('\t', 1)
                if mnemonic == mnemonicInTable:
                    # print(opCodeInTable.strip(), end = '')
                    aObjectProgInALine = opCodeInTable.strip()
                    break
                if line is finallLine:
                    if opcodeFoundInOpcodeTable == 0:
                        error = 1
                        print('第' + str(l2P) + "行有誤，opcode找不到")
            f1PRead = open('Symbol_table_in_assembler.txt','r')
            liness = f1PRead.readlines()
            finalLine = liness[-1]
            for line in liness:
                operandFoundInSymbolTable = 0
                symbolInTable, locationInTable = line.split('\t', 1)
                if operand.count(',') > 1:
                    print('第' + str(l2P) + "行有誤，索引定址哪有這麼多逗號")
                    error = 1
                    break
                else:
                    weNeed, trash = operand.split(',')
                    if trash.strip(' ') != 'X':
                        print('第' + str(l2P) + "行有誤，索引定址類型錯誤")
                        error = 1
                        break
                    if weNeed.strip() == symbolInTable:
                        operandFoundInSymbolTable = 1
                        # print(int(locationInTable) + 8000, end = ' ')
                        locationInTableDec = int('0x' + locationInTable, 16)
                        output = int(locationInTableDec) + int('0x8000', 16)
                        aObjectProgInALine += hex(output).lstrip('0x').upper()
                        aObjectProgInALine += ' '
                        if aaa == 1:
                            tmpObjectProg += 'T '
                            tmpObjectProg += str(hexNewLineStartLoc.zfill(6))
                            tmpObjectProg += ' '
                            aaa = 0
                        if len(objectProgALine.replace(' ', '')) + len(aObjectProgInALine.replace(' ', '')) <= 60:
                            objectProgALine += aObjectProgInALine
                        else:
                            objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                            objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                            tmpObjectProg += str(objectProgALineLeng)
                            tmpObjectProg += ' '
                            tmpObjectProg += objectProgALine
                            tmpObjectProg += '\n'
                            hexNewLineStartLoc = str(hexNewLineStartLoc)
                            newLineStartLoc = int('0x' + hexNewLineStartLoc, 16)
                            newLineStartLoc += objectProgALineLengDec
                            hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
                            tmpObjectProg += 'T '
                            tmpObjectProg += str(hexNewLineStartLoc).zfill(6)
                            tmpObjectProg += ' '
                            objectProgALine = ''
                            objectProgALine += aObjectProgInALine
                        break
            if operandFoundInSymbolTable == 0:
                error = 1
                print('第' + str(l2P) + "行有誤，找不到symbol")
        elif mnemonic == 'RESB': # RESB就換行
            if objectProgALine != '':
                objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                tmpObjectProg += str(objectProgALineLeng)
                tmpObjectProg += ' '
                tmpObjectProg += objectProgALine
                objectProgALine = ''
                tmpObjectProg += '\n'
                aaa = 1
            newLineStartLoc += int(operand)
            newLineStartLoc += objectProgALineLengDec
            hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
            # tmpObjectProg += str(hexNewLineStartLoc)
            # tmpObjectProg += ' '
            # print(hexNewLineStartLoc)
        elif mnemonic == 'RESW': # RESW就換行
            if objectProgALine != '':
                objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
                objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper().zfill(2)
                tmpObjectProg += str(objectProgALineLeng)
                tmpObjectProg += ' '
                tmpObjectProg += objectProgALine
                objectProgALine = ''
                tmpObjectProg += '\n'
                aaa = 1
            newLineStartLoc += int(operand) * 3
            # newLineStartLoc += objectProgALineLengDec
            hexNewLineStartLoc = hex(newLineStartLoc).lstrip('0x').upper()
            # tmpObjectProg += str(hexNewLineStartLoc)
            # tmpObjectProg += ' '
        elif mnemonic != 'END' and effcL - 1 == lineNo: # flag設定時effcL = 1, lineNo = 0
            error = 1
            print('第' + str(l2P) + '行有誤，END必須在最末行')
        elif mnemonic == 'END' and effcL - 1 == lineNo: # END
            f1PRead = open('Symbol_table_in_assembler.txt','r')
            liness = f1PRead.readlines()
            for line in liness:
                symbolInTable, locationInTable = line.split('\t', 1)
                if operand != symbolInTable:
                    endError = 1
                elif operand == symbolInTable:
                    endError = 0
                    endLoc = locationInTable
                    break
            if endError == 1:
                error = 1
                print('第' + str(l2P) + '行有誤，END後的operand只能接任何symbol')
            f1PRead.close()
        elif mnemonic == 'END' and effcL - 1 != lineNo:
            error = 1
            print('第' + str(l2P) + '行有誤，END不能在最末行之外')
objectProgALineLengDec = int(1/2 * len(objectProgALine.replace(' ', '')))
objectProgALineLeng = hex(objectProgALineLengDec).lstrip('0x').upper()
tmpObjectProg += str(objectProgALineLeng).zfill(2)
tmpObjectProg += ' '
tmpObjectProg += objectProgALine
tmpObjectProg += '\nE '
tmpObjectProg += str(endLoc).strip().zfill(6)
objectProg = objectProgHead + tmpObjectProg
if error == 0:
    print(objectProg)
fClean = open('Symbol_table_in_assembler.txt', 'w')
fwrite = open('result.txt', 'w')
fwrite.write(objectProg)
# if something error
'''if errorInStartNotInHead == 1:
    print('首行必須是START')
if errorInRsub == 1:
    print('RSUB不得有Operand')
if errorInByteX == 1:
    print("X''裡須為偶數個")
if errorInByteXNot16 == 1:
    print("X''裡須為16進制")
if errorInStart == 1:
    print('START不能在第一行之外')
if errorInEnd == 1:
    print('END不能在最末行之外')
if symbolRepeat == 1:
    print('Symbol不能重複定義')'''