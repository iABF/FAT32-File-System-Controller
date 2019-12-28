import time


class DBR:
    def __init__(self, data):
        data.seek(0x0B)
        self.sizeofSector = int.from_bytes(data.read(2), 'little')
        data.seek(0x0D)
        self.SectorPerCluster = int.from_bytes(data.read(1), 'little')
        data.seek(0x0E)
        self.NumberOfReservedSector = int.from_bytes(data.read(2), 'little')
        data.seek(0x20)
        self.NumberOfSector = int.from_bytes(data.read(4), 'little')
        data.seek(0x24)
        self.SectorPerFAT = int.from_bytes(data.read(4), 'little')
        data.seek(0x2C)
        self.ClusterNumberOfRootDir = int.from_bytes(data.read(4), 'little')  # in this case, always 2


class FAT:
    def __init__(self, Dbr):
        self.FAT1Offset = Dbr.NumberOfReservedSector * Dbr.sizeofSector
        self.FAT2Offset = Dbr.SectorPerFAT * Dbr.sizeofSector + self.FAT1Offset
        self.RootDirOffset = (Dbr.NumberOfReservedSector + Dbr.SectorPerFAT * 2) * Dbr.sizeofSector
        self.sizeofDir = 32
        self.sizeofCluster = Dbr.sizeofSector * Dbr.SectorPerCluster
        self.NumberOfDirInCluster = int(self.sizeofCluster / self.sizeofDir)
        self.AvailableClusterNumberInFAT = int(Dbr.SectorPerFAT * Dbr.sizeofSector / 4) - 2


file = open('fat32d.img', 'rb+')
# Assert this FS has 2 FAT
dbr = DBR(file)
fat = FAT(dbr)
curDir = 0x2
curFullDir = '/'
print(dbr.__dict__)
print(fat.__dict__)


class DIR:
    def __init__(self, cluster, offset):
        dirBegin = cluster[offset:]
        self.AttrByte = dirBegin[0x0B]
        '''Attribute - a bitvector. Bit 0: read only. Bit 1: hidden.
        Bit 2: system file. Bit 3: volume label. Bit 4: subdirectory.
        Bit 5: archive. Bits 6-7: unused.'''
        if self.AttrByte != 0x0F:
            # Short Filename Format
            self.ShortFileName = dirBegin[0x00:0x08]
            self.ShortFileExt = dirBegin[0x08:0x0B]
            self.CreateMilli = dirBegin[0x0D:0x0E]
            self.CreateTime = dirBegin[0x0E:0x10]
            self.CreateDate = dirBegin[0x10:0x12]
            self.LastAccessDate = dirBegin[0x12:0x14]
            self.LastModifiedTime = dirBegin[0x16:0x18]
            self.LastModifiedDate = dirBegin[0x18:0x1A]
            self.FirstClusterHigh = dirBegin[0x14:0x16]
            self.FirstClusterLow = dirBegin[0x1A:0x1C]
            self.FileSize = int.from_bytes(dirBegin[0x1C:0x20], 'little')
            if self.ShortFileName[0] != 0x00:
                self.ShortFileName = [chr(x) for x in self.ShortFileName if x != 0x20]
                self.ShortFileExt = [chr(x) for x in self.ShortFileExt if x != 0x20 and x != 0x00]
        else:
            self.LongAttr = dirBegin[0x0]
            self.LoneFileName = []
            for i in range(1, 10, 2):
                self.LoneFileName.append(dirBegin[i])
            for i in range(14, 25, 2):
                self.LoneFileName.append(dirBegin[i])
            for i in range(28, 31, 2):
                self.LoneFileName.append(dirBegin[i])
            self.LoneFileName = [chr(x) for x in self.LoneFileName if x != 0xFF and x != 0x00]


def findAvailableClusterNumber():
    for i in range(2, fat.AvailableClusterNumberInFAT):
        content = getNextClusterNumber(i)
        if content == 0x00000000:
            return i
    raise Exception('Sorry, this file system has no more space!')


def getNextClusterNumber(curClusterNumber):
    file.seek(fat.FAT1Offset + curClusterNumber * 4)
    return int.from_bytes(file.read(4), 'little')


def getDirList(clusterNumber):
    file.seek(fat.RootDirOffset + (clusterNumber - dbr.ClusterNumberOfRootDir) * fat.sizeofCluster)
    cluster = file.read(fat.sizeofCluster)
    dirList = []
    while True:
        flag = True
        for i in range(fat.NumberOfDirInCluster):
            cur = DIR(cluster, i * fat.sizeofDir)
            if cur.AttrByte != 0x0F and cur.ShortFileName[0] == 0x00:
                flag = False
                break
            if (cur.AttrByte == 0x0f and cur.LongAttr == 0xE5) \
                    or (cur.AttrByte != 0x0f and cur.ShortFileName[0] == 0xE5):
                continue
            dirList.append(cur)
        if flag is False:
            break
        clusterNumber = getNextClusterNumber(clusterNumber)
        if 0x2 <= clusterNumber <= 0xFFFFFEF:
            file.seek(fat.RootDirOffset + (clusterNumber - dbr.ClusterNumberOfRootDir) * fat.sizeofCluster)
            cluster = file.read(fat.sizeofCluster)
        else:
            break
    return dirList


