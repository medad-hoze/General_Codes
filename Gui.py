# -*- coding: utf-8 -*-

import sys,os
from PyQt6.QtWidgets import QFileDialog,QApplication, QWidget, QTableWidget, QTableWidgetItem, \
    QPushButton, QVBoxLayout,QLabel,QProgressBar

import pandas as pd # pip install pandas

from pathlib import Path

def createFolder(dic):
    try:
        if not os.path.exists(dic):
            os.makedirs(dic)
    except OSError:
        print ("Error Create dic")       

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.window_width, self.window_height = 700, 500
        self.resize(self.window_width, self.window_height)
        self.setWindowTitle('SOD Conflicts Results Report')

        layout = QVBoxLayout()
        self.setLayout(layout)

        # load Excel
        # self.inputField = QLineEdit()
        # layout.addWidget(self.inputField)

        self.btn = QPushButton('Dialog', self)
        self.btn.move(280, 32)
        self.btn.clicked.connect(self.showDialog)

        self.status = QLabel('')
        layout.addWidget(self.status)

        # Create view Table
        self.table = QTableWidget()
        layout.addWidget(self.table)

        # load Data
        self.button = QPushButton('&Browse Data')
        self.button.clicked.connect(lambda _, sheet_name= '': self.loadExcelData(self.showDialog()))
        layout.addWidget(self.button)

        self.button2 = QPushButton('Run')
        self.button2.clicked.connect(self.closeApp)
        layout.addWidget(self.button2)


        self.prog_bar = QProgressBar(self)
        self.prog_bar.setGeometry(230, 380, 250, 30)


    def closeApp(self):
        self.close()

    def showDialog(self):

        home_dir = str(Path.home())
        fname = QFileDialog.getOpenFileName(self, 'Open file', home_dir)
        self.status.setText(fname[0])
        if fname[0]:
            return fname[0]


    # def Get_path(self):
    #     inputText = self.inputField.text()
    #     return inputText

    def Run_program(self,df):
        new_folder = os.path.dirname(self.path) + '\\' + 'new_dir'
        createFolder(new_folder)
        pass

    def loadExcelData(self, excel_file_dir):
        self.path = excel_file_dir
        df = pd.read_excel(excel_file_dir)
        if df.size == 0:
            return

        df.fillna('', inplace=True)
        self.table.setRowCount(df.shape[0])
        self.table.setColumnCount(df.shape[1])
        self.table.setHorizontalHeaderLabels(df.columns)

        # returns pandas array object
        for row in df.iterrows():
            values = row[1]
            value2 = self.prog_bar.value()
            for col_index, value in enumerate(values):
                if isinstance(value, (float, int)):
                    value = '{0:0,.0f}'.format(value)
                    self.prog_bar.setValue(value2 + 1)
                tableItem = QTableWidgetItem(str(value))
                self.table.setItem(row[0], col_index, tableItem)

        self.table.setColumnWidth(2, 300)

        self.Run_program(df)
        
if __name__ == '__main__':
    # don't auto scale when drag app to a different monitor.
    # QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
    


    app = QApplication(sys.argv)


    
    myApp = MyApp()
    myApp.show()

    try:
        sys.exit(app.exec())
    except SystemExit:
        print('Closing Window...')


        