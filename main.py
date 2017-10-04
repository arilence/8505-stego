import os, struct, sys
from dcimage import StegoImage

if __name__ == "__main__":
    stego = StegoImage()

    if (len(sys.argv) == 4):
        print("Hiding Data...")
        newCarrierImage = stego.hideSecret(sys.argv[1], sys.argv[2], sys.argv[3])

    if (len(sys.argv) == 2):
        print("Retrieving Data...")
        secretFile = stego.showSecret(sys.argv[1])
