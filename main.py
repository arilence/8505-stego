"""---------------------------------------------------------------------------------------
--      SOURCE FILE:        main.py - main entry point of the application
--
--      PROGRAM:            steganography encrypter
--
--      FUNCTIONS:          __init__(self, parent=none)
--                          exitButtonPressed(self)
--                          carrierButtonPressed(self)
--                          SecretButtonPressed(self)
--                          encodeFileButtonPressed(self)
--                          encodeButtonPressed(self)
--                          decodeButtonPressed(self)
--                          showDialog(self, message)
--                          showError(self, errorMessage)
--                          showThumbnail(self, file, label)
--                          signalReceived(self)
--                          errorSignal(self)
--                          getPassword(self)
--
--
--      DATE:               October 7, 2017
--
--      DESIGNERS:          Anthony Smith, Thomas Yu
--
--      PROGRAMMERS:        Anthony Smith, Thomas Yu
--
--      NOTES:
--      This program is the main entry point for a steganography and encryption program
--      that is able to hide and decrypt a secret file in a bmp/png image.
---------------------------------------------------------------------------------------"""

import os, struct, sys
from PIL import Image
from PIL.ImageQt import ImageQt
from dcimage import StegoImage
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
from ui.mainwindow import Ui_MainWindow

#UI Class
class View(QMainWindow, Ui_MainWindow):

    #Constructor
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.stego = StegoImage()
        self.setupUi(self)
        self.exitButton.clicked.connect(self.exitButtonPressed)
        self.carrierButton.clicked.connect(self.carrierButtonPressed)
        self.secretButton.clicked.connect(self.secretButtonPressed)
        self.encodeFileButton.clicked.connect(self.encodeFileButtonPressed)
        self.encodeButton.clicked.connect(self.encodeButtonPressed)
        self.decodeButton.clicked.connect(self.decodeButtonPressed)
        self.stego.completeSignal.connect(self.signalReceived)
        self.stego.errorSignal.connect(self.errorSignal)

    #Exit button
    def exitButtonPressed(self):
        sys.exit(0)

    #Select carrier file button
    def carrierButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","png files (*.png);;bmp files (*.bmp)", options=options)
        if file:
            self.carrierEdit.setText(file)
            self.showThumbnail(file, self.carrierImage)

    #Select secret file button
    def secretButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if file:
            self.secretEdit.setText(file)

    #Select encoded file button
    def encodeFileButtonPressed(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
        if file:
            self.encodedEdit.setText(file)
            self.showThumbnail(file, self.encodedImage)

    #Encode button
    def encodeButtonPressed(self):
        carrierFilePath = self.carrierEdit.text()
        secretFilePath = self.secretEdit.text()
        secretFileName = os.path.basename(secretFilePath)
        carrierFileName = os.path.basename(carrierFilePath)
        outDirectory = os.getcwd() + '/out/' + carrierFileName
        if carrierFilePath and secretFilePath:
            # Check if hidden file can fit into carrier image
            carrierSize = os.stat(carrierFilePath).st_size
            secretSize = os.stat(secretFilePath).st_size

            if ((secretSize * 8) + 264 >= carrierSize - 54):
                self.showError("Carrier image is too small, or secret file is too small."
                + "Ensure that the carrier file is atleast 8 times larger than the secret file + 264 bytes")
                return
            print(secretFileName)
            print(carrierFileName)

            if not (carrierFileName.endswith('.bmp') or carrierFileName.endswith('png')):
                self.showError("unsupported file type")
                return

            password = self.getPassword()
            passwordByte= str.encode(password)
            newCarrierImage = self.stego.hideSecret(carrierFilePath, secretFilePath, outDirectory, passwordByte)

        else:
            self.showError("Please select a carrier and secret file")

    #Decode button
    def decodeButtonPressed(self):
        encodedFilePath = self.encodedEdit.text()
        encodedFileName = os.path.basename(encodedFilePath)
        if not (encodedFileName.endswith('.bmp') or encodedFileName.endswith('.png')):
            self.showError("unsupported file type")
            return
        if encodedFilePath:
            password = self.getPassword()
            passwordByte= str.encode(password)
            self.stego.showSecret(encodedFilePath, passwordByte)
        else:
            self.showError("Please select an encoded file")

    #Show and create dialog box
    def showDialog(self, message):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Information)

       msg.setText(message)
       msg.setWindowTitle("Alert")
       msg.setStandardButtons(QMessageBox.Ok)

       msg.exec_()

    #Show error dialog box
    def showError(self, errorMessage):
       msg = QMessageBox()
       msg.setIcon(QMessageBox.Warning)

       msg.setText("Uh oh, something went wrong...")
       msg.setWindowTitle("Alert")
       msg.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
       msg.setDetailedText(errorMessage)

       msg.exec_()

    #Show thumbnail image
    def showThumbnail(self, file, label):
        thumb = Image.open(file)
        thumb = thumb.convert("RGBA")
        size = 400, 600
        thumb.thumbnail(size, Image.ANTIALIAS)
        qim = ImageQt(thumb)
        label.setPixmap(QPixmap.fromImage(qim))

    #Task complete signal
    def signalReceived(self):
        self.showDialog("Task Complete")

    #Error signal
    def errorSignal(self, msg):
        self.showError(msg)

    #Get password dialog
    def getPassword(self):
        text, okPressed = QInputDialog.getText(self, "Get text","Enter Password:", QLineEdit.Normal, "")
        if okPressed and text != '':
            return text

app = QApplication(sys.argv)
widget = View()
widget.show()
sys.exit(app.exec_())
