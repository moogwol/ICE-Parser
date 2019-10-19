import sys
from PyQt5.QtWidgets import QApplication

from read_write_classes import (OpenFileDialog, TodaysDate, RelevantData,
                                RowContainer, CSVData, Row, ExcelWriter)

app = QApplication(sys.argv)

# Open file dialog to allow user to select which csv file they want
# to extract data from
dialog = OpenFileDialog()

# Get today's date
td = TodaysDate()
today = td.today

# Convert the csv file into a list object
all_data_obj = []
try:
    all_data_obj = CSVData(dialog.filename)
except FileNotFoundError:
    err = ErrorMessage('Incorrect or no file chosen.')

# Create an object that will retrieve only the relevant data
rd = RelevantData(all_data_obj)
rd.get_relevant_data()
relevant_data_list = rd.relevant_data

# create an instance of RowContainer and fill it with Row objects
row_container = RowContainer()
for row in relevant_data_list:
    row_obj = Row(row)
    if row_obj.date_object >= today:
        row_container.append_to_row_list(row_obj)

# Write the data to Excel
writer = ExcelWriter(row_container)
writer.write_data()

sys.exit((app.exec_()))



