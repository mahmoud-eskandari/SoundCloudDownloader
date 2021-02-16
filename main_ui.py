import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QProgressBar
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
import time 
from Handler import Handler 


# handler = Handler()

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Soundcloud Downloader'
        self.left = 250
        self.top = 250
        self.width = 600
        self.height = 150
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(500,20)
        self.textbox.setPlaceholderText("Past url of track here") 
        
        # Create a button in the window
        self.button = QPushButton('Download', self)
        self.button.move(20,70)
        self.button.resize(120,30)

        #BAR
        self.pbar = QProgressBar(self)
        # self.pbar.setGeometry(80, 140, 200, 25) 
        self.pbar.move(180,70)
        self.pbar.resize(200,30)

        # self.btn = QPushButton('Start', self) 
        # self.btn.move(40, 140) 
        # self.btn.clicked.connect(self.progress) 
        
        self.button.clicked.connect(self.on_start)
        self.show()
    
    @pyqtSlot()
    def on_start(self):
        textboxValue = self.textbox.text()
        Handler().getMp3Track(textboxValue,self.pbar,QApplication)
        # handler.getMp3Track("https://soundcloud.com/revealed-recordings/dj-st3v3-washint-free-download")

    def progress(self): 
        for i in range(101): 
            time.sleep(0.05) 
            self.pbar.setValue(i) 

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())