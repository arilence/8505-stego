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
        self.carrierButton.clicked.connect(self.btn_sendMessagePressed)
        self.btn_startReceiver.clicked.connect(self.btn_startReceiverPressed)
        self.btn_clearMessages.clicked.connect(self.btn_clearMessagesPressed)

        self.controller.receiver.logSignal.connect(self.updateMessageLog)
        self.controller.sender.logSignal.connect(self.updateSendState)
"""



"""
if __name__ == "__main__":

    carrierPath = sys.argv[1]
    secretPath = sys.argv[2]
    outputPath = sys.argv[3]

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
"""
