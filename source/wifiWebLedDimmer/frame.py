# from datetime import datetime

class Frame:
    Master = 64; ServerReq = 100;
    returnPowerOrStatus = ''
    returnMac = ''

    pidOrg = [0,1]; rxtxOrg = [Master,1];
    sensor = [1,1]; micom = [1,1]; gidOrg = [0,2]
    high = [100,1]; low = [1,1]; level = [50,1]; Type = [1,1]; rate = [1,1]
    status = [1,1]; dtime = [1,2]
    cmd = [ServerReq,1]; sub = [1,1]; time = [1,2]
    pid = [1,1]; rxtx = [64,1];  gid = [2,2]; srcGid = [1,2]
    tbd0 = [1,2]; tbd1 = [1,2]; tbd2 = [1,2]; zone = [1,1]; CheckSum = [1,1]
    crc = [1,2]

    frameList = [ pidOrg, rxtxOrg, sensor, micom, gidOrg,
        high, low, level, Type, rate, status, dtime,
        cmd, sub, time,
        pid, rxtx, gid, srcGid, tbd0, tbd1, tbd2, zone, CheckSum, crc ]

    frame = ''
    byteList = []
    # input buffer clear
    clearBuffFlag = False
    newFrameFlag = False

    def __init__(self):
        self.frame = ''
        print('=================== frame start')

    def getFrame(self):
        return self.frame

    def setCrcFrame(self, frame):
        tempList = []

        for numList in frame:
            if(numList[1]==2):
                tempList.append(numList[0]%256)
                tempList.append(int(numList[0]/256))
            else:
                tempList.append(numList[0])
        tempList = tempList[0:(len(tempList)-2)]
        crcIn = bytearray(tempList)
        crcResult = self.getCrc(crcIn)
        self.crc[0] = crcResult

    def setFrame(self):
        self.setCrcFrame(self.frameList)
        self.frame = '{'
        for numList in self.frameList:
            if(numList[1]==2):
                self.frame += '%02x' % (numList[0]%256)
                self.frame += '%02x' % int(numList[0]/256)
            else:
                self.frame += '%02x' % numList[0]
        self.frame += '}'
        # print('SendFrame:{}'.format(self.frame))
        # self.returnPowerOrStatus = 'No Ack From Gateway'
    def getCrc(self, data):
        from crc import CRC
        crc16 = CRC()
        return crc16.update(data)

    def setReceiveFrame(self):
        # dt = datetime.now()
        self.setCrcFrame(self.frameList)
        self.frame = '{'
        for numList in self.frameList:
            if(numList[1]==2):
                self.frame += '%02x' % (numList[0]%256)
                self.frame += '%02x' % int(numList[0]/256)
            else:
                self.frame += '%02x' % numList[0]
        self.frame += '}'
        # with open('receive.txt','a') as fp:
        #     writeStr = 'Receive:: '+ self.frame
        #     print(writeStr, file = fp)
            # print(self.frame, file = fp)
        print(self.frame)

    def printSubName(self, sub):
        result = ''
        if(sub == 103):
            result = 'Control Ack'
        elif sub == 104:
            result = 'AutoMode Ack'
        elif( sub == 102 ):
            result = 'Monitor Ack'
        elif( sub == 108 ):
            result = 'GroupChange Ack'
        elif( sub == 109 ):
            result = 'Alternaibe Ack'
        elif sub == 110:
            result = 'Status Ack'
        elif sub == 101:
            result = 'PowerRead Ack'
        else:
            result = 'Error:{}'.format(sub)
        return result

    def parseFrame(self, inFrame):
        first = inFrame.rfind('{')
        last = inFrame.rfind('}')
        self.returnPowerOrStatus = 'No Return From Gateway'
        if last > 150:
            self.clearBuffFlag = True
        else:
            self.clearBuffFlag = False

        if (last - first -1) == 68:
            self.clearBuffFlag = True
            result = inFrame[(first+1):last]

            count = 0
            temp = list(); self.byteList = list();
            for s in range(1,35):
                ss = result[count:count+2]
                temp.append(int(ss,16))
                self.byteList.append(int(ss,16))
                count += 2
            temp = temp[0:(len(temp)-2)]
            crcIn = bytearray(temp)
            crcResult = self.getCrc(crcIn)

            count = 0
            for i in self.frameList:
                if i[1] == 2:
                    i[0] = self.byteList[count]
                    count += 1
                    i[0] += self.byteList[count]*256
                else:
                    i[0] = self.byteList[count]
                count += 1

            if crcResult == self.crc[0]:
                # print('Crc Ok, Passed')
                if self.sub[0] == 101: #Power Read
                    print('Power:{}'.format(self.rate[0]+self.status[0]*0x100+
                        self.dtime[0]*0x10000))
                    self.returnPowerOrStatus = 'Power:{}'.format(self.rate[0]+self.status[0]*0x100+
                        self.dtime[0]*0x10000)

                elif self.sub[0] == 110:   #Status
                    print('Photo:{} traffic:{} status:{} level:{}'.format(self.dtime[0],
                        (self.high[0] + self.low[0]*256), self.rate[0], self.level[0]))

                    self.returnPowerOrStatus = 'Photo:{} traffic:{} status:{} level:{}'.format(self.dtime[0],
                        (self.high[0] + self.low[0]*256), self.rate[0], self.level[0])
                else:
                    self.returnPowerOrStatus = 'Command:{}'.format(self.printSubName(self.sub[0]))

                print('Cmd:{}, Sub:{}'.format(self.cmd[0], self.sub[0]))
                # print('{:04x},{:04x},{:04x}'.format(self.tbd01[0],self.tbd11[0],
                    # self.tbd21[0]))
                    # pidOrg1, rxtxOrg1, sensor1, micom1, gidOrg1,
                self.returnMac = 'Gid:{}, Pid:{}, RxTx:{}:::{:04x},{:04x},{:04x}'.format(
                    self.gidOrg[0], self.pidOrg[0], self.rxtxOrg[0],
                    self.tbd0[0],self.tbd1[0],self.tbd2[0])
                self.newFrameFlag = True
                self.setReceiveFrame()
            else:
                print('Crc error:{},{}'.format(crcResult, self.crc[0]))

            return True

        else:
            return False
