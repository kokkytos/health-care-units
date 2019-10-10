# -*- coding: utf-8 -*-
import ConfigParser
import os
import time

from PyQt4 import QtCore, QtGui, QtSql, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from frm_map_settings import Ui_Dialog
from myfunctions import *
from mysettings import  *
from qgis.core import *





class frm_map_settins_Dialog(QtGui.QDialog):
    '''Class to handle medical data'''       
        
    def __init__(self): 
       QtGui.QDialog.__init__(self) 
         # Set up the user interface from Designer. 
       self.ui = Ui_Dialog ()
       self.ui.setupUi(self)

       
       modes = { QgsGraduatedSymbolRendererV2.EqualInterval : u"Ισομεγέθη",
          QgsGraduatedSymbolRendererV2.StdDev        : u"Τυπική απόκλιση",

        }
       
       for k,v in modes.items():
            self.ui.comboBox.addItem(v,k)
   
       #signals and slots
       self.ui.buttonBox.accepted.connect(self.accept)
       self.ui.buttonBox.rejected.connect(self.reject)

