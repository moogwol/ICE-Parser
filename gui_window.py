import sys
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout,
                             QRadioButton, QFileDialog, QMessageBox,
                             QPushButton, QLabel)
from read_write_classes import (TodaysDate, RelevantData,
                                RowContainer, CSVData, Row, ExcelWriter)

from broker_classes import BrokerAugust, BrokerAdatmtr

class OpenFileDialog(QFileDialog):
    """Open a file dialog which lets the user select a file.
     The file path is then stored"""
    def __init__(self):
        super().__init__()
        self.filename = self.get_filename()

    def get_filename(self):
        filename = QFileDialog.getOpenFileName()
        return filename[0]

class MainWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle('ICE Parser')
        self.setGeometry(200, 300, 300, 200)
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.current_broker = BrokerAugust()
        self.current_broker_name = 'August'
        self.welcome_label()
        self.radio_buttons()
        self.file_search()
        self.broker = None
        self.show()

    def welcome_label(self):
        label1 = QLabel('Welcome to ICE Parser')
        label2 = QLabel('Please select a broker and import your csv file')
        self.layout.addWidget(label1)
        self.layout.addWidget(label2)


    def radio_buttons(self):
        # Add a radio button for each broker here

        radio_button1 = QRadioButton('August') # Broker name
        radio_button1.broker = BrokerAugust() # tells the app which broker class to use
        radio_button1.setChecked(True)
        radio_button1.toggled.connect(self.on_toggled)
        self.layout.addWidget(radio_button1)

        radio_button2 = QRadioButton('Adatmtr')
        radio_button2.broker = BrokerAdatmtr()
        radio_button2.toggled.connect(self.on_toggled)
        self.layout.addWidget(radio_button2)

    def file_search(self):
        # A button which opens a file dialog to import a CSV file
        button = QPushButton('Import CSV')
        self.layout.addWidget(button)
        button.clicked.connect(self.on_pressed)

    def on_pressed(self):
        fd = OpenFileDialog()
        self.broker = fd.filename
        print(self.broker)
        self.read_data()

    def on_toggled(self):
        radio_button = self.sender()
        if radio_button.isChecked():
            self.current_broker = radio_button.broker
            self.current_broker_name = radio_button.text()
            print(self.current_broker_name)

    def read_data(self):
        td = TodaysDate()
        today = td.today

        print('reading data')
        # Convert the csv file into a list object
        all_data_obj = []
        try:
            all_data_obj = CSVData(self.broker)
        except FileNotFoundError:
            err = ErrorMessage('Incorrect or no file chosen.')

        # Create an object that will retrieve only the relevant data
        rd = RelevantData(all_data_obj)
        rd.get_relevant_data(self.current_broker)
        relevant_data_list = rd.relevant_data

        # create an instance of RowContainer and fill it with Row objects
        row_container = RowContainer()
        for row in relevant_data_list:
            row_obj = Row(row)
            if row_obj.date_object >= today:
                row_container.append_to_row_list(row_obj)
        # Write the data to Excel
        writer = ExcelWriter(row_container, self.current_broker_name)
        writer.write_data()

        sys.exit()


class ErrorMessage(QWidget):
    def __init__(self, msg, parent=None):
        super(ErrorMessage, self).__init__(parent)
        self.msg = msg
        self.set_up()

    def set_up(self):
        err_msg = QMessageBox.warning(self,
                                  'Error Occurred',
                                  self.msg,
                                  QMessageBox.Close,
                                  QMessageBox.Close)
        if err_msg == QMessageBox.Close:
            sys.exit()
        self.show()