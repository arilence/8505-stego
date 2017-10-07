import os, struct, sys
from PIL import Image
from PIL.ImageQt import ImageQt
from dcimage import StegoImage
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from ui.mainwindow import Ui_MainWindow



class View(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setupUi(self)
        self.exitButton.clicked.connect(self.exitButtonPressed)
        self.carrierButton.clicked.connect(self.carrierButtonPressed)
        self.secretButton.clicked.connect(self.secretButtonPressed)

    def exitButtonPressed(self):
        sys.exit(0)
    def carrierButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if file:
            self.carrierEdit.setText(file)
            self.showThumbnail(file, self.carrierImage)


    def secretButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if file:
            self.secretEdit.setText(file,)
            self.showThumbnail(file, self.secretImage)

    def showThumbnail(self, file, label):
        thumb = Image.open(file)
        thumb = thumb.convert("RGBA")
        size = 200, 200
        thumb.thumbnail(size, Image.ANTIALIAS)
        qim = ImageQt(thumb)
        label.setPixmap(QPixmap.fromImage(qim))



app = QApplication(sys.argv)
widget = View()
widget.show()
sys.exit(app.exec_())




"""
if __name__ == "__main__":


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
"""