def bytes2TimeMonthDayYear(tim, date):
    tim = int.from_bytes(tim, 'little')
    date = int.from_bytes(date, 'little')
    second = (tim << 1) & 0x3f
    minute = (tim >> 5) & 0x3f
    hour = tim >> 11
    day = date & 0x1f
    month = (date >> 5) & 0xf
    year = (date >> 9) + 1980
    monthName = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    return '{:0>2d}:{:0>2d}:{:0>2d}    {}  {:>2d}  {:>4d}' \
        .format(hour, minute, second, monthName[month - 1], day, year)


def printComplexList(dirList):
    longName = ''
    nameList = []
    for di in dirList:
        if di.AttrByte == 0x0F:
            # Long names are successive
            longName = ''.join(di.LoneFileName) + longName
        elif di.AttrByte & 0x08:
            # Volume label
            continue
        elif di.AttrByte & 0x10:
            # subdirectory
            if len(longName):
                nameList.append('{:08b} '.format(di.AttrByte)
                                + bytes2TimeMonthDayYear(di.CreateTime, di.CreateDate)
                                + ' {:>10d}  '.format(di.FileSize) + '\033[1;32;41m' + longName + '\033[0m')
                longName = ''
            else:
                if len(di.ShortFileExt) == 0:
                    nameList.append('{:08b} '.format(di.AttrByte)
                                    + bytes2TimeMonthDayYear(di.CreateTime, di.CreateDate)
                                    + ' {:>10d}  '.format(di.FileSize)
                                    + '\033[1;32;41m' + ''.join(di.ShortFileName) + '\033[0m')
                else:
                    nameList.append('{:08b} '.format(di.AttrByte)
                                    + bytes2TimeMonthDayYear(di.CreateTime, di.CreateDate)
                                    + ' {:>10d}  '.format(di.FileSize)
                                    + '\033[1;32;41m' + ''.join(di.ShortFileName) + '.' + ''.join(
                        di.ShortFileExt) + '\033[0m')
        elif di.AttrByte & 0x20:
            # archive
            if len(longName):
                nameList.append('{:08b} '.format(di.AttrByte)
                                + bytes2TimeMonthDayYear(di.CreateTime, di.CreateDate)
                                + ' {:>10d}  '.format(di.FileSize) + longName)
                longName = ''
            else:
                nameList.append('{:08b} '.format(di.AttrByte)
                                + bytes2TimeMonthDayYear(di.CreateTime, di.CreateDate)
                                + ' {:>10d}  '.format(di.FileSize)
                                + ''.join(di.ShortFileName) + '.' + ''.join(di.ShortFileExt))
    for name in nameList:
        print(name)


def printList(dirList):
    longName = ''
    nameList = []
    for di in dirList:
        if di.AttrByte == 0x0F:
            # Long names are successive
            longName = ''.join(di.LoneFileName) + longName
        elif di.AttrByte & 0x08:
            # Volume label
            continue
        elif di.AttrByte & 0x10:
            # subdirectory
            if len(longName):
                nameList.append('\033[1;32;41m' + longName + '\033[0m')
                longName = ''
            else:
                assert longName == ''
                if len(di.ShortFileExt) == 0:
                    nameList.append('\033[1;32;41m' + ''.join(di.ShortFileName) + '\033[0m')
                else:
                    nameList.append(
                        '\033[1;32;41m' + ''.join(di.ShortFileName) + '.' + ''.join(di.ShortFileExt) + '\033[0m')
        elif di.AttrByte & 0x20:
            # archive
            if len(longName):
                nameList.append(longName)
                longName = ''
            else:
                nameList.append(''.join(di.ShortFileName) + '.' + ''.join(di.ShortFileExt))
    pagedList = [nameList[i:i + 10] for i in range(0, len(nameList), 10)]
    for _ in pagedList:
        print('\t'.join(_))


def getDirOneStep(curPos, dirName):
    dirList = getDirList(curPos)
    longName = ''
    for di in dirList:
        if di.AttrByte == 0x0F:
            longName = ''.join(di.LoneFileName) + longName
        elif di.AttrByte & 0x10:
            if len(longName):
                if longName == dirName:
                    ans = int.from_bytes(di.FirstClusterHigh, 'little')
                    ans = (ans << 16) + int.from_bytes(di.FirstClusterLow, 'little')
                    return ans
                longName = ''
            else:
                if len(di.ShortFileExt) == 0:
                    if ''.join(di.ShortFileName) == dirName:
                        ans = int.from_bytes(di.FirstClusterHigh, 'little')
                        ans = (ans << 16) + int.from_bytes(di.FirstClusterLow, 'little')
                        return ans
                else:
                    if ''.join(di.ShortFileName) + '.' + ''.join(di.ShortFileExt) == dirName:
                        ans = int.from_bytes(di.FirstClusterHigh, 'little')
                        ans = (ans << 16) + int.from_bytes(di.FirstClusterLow, 'little')
                        return ans
        elif di.AttrByte & 0x20:
            longName = ''
    raise Exception('Illegal directory!')


