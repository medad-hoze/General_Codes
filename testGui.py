import sys

from PyQt6.QtWidgets import QApplication,QWidget,QLineEdit,QPushButton,QTextEdit,QVBoxLayout

from PyQt6.QtGui import QIcon


class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('hello app')
        self.setWindowIcon(QIcon('maps.ico'))
        self.resize(500,350)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.KeepWords = []

        self.inputField = QLineEdit()
        button = QPushButton('&hello efrat',clicked=self.sayHello)
        self.output = QTextEdit()
        

        layout.addWidget(self.inputField)
        layout.addWidget(button)
        layout.addWidget(self.output)

    def sayHello(self):
        inputText = self.inputField.text()
        self.KeepWords.append(inputText)
        if inputText == 'clean':
             self.KeepWords = []
        self.output.setText(','.join(i for i in self.KeepWords if i not in ('[',']')))



        

app = QApplication(sys.argv)

window = MyApp()
window.show()

app.exec()