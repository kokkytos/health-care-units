# -*- coding: utf-8 -*-

import os
import time

from PyQt4 import QtCore, QtGui, QtSql, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from frm_dbSettings import Ui_MainWindow
from mysettings import  *
from qgis.core import *


# create the dialog for paradosiakoioikismoi
class dbSettings_Dialog(QtGui.QMainWindow):
    '''Class to handle db connection settings'''  
  

        
                
        
    def __init__(self): 
      
        QtGui.QMainWindow.__init__(self) 


    
         # Set up the user interface from Designer. 
        self.ui = Ui_MainWindow ()
        self.ui.setupUi(self)
     
    
        self.lb=QLabel( )
        self.lb.setFrameStyle(QtGui.QFrame.Panel |QtGui.QFrame.Sunken)
    
        
    
        self.db = QtSql.QSqlDatabase.database( "health_connection") #ανοίγει ταυτόχρονα και η σύνδεση:
    
        print "My DB is already opened:", self.db.isOpen ()
        
        if not self.db.isOpen ():

            ok = self.db.open()
            if ok==True:
                print "Database just opened now!"
                
            else:
                print "Failed to open database!"
                error= self.db.lastError()
                print error.text()
                self.lb=QLabel(u"<font color='red'>Αποτυχία σύνδεσης...</font>")
                
        #add widget label to statusBar
        self.statusBar().addWidget(self.lb,0)
        
        if self.db.isOpen ():
             self.lb.setText(u"<font color='green'>Επιτυχής σύνδεση!</font>")
                

        
        self.ui.lineEdit_host.setText(HOST)
        self.ui.lineEdit_port.setText(str(PORT))
        self.ui.lineEdit_schema.setText(SCHEMA)
        self.ui.lineEdit_username.setText(USERNAME)
        self.ui.lineEdit_password.setText(PASSWORD)
        self.ui.lineEdit_db.setText(DBNAME)
        
        
        #signals and slots
        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.close)
        
    def accept(self):
        
        self.dbdriver=DBDRIVER
        self.host = self.ui.lineEdit_host.text()
        self.port=int(self.ui.lineEdit_port.text())
        self.schema = self.ui.lineEdit_schema.text()
        self.username = self.ui.lineEdit_username.text()
        self.password = self.ui.lineEdit_password.text()
        self.dbname = self.ui.lineEdit_db.text()
        
        
        #call write function
        args={"host":self.host, "dbname":self.dbname, "port":self.port,"schema":self.schema, "username":self.username,"password":self.password}
        write(**args)
        
        if self.db.isOpen:
            self.db.close ()
            del self.db
            QtSql.QSqlDatabase.removeDatabase("health_connection")
             
            self.db=QtSql.QSqlDatabase.addDatabase(self.dbdriver, "health_connection" )
            self.db.setHostName(self.host)
            self.db.setPort(int(self.port)) 
            self.db.setDatabaseName( self.dbname)
             
            self.db = QtSql.QSqlDatabase.database( "health_connection") #ανοίγει ταυτόχρονα και η σύνδεση:
            self.db.open(self.username, self.password)

            
        if not self.db.isOpen ():

            ok = self.db.open()
            if ok==True:
                print "Database just opened now!"
                
            else:
                print "Failed to open database!"
                error= self.db.lastError()
                print error.text()
                self.lb.setText(u"<font color='red'>Αποτυχία σύνδεσης...</font>")
                QMessageBox.warning(None,u"Ενημέρωση!",error.text())
        
        
        if self.db.isOpen ():
             self.lb.setText(u"<font color='green'>Επιτυχής σύνδεση!</font>")
             QMessageBox.information(None,u"Ενημέρωση!",u"Παρακαλώ επανεκκινήστε την εφαρμογή για την ενημέρωση των νέων ρυθμίσεων.")
        