#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from Hsv_form_detection_final import Find_object
from correct_skew import Skew


# L'application Qt
class QtAppli(QApplication):

    # Constructeur fenêtre
    def __init__(
            self,
            argv):

        # Appel constructeur de l'objet hérité
        QApplication.__init__(self, argv)

        # Attributs de l'application (c'est juste par habitude)
        self.argv = argv

        # Widget principale
        self.wid = QMainWindow()
        self.wid.setCentralWidget(QWidget(self.wid))
        self.wid.statusBar()

        # Titre
        self.wid.setWindowTitle("Planning Intéractif")

        # Un espace de rangement
        layoutG = QVBoxLayout(self.wid.centralWidget())
        layoutG.setMargin(5)
        layoutG.setSpacing(5)

        # Le module de saisie
        myEdit = QtSaisie()

        # Pour quitter
        quit = QPushButton()
        quit.setText("Quitter")
        self.connect(quit, SIGNAL("clicked()"), self.wid, SLOT("close()"))

        # Rangement des éléments dans le layout
        layoutG.addWidget(myEdit)
        layoutG.addWidget(quit)

    # Affichage et lancement application
    def run(self):
        self.wid.show()
        self.exec_()

# Mon module de saisie
class QtSaisie(QFrame):
    # Constructeur module
    def __init__(self):
        # Appel constructeur de l'objet hértié
        QFrame.__init__(self)

        # Un espace de rangement
        layoutG = QVBoxLayout(self)
        layoutG.setMargin(0)
        layoutG.setSpacing(0)

        # La zone saisie nom et son action
        layoutNom = QGridLayout()
        layoutNom.setMargin(0)
        layoutNom.setSpacing(0)
        labelNom = QLabel("Nom du fichier")
        self.__editNom = QLineEdit()
        self.connect(self.__editNom, SIGNAL("textChanged(const QString &)"), self.__slotEdited)
        self.__action = QPushButton("Upload")
        self.__action.setDisabled(True)
        self.connect(self.__action, SIGNAL("clicked()"), self.__slotAction)
        layoutNom.addWidget(labelNom, 0, 0, 1, 1)
        layoutNom.addWidget(self.__editNom, 1, 0, 1, 1)
        layoutNom.addWidget(self.__action, 1, 1, 1, 1)

        # Rangement des éléments dans le layout
        layoutG.addLayout(layoutNom)
        layoutG.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding,))

    # Nettoyage (si besoin)
    def clear(self):
        # Nettoyage des zones
        self.__nomEdit.clear()

    # Quand la zone de saisie est modifiée
    def __slotEdited(self, text):
        # Le bouton n'est activé que si la zone n'est pas vide
        self.__action.setEnabled(len(text) != 0)


    # Action sur le bouton
    def __slotAction(self):
        # Appel des fonctions des autres fichiers pour traiter l'image
        csvname = self.__editNom.text()
        dialog = QFileDialog()

        filename = dialog.getOpenFileName(None, 'Import Image ', "", "jpg data files (*.jpg)")
        Skew.__init__(Skew, filename)
        Find_object.__init__(Find_object, filename, csvname)


# Pour lancer le programme
if __name__ == "__main__":
    # Application Qt qui va afficher la fenetre
    Appli = QtAppli(sys.argv)
    Appli.run()
