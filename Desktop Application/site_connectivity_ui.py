#!/usr/bin/env python3
"""UI for Site Connectivity Checking Program
   Built with PyQt5 UI to check a single URL and enable user to choose running the 
   program as a background process and send notification when status changed."""

import sys
from datetime import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore
from PyQt5.QtCore import Qt, QRect, QObject, QThread
from site_connectivity_check_with_ui import *


class Worker(QObject):
    finished = QtCore.pyqtSignal()
    
    def run_regular_check(self, url, interval ):
        self.url = url
        self.interval = interval
        self.run_regular_check= regular_check(url, interval)
        self.finished.emit()


class Thread(QThread):
    def __init__(self, parent=None):
        super(QThread, self).__init__(parent)
        
    def start(self):
        QThread.start(self)

    def run(self):
        while True:
            QThread.run(self)
            global stop_thread 
            # kill the thread
            if stop_thread:
                break
    

class MainWindow(QMainWindow):
    '''Main Window'''

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.setWindowTitle("Site Connectivity Check")
        self.setFixedSize(500, 300)
        self.generalLayout = QVBoxLayout()

        # Set the central widget
        self._centralWidget = QWidget(self)
        self.setCentralWidget(self._centralWidget)
        self._centralWidget.setLayout(self.generalLayout)

        # calling methods
        self._createUrlDisplay()
        self._createIntervalDisplay()
        self._createStatusDisplay()
        self._createButtons()
        self._createBackgroundCheck()

        self.show()

        
    def _createUrlDisplay(self):
        ''' Create the URL display for user's input'''
        self.urlBoxLayout = QHBoxLayout()
        # add label and text box 
        self.urlLabel = QLabel("URL:")
        self.urlBoxLayout.addWidget(self.urlLabel)
        self.urlBoxLayout.addWidget(self.urlText)
        # Add display to general layout
        self.generalLayout.addLayout(self.urlBoxLayout)


    def _createIntervalDisplay(self):
        '''Create the display for Interval Time check'''
        self.interval = QHBoxLayout()
        self.intervalLabel = QLabel("Interval Checktime (Optional - in second):")
        self.intervalText = QLineEdit()
        self.interval.addWidget(self.intervalLabel)
        self.interval.addWidget(self.intervalText)
        self.generalLayout.addLayout(self.interval)


    def _createStatusDisplay(self):
        '''Create the URL status display'''
        self.statBoxLayout = QHBoxLayout()
        self.statLabel = QLabel("Status")
        self.statText = QLineEdit()
        self.statText.setReadOnly(True)
        self.statBoxLayout.addWidget(self.statLabel)
        self.statBoxLayout.addWidget(self.statText)
        self.generalLayout.addLayout(self.statBoxLayout)
        
    
    def _createButtons(self):
        '''Create buttons'''
        self.buttonLayout = QHBoxLayout()

        button_start = QPushButton('Start', self)
        button_start.setFixedSize(90, 40)
        button_start.clicked.connect(self._start_process)
        self.buttonLayout.addWidget(button_start)

        button_stop = QPushButton('Stop', self)
        button_stop.setFixedSize(90, 40)
        button_stop.clicked.connect(self._stop_process)
        self.buttonLayout.addWidget(button_stop)
    
        # Button to clear the inputs
        button_clear = QPushButton('Clear', self)
        button_clear.setFixedSize(140, 40)
        button_clear.clicked.connect(self._clearDisplay)
        self.buttonLayout.addWidget(button_clear)

        # add to parent layout
        self.generalLayout.addLayout(self.buttonLayout)


    def _createBackgroundCheck(self):
        '''Create button for Background Check'''
        self.buttonRegular = QHBoxLayout()
        button_regular_check = QPushButton('Keep checking in background. Send alert when URL can be connected.')
        button_regular_check.clicked.connect(self._regular_check)
        self.buttonRegular.addWidget(button_regular_check)
        self.generalLayout.addLayout(self.buttonRegular)


    def _start_process(self):
        url = self.urlText.text()
        if url:
            try: 
                check_valid_url(url)
                status = start_process(url)
                return self.statText.setText(status)
            except Exception:  
                QMessageBox.about(self, 'Error', 'Not a valid URL.')
        else:
            QMessageBox.about(self, 'Error','Please enter the URL.')


    def _stop_process(self):
        url = self.urlText.text()
        if url:
            stop_process(url)
        else:
            stop_process()


    def _regular_check(self):
        url = self.urlText.text()
        interval = self.intervalText.text()
        if url:
            try:
                check_valid_url(url)
            except Exception:
                QMessageBox.about(self, 'Error', 'Not a valid url.')
        if interval:
            try:
                interval_num = int(interval)
                # Start a thread
                thread = Thread() 
                obj = Worker()
                obj.moveToThread(thread)
                obj.finished.connect(thread.quit)
                thread.started.connect(obj.run_regular_check)
                thread.start()   
            except ValueError:
                QMessageBox.about(self, 'Error','Input can only be a number')
        else:
            QMessageBox.about(self, 'Error','Interval Check is required for this task.')


    def _clearDisplay(self):
        """Clear the display."""
        # we all total 3 text fields 
        text_fields = [self.urlText, self.intervalText, self.statText]
        for i in range(len(text_fields)):
            text_fields[i].setText('')


# Automatically kill the thread in background 
# after 5 days 
def schedule_kill_thread():
    global start_time
    endtime = datetime.now()
    if endtime.day - 5 > start_time.day:
        stop_thread = False
    

def main():
    start_time = start_time = datetime.now()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
    app.deleteLater()   
    schedule_kill_thread()     


if __name__ == '__main__':
    main()