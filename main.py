from PIL import Image
import itertools, os, struct, sys

# Lets design the header
# headerSize        = 2 bytes
# fileSize          = 8 bytes
# fileName          = 248 bytes
# would be nice to have a relative fileName size using the header size
class Header:
    def __init__(self, fileName, fileSize):
        self.fileName     = fileName
        self.fileSize     = fileSize

    def toBytes(self):
        packQuery = "hQ248s"
        return struct.pack(packQuery, 
                           0,
                           self.fileSize,
                           self.fileName.encode())

    @staticmethod
    def fromBytes(data):
        packQuery = "hQ248s"
        headerData = struct.unpack(packQuery, data[:2+8+254])
        fileSize   = headerData[1]
        fileName   = headerData[2].decode().strip("\x00")
        return Header(fileName, fileSize)

def encodeData(carrierImage, secretFile):
    carrierPixels = list(carrierImage.getdata())

    secretBytes = bytearray(secretFile.read())

    secretFileName = os.path.basename(secretFile.name)
    secretFileSize = os.fstat(secretFile.fileno()).st_size
    header = Header(secretFileName, secretFileSize)
    secretBytes = header.toBytes() + secretBytes

    for idx1, pixelList in enumerate(carrierPixels):

        if (idx1 < len(secretBytes)):
            r = (pixelList[0] & 0xFC) | ((secretBytes[idx1]) & 0x3)
            g = (pixelList[1] & 0xFC) | ((secretBytes[idx1]>>2) & 0x3)
            b = (pixelList[2] & 0xFC) | ((secretBytes[idx1]>>4) & 0x3)
            a = (pixelList[3] & 0xFC) | ((secretBytes[idx1]>>6) & 0x3)
            pixelList = (r,g,b,a)
            carrierPixels[idx1] = pixelList
        else:
            break

    newImage = Image.new(carrierImage.mode, carrierImage.size)
    newImage.putdata(carrierPixels)
        
    return newImage

def decodeData(carrierImage):
    carrierPixels = list(carrierImage.getdata())

    secretBytes = []

    for idx1, pixelList in enumerate(carrierPixels):

        if (idx1 < len(carrierPixels)):
            r = (pixelList[0] & 0x3)
            g = ((pixelList[1] & 0x3)<<2)
            b = ((pixelList[2] & 0x3)<<4)
            a = ((pixelList[3] & 0x3)<<6)
            
            secretBytes += struct.pack("B", r + g + b + a)
        else:
            break
    secretBytes = bytearray(secretBytes)

    header = Header.fromBytes(secretBytes)

    secretFile = open("./" + header.fileName, 'wb')
    secretFile.write(secretBytes[264:header.fileSize+264])

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
