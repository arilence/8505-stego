import os, struct, sys
from dcimage import StegoImage

if __name__ == "__main__":
    carrierPath = sys.argv[1]
    secretPath = sys.argv[2]
    outputPath = sys.argv[3]

    stego = StegoImage()

    # TODO: Show helper function with --help

    # Check if carrier file and secret file exist
    if (os.path.exists(carrierPath) and os.path.exists(secretPath)):
        print("✓ Both files exist")
    else:
        print("✖ Both files must be valid")
        sys.exit(1)

    # TODO: Check if hidden file can fit into carrier image


    if (len(sys.argv) == 4):
        print("Hiding Data...")
        newCarrierImage = stego.hideSecret(sys.argv[1], sys.argv[2], sys.argv[3])

    if (len(sys.argv) == 2):
        print("Retrieving Data...")
        secretFile = stego.showSecret(sys.argv[1])
