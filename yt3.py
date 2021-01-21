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

    # run method gets called when we start the thread
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
        # Here we are telling to call download method when
        # someone clicks on the pushButton.
        self.pushButton.clicked.connect(self.download)
        self.yt_thread = CloneThread()  # This is the thread object
        # Connect the signal from the thread to the finished method
        self.yt_thread.signal.connect(self.finished)

    def download(self):
        self.yt_thread.yt_url = self.lineEdit.text()  # Get the git URL
        self.pushButton.setEnabled(False)  # Disables the pushButton
        self.textEdit.setText("Starting Download.")  # Updates the UI
        self.yt_thread.start()  # Finally starts the thread

    def finished(self, result):
        self.textEdit.setText("Downloaded at {0}".format(result))  # Show the output to the user
        self.pushButton.setEnabled(True)  # Enable the pushButton


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = ExampleApp()
    form.show()
    app.exec_()


if __name__ == '__main__':
    main()


