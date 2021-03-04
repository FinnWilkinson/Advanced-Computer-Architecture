class RegFile :

    # Registers. int corresponding value ==> rx = int(x)    i.e. r13 = 13
    # r0, r1, r2, r3, r4, r5, r6, r7, r8, r9, r10, r11, r12, r13, r14, r15, r16, 
    # r17, r18, r19, r20, r21, r22, r23, r24, r25, r26, r27, r28, r29, r30, r31

    def __init__(self, numberOfRegisters) :
        self.Register = [0] * numberOfRegisters

    def Get(self, reg) :
        if(reg == "r0") :
            return self.Register[0]
        elif(reg == "r1") :
            return self.Register[1]
        elif(reg == "r2") :
            return self.Register[2]
        elif(reg == "r3") :
            return self.Register[3]
        elif(reg == "r4") :
            return self.Register[4]
        elif(reg == "r5") :
            return self.Register[5]
        elif(reg == "r6") :
            return self.Register[6]
        elif(reg == "r7") :
            return self.Register[7]
        elif(reg == "r8") :
            return self.Register[8]
        elif(reg == "r9") :
            return self.Register[9]
        elif(reg == "r10") :
            return self.Register[10]
        elif(reg == "r11") :
            return self.Register[11]
        elif(reg == "r12") :
            return self.Register[12]
        elif(reg == "r13") :
            return self.Register[13]
        elif(reg == "r14") :
            return self.Register[14]
        elif(reg == "r15") :
            return self.Register[15]
        elif(reg == "r16") :
            return self.Register[16]
        elif(reg == "r17") :
            return self.Register[17]
        elif(reg == "r18") :
            return self.Register[18]
        elif(reg == "r19") :
            return self.Register[19]
        elif(reg == "r20") :
            return self.Register[20]
        elif(reg == "r21") :
            return self.Register[21]
        elif(reg == "r22") :
            return self.Register[22]
        elif(reg == "r23") :
            return self.Register[23]
        elif(reg == "r24") :
            return self.Register[24]
        elif(reg == "r25") :
            return self.Register[25]
        elif(reg == "r26") :
            return self.Register[26]
        elif(reg == "r27") :
            return self.Register[27]
        elif(reg == "r28") :
            return self.Register[28]
        elif(reg == "r29") :
            return self.Register[29]
        elif(reg == "r30") :
            return self.Register[30]
        elif(reg == "r31") :
            return self.Register[31]

    def Set(self, reg, value) :
        if(reg == "r0") :
            return                      #r0 always returns 0
        elif(reg == "r1") :
            self.Register[1] = value
        elif(reg == "r2") :
            self.Register[2] = value
        elif(reg == "r3") :
            self.Register[3] = value
        elif(reg == "r4") :
            self.Register[4] = value
        elif(reg == "r5") :
            self.Register[5] = value
        elif(reg == "r6") :
            self.Register[6] = value
        elif(reg == "r7") :
            self.Register[7] = value
        elif(reg == "r8") :
            self.Register[8] = value
        elif(reg == "r9") :
            self.Register[9] = value
        elif(reg == "r10") :
            self.Register[10] = value
        elif(reg == "r11") :
            self.Register[11] = value
        elif(reg == "r12") :
            self.Register[12] = value
        elif(reg == "r13") :
            self.Register[13] = value
        elif(reg == "r14") :
            self.Register[14] = value
        elif(reg == "r15") :
            self.Register[15] = value
        elif(reg == "r16") :
            self.Register[16] = value
        elif(reg == "r17") :
            self.Register[17] = value
        elif(reg == "r18") :
            self.Register[18] = value
        elif(reg == "r19") :
            self.Register[19] = value
        elif(reg == "r20") :
            self.Register[20] = value
        elif(reg == "r21") :
            self.Register[21] = value
        elif(reg == "r22") :
            self.Register[22] = value
        elif(reg == "r23") :
            self.Register[23] = value
        elif(reg == "r24") :
            self.Register[24] = value
        elif(reg == "r25") :
            self.Register[25] = value
        elif(reg == "r26") :
            self.Register[26] = value
        elif(reg == "r27") :
            self.Register[27] = value
        elif(reg == "r28") :
            self.Register[28] = value
        elif(reg == "r29") :
            self.Register[29] = value
        elif(reg == "r30") :
            self.Register[30] = value
        elif(reg == "r31") :
            self.Register[31] = value
