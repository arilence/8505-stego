import os, struct, sys, argparser
from dcimage import StegoImage

if __name__ == "__main__":
    stego = StegoImage()

    if (len(sys.argv) == 4):
        carrierPath = sys.argv[1]
        secretPath = sys.argv[2]
        outputPath = sys.argv[3]

        # Check if carrier file and secret file exist
        if (not os.path.exists(carrierPath) and not os.path.exists(secretPath)):
            print("✖ Both files must be valid.")
            sys.exit(1)

        # Check if hidden file can fit into carrier image
        carrierSize = os.stat(carrierPath).st_size
        secretSize = os.stat(secretPath).st_size
        if ((secretSize * 8) + 264 >= carrierSize - 54):
            print("✖ Secret file will not fit within the carrier.")
            sys.exit(1)

        print("Hiding Data...")
        newCarrierImage = stego.hideSecret(carrierPath, secretPath, outputPath)

    if (len(sys.argv) == 2):
        encryptedFilePath = sys.argv[1]

        # Check if encrypted file exists
        if (not os.path.exists(encryptedFilePath)):
            print("✖ Both files must be valid.")
            sys.exit(1)

        print("Retrieving Data...")
        secretFile = stego.showSecret(encryptedFilePath)
