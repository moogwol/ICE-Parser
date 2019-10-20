import sys
from PyQt5.QtWidgets import QApplication
from gui_window import MainWindow, OpenFileDialog, ErrorMessage

from read_write_classes import (TodaysDate, RelevantData,
                                RowContainer, CSVData, Row, ExcelWriter)
app = QApplication(sys.argv)


# Initiate the GUI
gui = MainWindow()


sys.exit((app.exec_()))



