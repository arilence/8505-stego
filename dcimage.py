from PIL import Image
from dcutils import Encryptor, Encoder
import itertools, os, struct, sys

class Header:
    fileSizeBytes = 8
    fileNameBytes = 254

    def __init__(self, fileName, fileSize):
        self.fileName     = fileName
        self.fileSize     = fileSize

    def toBytes(self):
        packQuery = "hQ248s"
        something = struct.pack(packQuery, 
                           0,
                           self.fileSize,
                           self.fileName.encode('utf-8'))
        return something

    @staticmethod
    def fromBytes(data):
        packQuery = "hQ248s"
        headerData = struct.unpack(packQuery, data[:2+Header.fileSizeBytes+Header.fileNameBytes])
        fileSize   = headerData[1]
        fileName   = headerData[2].decode('utf-8').strip("\x00")
        return Header(fileName, fileSize)

class StegoImage:
    """
     * Retrieves a list of bits from a single byte
    """
    def access_bit(self, data, num):
        base = int(num/8)
        shift = num % 8
        return (data[base] & (1<<shift)) >> shift

    """
     * Converts an array of bytes to an array of bits
     * bytearray -> bitarray
    """
    def byteArrayToBitArray(self, bytess):
        data = bytearray(bytess)
        newData = [self.access_bit(data,i) for i in range(len(data)*8)]
        return newData

    """
     * Converts an array of bits to an array of bytes
     * bitarray -> bytearray
    """
    def bitArrayToByteArray(self, bits):
        bytes = [sum([byte[b] << b for b in range(0,8)])
                    for byte in zip(*(iter(bits),) * 8)
                ]
        return bytes

    """
     * Uses an image to hide encrypted secret data within it.
     * @param   carrierImagePath    location to carrier image on disk
     * @param   secretFilePath      location to secret file on disk
     * @param   outputFilePath      location where the new output file will be saved
    """
    def hideSecret(self, carrierImagePath, secretFilePath, outputFilePath):
        carrierImage = Image.open(carrierImagePath)
        secretFile = open(secretFilePath, 'rb')

        encryptor = Encryptor()
        encoder = Encoder()

        carrierPixels = list(carrierImage.getdata())
        secretFileName = os.path.basename(secretFile.name)
        secretFileSize = os.fstat(secretFile.fileno()).st_size

        header = Header(secretFileName, secretFileSize)
        secretBytes = header.toBytes() + bytearray(secretFile.read())
        secretBytes = encryptor.encryptData(secretBytes)
        secretBits = self.byteArrayToBitArray(secretBytes)

        carrierPixels = encoder.encode(carrierPixels, secretBits)
        newImage = Image.new(carrierImage.mode, carrierImage.size)
        newImage.putdata(carrierPixels)
        newImage.save(outputFilePath)

    """
     * Uses an image to retrieve encrypted secret data within it.
     * The secret filename is stored within the carrier, and will be
     * saved to disk as the stored name within the same directory.
     * @param   carrierImagePath    location to carrier image on disk
    """
    def showSecret(self, carrierImagePath):
        carrierImage = Image.open(carrierImagePath)
        encryptor = Encryptor()
        encoder = Encoder()

        carrierPixels = list(carrierImage.getdata())

        secretBits = encoder.decode(carrierPixels)
        secretBytes = self.bitArrayToByteArray(secretBits)
        decryptedBytes = encryptor.decryptData(bytes(secretBytes))
        header = Header.fromBytes(decryptedBytes)
        secretFile = open("./" + header.fileName, 'wb')
        secretFile.write(bytearray(decryptedBytes)[264:header.fileSize+264])

