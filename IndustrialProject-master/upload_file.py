#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from Hsv_form_detection_final import test


class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()
        self.initUI()

    def initUI(self):
        #create btn to find your picture
        qbtn = QtGui.QPushButton('Upload your image here', self)
        #qbtn.clicked.connect(QtCore.QCoreApplication.instance().quit)
        #qbtn.clicked(self,self,self.upload_csv())$
        qbtn.clicked.connect(lambda: self.upload_csv())

        qbtn.resize(qbtn.sizeHint())
        qbtn.move(50, 50)

        self.qtext = QtGui.QLineEdit(self)
        self.qtext.move(50, 100)
        self.qtext.resize(self.qtext.sizeHint())

        qbtn_val = QtGui.QPushButton('Valider', self)
        qbtn_val.resize(qbtn_val.sizeHint())
        qbtn_val.move(50, 125)
        qbtn_val.clicked.connect(lambda: self.recover_csvname())


        #create windows
        self.setGeometry(300, 300, 250, 250)
        self.setWindowTitle('Planmeric Your planning generator')
        self.show()

    def recover_csvname(self):
        csvname = self.qtext.text()
        test.__init__(self, self.upload_csv(), csvname)

    def upload_csv(self):
        #call when you click on the button to open "explorateur fichier"
        dialog = QtGui.QFileDialog()
        filename = dialog.getOpenFileName(None, 'Import Image ',"",  "jpg data files (*.jpg)")
        return filename

        #fname = dialog.getOpenFileName(None, "Import CSV", "", "CSV data files (*.csv)")


def main():
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()






