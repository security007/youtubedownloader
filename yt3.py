#!/usr/bin/python3

import sys
import pytube
from PyQt5 import QtWidgets
from PyQt5.QtCore import QThread, pyqtSignal

from mainwindow import Ui_MainWindow


class CloneThread(QThread):
    signal = pyqtSignal('PyQt_PyObject')

    def __init__(self):
        QThread.__init__(self)
        self.yt_url = ""

   
    def run(self):
        frm = "18"
        url = pytube.YouTube(self.yt_url)
        video = url.streams.get_by_itag('135')
        video.download()
        self.signal.emit(video.download())


class ExampleApp(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):
        super(ExampleApp, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.setText("Download")
       
        self.pushButton.clicked.connect(self.download)
        self.yt_thread = CloneThread()
        
        self.yt_thread.signal.connect(self.finished)

    def download(self):
        self.yt_thread.yt_url = self.lineEdit.text()  
        self.pushButton.setEnabled(False)  
        self.textEdit.setText("Starting Download.") 
        self.yt_thread.start()  

    def finished(self, result):
        self.textEdit.setText("Downloaded at {0}".format(result)) 
        self.pushButton.setEnabled(True)  


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()


