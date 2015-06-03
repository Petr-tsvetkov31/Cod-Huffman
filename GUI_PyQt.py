# -*- coding: utf-8 -*-

import sys

from PyQt4 import QtGui, QtCore

import Core


class MainGuiWidget(QtGui.QWidget):
    """Основное окно приложения"""

    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setFixedSize(800, 400)
        self.setWindowTitle("Huffman's code")
        self.center()

        inputLabel = QtGui.QLabel("Please, enter your text and push the button...", self)
        inputLabel.setGeometry(10, 30, 350, 30)

        global inputArea
        inputArea = QtGui.QTextEdit(self)
        inputArea.setGeometry(10, 100, 350, 200)

        outputLabel = QtGui.QLabel("Codes:", self)
        outputLabel.setGeometry(460, 10, 330, 30)

        global outputArea
        outputArea = QtGui.QTextEdit(self)
        outputArea.setGeometry(460, 50, 330, 300)
        outputArea.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)

        enterButton = QtGui.QPushButton("Encode=>", self)
        enterButton.setGeometry(360, 155, 100, 100)

        clearButton = QtGui.QPushButton("Clear", self)
        clearButton.setGeometry(10, 310, 80, 35)

        exitButton = QtGui.QPushButton("Exit", self)
        exitButton.setGeometry(10, 360, 80, 35)

        # exitButton.clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.connect(exitButton, QtCore.SIGNAL("clicked()"), QtCore.QCoreApplication.instance().quit)

        self.connect(clearButton, QtCore.SIGNAL("clicked()"), inputArea, QtCore.SLOT("clear()"))
        self.connect(enterButton, QtCore.SIGNAL("clicked()"), self.encode)

    def closeEvent(self, event):

        reply = QtGui.QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QtGui.QMessageBox.Yes |
            QtGui.QMessageBox.No, QtGui.QMessageBox.No)

        if reply == QtGui.QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()

    def center(self):
        """Функция выравнивания окна по центру экрана"""
        screen = QtGui.QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width() - size.width()) / 2, (screen.height() - size.height()) / 2)

    def encode(self):
        """Обработка в соответсвии с алгоритмом Хаффмана (модуль Core.py)"""
        inpStr = inputArea.toPlainText()
        outStr = ""
        Code, HuffTree = Core.HuffCode(inpStr)
        for key, value in Code.items():
            outStr += "{:^5} => {}\n".format(key, value)
        outStr += "\nYour text, encoded by Huffman's codes:\n" + Core.HuffStr(inpStr)
        outputArea.setPlainText(outStr)


app = QtGui.QApplication(sys.argv)
wind = MainGuiWidget()
wind.show()
sys.exit(app.exec_())
