# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'frm_per_iatreia.ui'
#
# Created: Wed Nov 12 11:29:37 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(723, 510)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setMaximumSize(QtCore.QSize(29, 16777215))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 0, 0, 1, 1, QtCore.Qt.AlignRight)
        self.cboYear = QtGui.QComboBox(self.centralwidget)
        self.cboYear.setObjectName(_fromUtf8("cboYear"))
        self.gridLayout.addWidget(self.cboYear, 0, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 2, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_4.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(self.centralwidget)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.horizontalLayout_4.addWidget(self.lineEdit)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.groupBox_data = QtGui.QGroupBox(self.centralwidget)
        self.groupBox_data.setObjectName(_fromUtf8("groupBox_data"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.groupBox_data)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.checkBox = QtGui.QCheckBox(self.groupBox_data)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.verticalLayout_2.addWidget(self.checkBox)
        self.tableView = QtGui.QTableView(self.groupBox_data)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout_2.addWidget(self.tableView)
        self.verticalLayout.addWidget(self.groupBox_data)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 723, 19))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_zoom = QtGui.QAction(MainWindow)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ygeia/icons/1394568050_Zoom.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_zoom.setIcon(icon)
        self.action_zoom.setObjectName(_fromUtf8("action_zoom"))
        self.action_showmap = QtGui.QAction(MainWindow)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/ygeia/icons/map_add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_showmap.setIcon(icon1)
        self.action_showmap.setObjectName(_fromUtf8("action_showmap"))
        self.toolBar.addAction(self.action_zoom)
        self.toolBar.addAction(self.action_showmap)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "Αναζήτηση με βάση την ονομασία", None))
        self.label_2.setText(_translate("MainWindow", "Έτος", None))
        self.label.setText(_translate("MainWindow", "Ονομασία:", None))
        self.groupBox_data.setTitle(_translate("MainWindow", "Δεδομένα", None))
        self.checkBox.setText(_translate("MainWindow", "Άμεση επιλογή/εστίαση στον χάρτη", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.action_zoom.setText(_translate("MainWindow", "Εστίαση στο επιλεγμένο αντικείμενο", None))
        self.action_zoom.setToolTip(_translate("MainWindow", "Εστίαση στο επιλεγμένο αντικείμενο", None))
        self.action_showmap.setText(_translate("MainWindow", "Οπτικοποίηση στον χάρτη", None))
        self.action_showmap.setToolTip(_translate("MainWindow", "Οπτικοποίηση στον χάρτη", None))

import resources_rc
