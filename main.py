from PIL import Image
import itertools, os, struct, sys

class Header:
    def __init__(self, fileName, fileSize):
        self.fileName     = fileName
        self.fileSize     = fileSize

    def toBytes(self):
        packQuery = "hQ248s"
        something = struct.pack(packQuery, 
                           0,
                           self.fileSize,
                           self.fileName.encode('utf-8'))
        print(something)
        return something

    @staticmethod
    def fromBytes(data):
        packQuery = "hQ248s"
        headerData = struct.unpack(packQuery, data[:2+8+254])
        print(headerData)
        fileSize   = headerData[1]
        fileName   = headerData[2].decode('utf-8').strip("\x00")
        return Header(fileName, fileSize)

# get bits from a byte
def access_bit(data, num):
    base = int(num/8)
    shift = num % 8
    return (data[base] & (1<<shift)) >> shift

# returns a list of bits
def byteArrayToBitArray(bytess):
    data = bytearray(bytess)
    newData = [access_bit(data,i) for i in range(len(data)*8)]
    return newData

# returns a list of bytes
def bitArrayToByteArray(bits):
    bytes = [sum([byte[b] << b for b in range(0,8)])
                for byte in zip(*(iter(bits),) * 8)
            ]
    return bytes

def encodeData(carrierImage, secretFile):
    carrierPixels = list(carrierImage.getdata())

    secretFileName = os.path.basename(secretFile.name)
    secretFileSize = os.fstat(secretFile.fileno()).st_size

    header = Header(secretFileName, secretFileSize)

    secretBytes = header.toBytes() + bytearray(secretBytes.read())
    secretBits = byteArrayToBitArray(secretBytes)

    # Super hacky..
    # Image data comes in a tuple (which is immutable). To modify, I keep 
    # track of the three values in the tuple and make a new tuple to
    # override the previous one LOL. This section also causes the most lag.
    i = 0
    for idx1, pixelList in enumerate(carrierPixels):
        tempPixelList = []
        for idx2, value in enumerate(pixelList):
            value = value & 0xFE
            if (i < len(secretBits)):
                value = value | secretBits[i]
            i = i + 1
            tempPixelList.append(value)
        if (len(tempPixelList) == 4):
            pixelList = (tempPixelList[0], tempPixelList[1], tempPixelList[2], tempPixelList[3])
        else:
            pixelList = (tempPixelList[0], tempPixelList[1], tempPixelList[2])
        carrierPixels[idx1] = pixelList

    newImage = Image.new(carrierImage.mode, carrierImage.size)
    newImage.putdata(carrierPixels)
        
    return newImage

def decodeData(carrierImage):
    carrierPixels = list(carrierImage.getdata())
    secretBits = []

    i = 0
    for pixelList in carrierPixels:
        for value in pixelList:
            secretBits.append(value & 0x1)
            i = i + 1

    secretBytes = bitArrayToByteArray(secretBits)
    header = Header.fromBytes(bytearray(secretBytes))
    secretFile = open("./" + header.fileName, 'wb')
    secretFile.write(bytearray(secretBytes)[264:header.fileSize+264])

if __name__ == "__main__":
    if (len(sys.argv) == 4):
        print("Encoding")
        carrierImage = Image.open(sys.argv[1])
        secretFile = open(sys.argv[2], 'rb')
        newCarrierImage = encodeData(carrierImage, secretFile)
        newCarrierImage.save(sys.argv[3])

    if (len(sys.argv) == 2):
        print("Decoding")
        carrierImage = Image.open(sys.argv[1])
        secretFile = decodeData(carrierImage)
