import csv,sys
import datetime
from openpyxl import Workbook
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget, QMessageBox
from broker_classes import BrokerAugust




class CSVData:
    """Reads a csv file and store the data as a list"""
    def __init__(self, file):
        self.file = file
        self.data = self.read_data()

    def read_data(self):
        with open(self.file, 'r') as f:
            reader = csv.reader(f)
            data = list(reader)
        return data


class RelevantData:
    """Takes an object containg a list and strips all of the irrelevant data"""
    def __init__(self, data_obj):
        self.data_obj = data_obj
        self.old_list = self.data_obj.data
        self.relevant_data = []

    def get_relevant_data(self, brkr):

        broker = brkr

        for row in self.old_list:

            description = row[broker.description].strip()
            name = row[broker.name].strip()
            symbol = row[broker.symbol].strip()
            date = row[broker.date].strip()
            put_call = row[broker.put_call].strip()
            strike = row[broker.strike].strip()

            self.relevant_data.append([description, name, symbol,
                                       date, put_call, strike])


class Row:

    """Models a row in Excel"""
    months_dict = {'01': {'month_code': 'F', 'call_code': 'A', 'put_code': 'M'},
                   '02': {'month_code': 'G', 'call_code': 'B', 'put_code': 'N'},
                   '03': {'month_code': 'H', 'call_code': 'C', 'put_code': 'O'},
                   '04': {'month_code': 'J', 'call_code': 'D', 'put_code': 'P'},
                   '05': {'month_code': 'K', 'call_code': 'E', 'put_code': 'Q'},
                   '06': {'month_code': 'M', 'call_code': 'F', 'put_code': 'R'},
                   '07': {'month_code': 'N', 'call_code': 'G', 'put_code': 'S'},
                   '08': {'month_code': 'Q', 'call_code': 'H', 'put_code': 'T'},
                   '09': {'month_code': 'U', 'call_code': 'I', 'put_code': 'U'},
                   '10': {'month_code': 'V', 'call_code': 'J', 'put_code': 'V'},
                   '11': {'month_code': 'X', 'call_code': 'K', 'put_code': 'W'},
                   '12': {'month_code': 'Z', 'call_code': 'L', 'put_code': 'X'},
                   '': {'month_code': None, 'call_code': None, 'put_code': None}
                   }

    def __init__(self, data_list):
        self.data_list = data_list
        self.description = self.data_list[0]
        self.name = self.data_list[1]
        self.symbol = self.data_list[2]
        self.date = self.data_list[3]
        self.call_put = self.data_list[4]
        self.strike = self.data_list[5]
        self.formatted_price = f"{float(self.strike):.2f}"
        self.year = self.date[2:4]
        self.month = self.date[4:6]
        self.day = self.date[6:]
        self.call_put_code = self.create_call_put_code()
        self.ice_option_code = self.create_ice_option_code()
        self.date_object = self.create_date_object()

    def create_month_code(self):
        """Takes a 2 digit month and outputs a code letter"""
        pass

    def create_call_put_code(self):
        """Takes a 2 digit month and outputs a code letter depending on
        whether the product is a call or a put"""
        if self.call_put == 'C':
            cp_code = self.months_dict[self.month]['call_code']
        elif self.call_put == 'P':
            cp_code = self.months_dict[self.month]['put_code']
        else:
            cp_code = None
        return cp_code

    def create_ice_option_code(self):
        """Takes symbol, year, put/call month code, strike price and day
        and generates an ICE option code for use in the ICE Excel plugin"""
        io_code = f"O:{self.symbol} {self.year}{self.call_put_code}" \
            f"{self.formatted_price}D{self.day}"
        return io_code

    def create_date_object(self):
        try:
            date_obj = datetime.datetime(int(self.date[:4]),
                                         int(self.date[4:6]),
                                         int(self.date[6:])).date()
            return date_obj
        except ValueError:
            date_obj = datetime.datetime(1876, 3, 26).date()
            return date_obj



class RowContainer:
    def __init__(self):
        """Takes a Row object and stores it in a list"""
        self.row_list = []

    def append_to_row_list(self, row_obj):
        self.row_list.append(row_obj)


class TodaysDate:
    """Gets today's date"""
    def __init__(self):
        self.today = datetime.datetime.now().date()


class ExcelWriter:
    """Writes a list of objects and their fields to an Excel file"""
    def __init__(self, list_obj, brkr_name):
        self.obj_list = list_obj.row_list
        self.dest_filename = f"{brkr_name}.xlsx"
        self.sheetname = 'ICE Codes'
        self.wb = Workbook()
        self.ws = self.wb.active
        self.headings = ['Description', 'Name', 'Symbol', 'Call/Put', 'Strike',
                         'Date','ICE Code']

    def write_data(self):
        """Gets a list of headings and appends them to the Excel worksheet.
        Then retrieves the relevant data from the RowContainer, formats
        it into a list representing an Excel row and appends each row to
         the worksheet"""
        self.ws.title = self.sheetname
        self.ws.append(self.headings)
        for obj in self.obj_list:
            row = [obj.description, obj.name, obj.symbol,
                   obj.call_put, obj.formatted_price,
                   obj.date_object, obj.ice_option_code]
            self.ws.append(row)
        self.wb.save(filename=self.dest_filename)