def changeDir(commandDir):
    global curDir, curFullDir
    if commandDir.startswith('/'):
        curDir = 0x2
        curFullDir = '/'
    dirList = commandDir.split('/')
    for d in dirList:
        curDir = getDirOneStep(curDir, d)
        if d == '.':
            pass
        elif d == '..':
            if curFullDir.count('/') == 1:
                curFullDir = '/'
            else:
                curFullDir = curFullDir[:curFullDir.rfind('/')]
        else:
            if curFullDir.endswith('/'):
                curFullDir = curFullDir + d
            else:
                curFullDir = curFullDir + '/' + d
    if curDir == 0:
        curDir = 2
        curFullDir = '/'


def makeShortDir(dirName):
    global curDir
    clusterNumber = curDir
    file.seek(fat.RootDirOffset + (clusterNumber - dbr.ClusterNumberOfRootDir) * fat.sizeofCluster)
    cluster = file.read(fat.sizeofCluster)
    while True:
        for i in range(fat.NumberOfDirInCluster):
            cur = DIR(cluster, i * fat.sizeofDir)
            if cur.AttrByte != 0x0F and cur.ShortFileName[0] == 0x00:
                baseOffset = fat.RootDirOffset + (
                        clusterNumber - dbr.ClusterNumberOfRootDir) * fat.sizeofCluster + i * fat.sizeofDir
                name = bytes(dirName, encoding='utf-8')
                for _ in range(8 - len(name)):
                    name = name + 0x20.to_bytes(length=1, byteorder='little')
                file.seek(baseOffset + 0x00)
                file.write(name)
                attr = 0x10.to_bytes(length=1, byteorder='little')
                file.seek(baseOffset + 0x0B)
                file.write(attr)
                size = 0x00.to_bytes(length=4, byteorder='little')
                file.seek(baseOffset + 0x1C)
                file.write(size)
                t = time.localtime()
                year, month, day, hour, minute, second = t[:6]
                year = (year - 1980) << 9
                month = int(month) << 5
                day = int(day)
                hour = int(hour) << 11
                minute = int(minute) << 5
                second = int(second // 2)
                ti = (hour + minute + second).to_bytes(2, 'little')
                date = (year + month + day).to_bytes(2, 'little')
                file.seek(baseOffset + 0x0E)
                file.write(ti)
                file.seek(baseOffset + 0x10)
                file.write(date)
                newDir = findAvailableClusterNumber()
                file.seek(fat.FAT1Offset + newDir * 4)
                file.write(b'0x0FFFFFFF')
                newDir = newDir.to_bytes(4, 'little')
                low = newDir[:2]
                high = newDir[2:]
                file.seek(baseOffset + 0x14)
                file.write(high)
                file.seek(baseOffset + 0x1A)
                file.write(low)
                return
        temp = clusterNumber
        clusterNumber = getNextClusterNumber(clusterNumber)
        if 0x2 <= clusterNumber <= 0xFFFFFEF:
            file.seek(fat.RootDirOffset + (clusterNumber - dbr.ClusterNumberOfRootDir) * fat.sizeofCluster)
            cluster = file.read(fat.sizeofCluster)
        elif 0x0FFFFFF8 <= clusterNumber <= 0x0FFFFFFF:
            # Reach the end of this directory and the end of this cluster at the same time
            file.seek(fat.FAT1Offset + temp * 4)
            newDir = findAvailableClusterNumber()
            file.write(newDir.to_bytes(length=4, byteorder='little', signed=False))
            file.seek(fat.FAT1Offset + newDir * 4)
            file.write(b'0x0FFFFFFF')
        else:
            break


def makeDir(dirName):
    if len(dirName) <= 8:
        makeShortDir(dirName)


def execute(command):
    if command.strip() == '':
        return
    if command == 'exit' or command == 'quit':
        file.close()
        exit()
    command = command.split()
    if command[0] == 'ls':
        dirList = getDirList(curDir)
        if '-l' in command:
            printComplexList(dirList)
        else:
            printList(dirList)
    elif command[0] == 'pwd' and len(command) == 1:
        print(curFullDir)
    elif command[0] == 'cd':
        changeDir(command[1])
    elif command[0] == 'mkdir':
        makeDir(command[1])


if __name__ == '__main__':
    print("**************************** Welcome to FAT32 ****************************")
    while True:
        cmd = input("[iABF@FAT32] » ")
        cmd = cmd.split(';')
        for cm in cmd:
            execute(cm)
