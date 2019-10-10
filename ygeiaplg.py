# -*- coding: utf-8 -*-
from PyQt4.QtCore import * 
from PyQt4.QtGui import *
from PyQt4.QtXml import *
from PyQt4 import QtSql


from qgis.core import *
from qgis.gui import *

# initialize Qt resources from file resouces.py
import resources_rc


from Ui_per_iatreia import per_iatreia_Dialog
from Ui_deiktes3 import deiktes3_Dialog
from Ui_dbSettings import dbSettings_Dialog
import processing

from mysettings import  *
from myfunctions import *

import tempfile
from datetime import datetime
from mylayer import myfield, mylayer, TabCategory
from __builtin__ import str

class ygeiaCls:


  def __init__(self, iface):
    # save reference to the QGIS interface
    self.iface = iface

    QtSql.QSqlDatabase.removeDatabase("health_connection")
    
    self.dbase = QtSql.QSqlDatabase.addDatabase(DBDRIVER, "health_connection")
    self.dbase.setHostName(HOST)
    self.dbase.setPort(int(PORT)) 
    self.dbase.setDatabaseName(DBNAME)
    self.dbase.setUserName(USERNAME)
    self.dbase.setPassword(PASSWORD)

 

        
  def initGui(self):
    # create action that will start plugin configuration
    self.action = QAction(QIcon(":/plugins/ygeia/icons/App-virussafe-injection-icon.png"), u"Περιφερειακά ιατρεία", self.iface.mainWindow())
    self.action2 = QAction(QIcon(":/plugins/ygeia/icons/App-virussafe-injection-icon.png"), u"Κέντρα Υγείας", self.iface.mainWindow())
    self.action3 = QAction(QIcon(":/plugins/ygeia/icons/App-virussafe-injection-icon.png"), u"Κρατικά νοσοκομεία", self.iface.mainWindow())
    self.action4 = QAction(QIcon(":/plugins/ygeia/icons/1-Normal-Train-icon.png"), u"Δρομολόγια τρένων", self.iface.mainWindow())
    self.action5 = QAction(QIcon(":/plugins/ygeia/icons/document-add-icon.png"), u"Αλλαγή αρχείου για τα δρομολόγια τρένων", self.iface.mainWindow())
    self.action6 = QAction(QIcon(":/plugins/ygeia/icons/qgis-icon-60x60.png"), u"Ανάκτηση αρχείου Qgis project", self.iface.mainWindow())
    self.action7 = QAction(QIcon(":/plugins/ygeia/icons/database-arrow-down-icon.png"), u"Ρυθμίσεις σύνδεσης στην Β.Δ.", self.iface.mainWindow())
    self.action14 = QAction(QIcon(":/plugins/ygeia/icons/Line-Chart-icon.png"), u"Δείκτες", self.iface.mainWindow())

    
    # self.action.setObjectName("testAction")
    self.action.setWhatsThis("Iατρικά δεδομένα")
    self.action.setStatusTip(u"Iατρικά δεδομένα")
    

    self.action.triggered.connect(self.runPI)
    self.action2.triggered.connect(self.runKY)
    self.action3.triggered.connect(self.runKN)
    
    path = (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'docs', "dromologia_athina_thessaloniki_alexandroupoli_dikaia.pdf"))  # pdf path για δρομολογια
    self.action4.triggered.connect(lambda: startfile(path))

    self.action5.triggered.connect(self.updatetrainfile)
    self.action6.triggered.connect(self.restoreQgisProject)


    self.action14.triggered.connect(self.deiktes3)
    self.action7.triggered.connect(self.dbsettings)
    


    # υπομενού Αναζήτηση δεδομένων
    self.menuSearch = QMenu(self.iface.mainWindow())
    self.menuSearch.setObjectName("Search")
    self.menuSearch.setTitle(u"Αναζήτηση δεδομένων")
    self.menuSearch.setIcon (QIcon(":/plugins/ygeia/icons/Filter-List-icon.png"))        
    self.menuSearch.addAction(self.action)
    self.menuSearch.addAction(self.action2)
    self.menuSearch.addAction(self.action3)
    
    


    
    # υπομενού Ρυθμίσεις
    self.menuSettings = QMenu(self.iface.mainWindow())
    self.menuSettings.setObjectName("Settings")
    self.menuSettings.setTitle(u"Διάφορα")
    self.menuSettings.setIcon (QIcon(":/plugins/ygeia/icons/setting-icon.png"))
    self.menuSettings.addAction(self.action7)
    self.menuSettings.addAction(self.action4)
    self.menuSettings.addAction(self.action5)
    self.menuSettings.addAction(self.action6)

    # Custom menu
    self.menu = QMenu(self.iface.mainWindow())
    self.menu.setObjectName("ygeiaMenu")
    self.menu.setTitle(u"Ιατρικά δεδομένα")
    menuBar = self.iface.mainWindow().menuBar()
    menuBar.insertMenu(self.iface.firstRightStandardMenu().menuAction(), self.menu)
    

    self.menu.addMenu(self.menuSearch)
    self.menu.addMenu(self.menuSettings)
    self.menu.addAction(self.action14)

    
  

  def updatetrainfile(self):
      import shutil
      
      fname = QFileDialog.getOpenFileName(filter=u"Αρχεία pdf (*.pdf)")
      if not fname:
          return
      print fname
      try:
          shutil.copyfile(fname, (os.path.join(os.path.dirname(os.path.realpath(__file__)), 'docs', "dromologia_athina_thessaloniki_alexandroupoli_dikaia.pdf")))
          QMessageBox.information(None, u"Ενημέρωση!", u"Επιτυχής ενημέρωση του αρχείου δρομολογίων")
      except:
          QMessageBox.critical(None, u"Σφάλμα", u"Σφάλμα ενημέρωσης του αρχείου δρομολογίων", QMessageBox.Ok | QMessageBox.Default, QMessageBox.NoButton)
      

  def restoreQgisProject(self):
      import shutil
      
      
      fileName = QFileDialog.getSaveFileName(None, 'Save File', os.getenv('HOME'), u"Αρχεία qgs (*.qgs)")
             
      if not fileName:
          return
      
      
      try:
          if not fileName.endswith('.qgs'):
             fileName = fileName + '.qgs'
          shutil.copyfile((os.path.join(os.path.dirname(os.path.realpath(__file__)), 'docs', "PFY.qgs")), fileName)
          QMessageBox.information(None, u"Ενημέρωση!", u"Το αρχείο ανακτήθηκε επιτυχώς!")
      except:
          QMessageBox.critical(None, u"Σφάλμα", u"Σφάλμα κατά την ανάκτηση του αρχείου", QMessageBox.Ok | QMessageBox.Default, QMessageBox.NoButton)
      


       
  def unload(self):
    # remove the plugin menu item and icon
    self.iface.removePluginMenu(u"Iατρικά δεδομένα", self.action)
    self.iface.removePluginMenu(u"Iατρικά δεδομένα", self.action2)
    self.iface.removePluginMenu(u"Iατρικά δεδομένα", self.action4)
    self.iface.removePluginMenu(u"Iατρικά δεδομένα", self.action7)
    self.iface.removePluginMenu(u"Iατρικά δεδομένα", self.action14)

    
    self.menu.deleteLater()
    


  def runKN(self):
    self.knlayer = mylayer("fun_kn_full", u'Κρατικά νοσοκομεια')
    
    fields = [
            # Tab1
            {'name':'pk_uid', 'alias':u"Α/Α εγγραφής", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':'the_geom', 'alias':u"Γεωμετρία", 'hidden':True, 'geomField':True, 'tabCategory':TabCategory.tab1},
            {'name':u'Επωνυμία', 'alias':u"Επωνυμία", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':u'Ειδικότητα', 'alias':u"Ειδικότητα", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':u"Κλινικές", 'alias':u"Κλινικές", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':'dhmosid', 'alias':u"Κωδικός Δήμου", 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':u'Τηλέφωνο', 'alias':u"Τηλέφωνο", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':u'Διεύθυνση', 'alias':u"Διεύθυνση", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':u'ΤΚ', 'alias':u"ΤΚ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':u'E-mail', 'alias':u"E-mail", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':u'Παρατηρήσεις', 'alias':u"Παρατηρήσεις", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
             
             # Tab2
             {'name':u'Γεωγραφικός Μήκος (WGS84)', 'alias':u"Γεωγραφικός Μήκος (WGS84)", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
             {'name':u'Γεωγραφικός Πλάτος (WGS84)', 'alias':u"Γεωγραφικός Πλάτος (WGS84)", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
             {'name':u'X ΕΓΣΑ87', 'alias':u"X ΕΓΣΑ87", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
             {'name':u'Υ ΕΓΣΑ87', 'alias':u"Υ ΕΓΣΑ87", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
             {'name':u'Δήμος', 'alias':u"Δήμος", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
             {'name':u'Περιφερειακή ενότητα', 'alias':u"Περιφερειακή ενότητα", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},

             # Tab3
             {'name':u"Έτος", 'alias':u"Έτος", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
             {'name':u"Αριθμός κλινών", 'alias':u"Αριθμός κλινών", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
             {'name':u"Εργαστήρια", 'alias':u"Εργαστήρια", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
             {'name':u"Αξονικός τομογράφος", 'alias':u"Αξονικός τομογράφος", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
             {'name':u"ΜΕΘ", 'alias':u"ΜΕΘ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
             {'name':u"Συχνότητα διακομιδων ΕΚΑΒ", 'alias':u"Συχνότητα διακομιδων ΕΚΑΒ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
             {'name':u"Διάγνωση", 'alias':u"Διάγνωση", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
              

            ]
    
    for field in fields:

        # print field['name'], field['alias']
        objField = myfield(name=field['name'], alias=field['alias'], hidden=field['hidden'], geomField=field['geomField'], tabCategory=field['tabCategory'])
        self.knlayer.addField(objField)
    
    
    # ορισμός πρωτεύοντος κλειδιού, απαραίτητο όταν καλό layer από sql
    self.knlayer.setPkey('pk_uid')
    self.knlayer.setFilterColumn(u'Επωνυμία')      
    self.knlayer.setSortColumn(u'Επωνυμία')      
    
    filterColumnIndex = 0  # με βάση την σειρά των πεδίων στην βάση
    sortColumnIndex = 0  # με βάση την σειρά των πεδίων στην βάση
    
   #############  #############  #############  #############  #############  #############

    
    self.dlg = per_iatreia_Dialog(self.iface, self.knlayer)
    
    self.dlg.setWindowTitle(u"Αναζήτηση κρατικών νοσοκομείων");
    self.dlg.setFocus(True)
    self.dlg.activateWindow()
    self.dlg.setStyle(QStyleFactory.create("plastique"))
    self.dlg.show()
    
  def runPI(self):
    self.pilayer = mylayer("fun_pi_full", u'Περιφερειακά ιατρεία')
    
    fields = [
          # Tab1
        {'name':'pk_uid', 'alias':u"Α/Α εγγραφής", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'perif_iatreio', 'alias':u"Περιφερειακό ιατρείο", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'ky', 'alias':u"Κέντρο υγείας", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'ype', 'alias':u"ΥΠΕ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'nosokomeio', 'alias':u"Νοσοκομείο", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'eidos', 'alias':u"Είδος", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'agono', 'alias':u"Άγονο", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'elstatid2011', 'alias':'elstatid2011', 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'paratiriseis', 'alias':u"Παρατηρήσεις", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
        {'name':'the_geom', 'alias':'the_geom', 'hidden':True, 'geomField':True, 'tabCategory':TabCategory.tab1},
        # Tab2
        {'name':'x_2100', 'alias':u'Χ ΕΓΣΑ87', 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'y_2100', 'alias':u'Υ ΕΓΣΑ87', 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'lat', 'alias':u"Γεωγραφικός Πλάτος (WGS84)", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'long', 'alias':u"Γεωγραφικός Μήκος (WGS84)", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'oikismos11', 'alias':u"Οικισμός", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'dt_tk11', 'alias':u"Δημοτική κοινότητα/τοπική κοινότητα", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'de11', 'alias':u"Δημοτική Ενότητα", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'dhmos11', 'alias':u"Δήμος", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        {'name':'pe11', 'alias':u"Περιφερειακή ενότητα", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
        # Tab3
        {'name':'pi_pk_uid', 'alias':'pi_pk_uid', 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab3},
        {'name':'eksetasthentes', 'alias':u"Εξετασθέντες", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
        {'name':'syntagografisi', 'alias':u"Συνταγογράφηση", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
        {'name':'pi_data_pk_uid', 'alias':'pi_data_pk_uid', 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab3}
            ]
    
    for field in fields:

        # print field['name'], field['alias']
        objField = myfield(name=field['name'], alias=field['alias'], hidden=field['hidden'], geomField=field['geomField'], tabCategory=field['tabCategory'])
        self.pilayer.addField(objField)
    
    
    # ορισμός πρωτεύοντος κλειδιού, απαραίτητο όταν καλό layer από sql
    self.pilayer.setPkey('pk_uid')
    self.pilayer.setFilterColumn('perif_iatreio')      
    self.pilayer.setSortColumn('perif_iatreio')      
    
    filterColumnIndex = 0  # με βάση την σειρά των πεδίων στην βάση
    sortColumnIndex = 0  # με βάση την σειρά των πεδίων στην βάση
    
   #############  #############  #############  #############  #############  #############

    
    self.dlg = per_iatreia_Dialog(self.iface, self.pilayer)
    
    self.dlg.setWindowTitle(u"Αναζήτηση περιφερειακών ιατρείων");
    self.dlg.setFocus(True)
    self.dlg.activateWindow()
    self.dlg.setStyle(QStyleFactory.create("plastique"))
    self.dlg.show()

    
  def runKY(self):

    # columns_hide=()

   #############  #############  #############  #############  #############  #############
   
    self.kylayer = mylayer("fun_ky_full", u'Κέντρα υγείας')
    
    fields = [
            # Tab1                     
            {'name':'ky_pk_uid', 'alias':u"Α/Α Κέντρου Υγείας", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':'ype', 'alias':u"ΥΠΕ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':'the_geom', 'alias':u"Γεωμετρία", 'hidden':True, 'geomField':True, 'tabCategory':TabCategory.tab1},
            {'name':'ky', 'alias':u"Κέντρο Υγείας", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':'nosokomeio', 'alias':u"Νοσοκομείο", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},

            {'name':'elstatid2011', 'alias':"elstatid2011", 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':'paratiriseis', 'alias':u"Παρατηρήσεις", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab1},
            
            # Tab2
            {'name':"lat", 'alias':u"Γεωγραφικός Πλάτος (WGS84)", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':"long", 'alias':u"Γεωγραφικός Μήκος (WGS84)", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':"x_2100" , 'alias':u"X ΕΓΣΑ87" , 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':"y_2100" , 'alias':u"Υ ΕΓΣΑ87" , 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},

  
             {'name':'oikismos', 'alias':u"Οικισμός", 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':'dhmos', 'alias':u"ΔΚ/ΤΚ", 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab2},
         
            
            {'name':'oikismos11', 'alias':u"Οικισμός", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':'dt_tk11', 'alias':u"ΔΚ/ΤΚ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':'de11', 'alias':u"Δημοτική ενότητα", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':'dhmos11', 'alias':u"Δήμος", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            {'name':"pe11" , 'alias':u"Περιφερειακή ενότητα" , 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab2},
            
           
            
            # Tab3
            {'name':'pk_uid', 'alias':u"Α/Α Κέντρου Υγείας", 'hidden':True, 'geomField':False, 'tabCategory':TabCategory.tab1},
            {'name':'year', 'alias':u"Έτος", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'syntagografisi', 'alias':u"ΣΥΝΤΑΓΟΓΡΑΦΗΣΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'eksetaseis_synolo', 'alias':u"ΕΞΕΤΑΣΕΙΣ ΣΥΝΟΛΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'eksetasthentes_synolo', 'alias':u"ΕΞΕΤΑΣΘΕΝΤΕΣ ΣΥΝΟΛΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_loipo_texniko', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΛΟΙΠΟ ΤΕΧΝΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_dioik_prosop', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΔΙΟΙΚΗΤΙΚΟ ΠΡΟΣΩΠΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_nosil_prosop', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΝΟΣΗΛΕΥΤΙΚΟ ΠΡΟΣΩΠΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_paraiat_prosop', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΠΑΡΑΙΑΤΡΙΚΟ ΠΡΟΣΩΠΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_iatriko_prosopiko', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΙΑΤΡΙΚΟ ΠΡΟΣΩΠΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_paidopsix', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΠΑΙΔΟΨΥΧΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_psixiatriki', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΨΥΧΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_gynaikologia', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΓΥΝΑΙΚΟΛΟΓΙΑ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_orthopediki', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΟΡΘΟΠΕΔΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_xeirourgiki', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΧΕΙΡΟΥΡΓΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_kardiologia', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΚΑΡΔΙΟΛΟΓΙΑ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_mikroviologoi', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΜΙΚΡΟΒΙΟΛΟΓΙΑ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_odontiatriki', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΟΔΟΝΤΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_paidiatriki', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΠΑΙΔΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_pathologia', 'alias':u"ΟΡΓΑΝΙΚΕΣ  Γ.Ι ΠΑΘΟΛΟΓΙΑ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'organ_aktinologiko', 'alias':u"ΟΡΓΑΝΙΚΕΣ ΑΚΤΙΝΟΛΟΓΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
           
            {'name':'ypir_loipo_texniko', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΛΟΙΠΟ ΤΕΧΝΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_dioikitiko', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΔΙΟΙΚΗΤΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_paraiat_prosop', 'alias':u"ΥΠΗΡΕΤ. ΠΑΡΑΙΑΤΡΙΚΟ ΠΡΟΣΩΠΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_nosil_prosop', 'alias':u"ΥΠΗΡΕΤ. ΝΟΣΗΛΕΥΤΙΚΟ ΠΡΟΣΩΠΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_iatriko_prosop', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΙΑΤΡΙΚΟ ΠΡΟΣΩΠΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_paidopsixiatriki', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΠΑΙΔΟΨΥΧΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_psixiatriki', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΨΥΧΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_gynaikologia', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΓΥΝΑΙΚΟΛΟΓΙΑ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_orthopediki', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΟΡΘΟΠΕΔΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':'ypir_xeirourgiki', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΧΕΙΡΟΥΡΓΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':u'ypir_mikroviologoi', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΜΙΚΡΟΒΙΟΛΟΓΟΙ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':u'ypir_kardiologia', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΚΑΡΔΙΟΛΟΓΙΑ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':u'ypir_odontiatriki', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΟΔΟΝΤΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':u'ypir_paidiatriki', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΠΑΙΔΙΑΤΡΙΚΗ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            
            {'name':u'ypir_pathologia', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ  Γ. Ι-ΠΑΘΟΛΟΓΙΑ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3},
            {'name':u'ypir_aktinologiko', 'alias':u"ΥΠΗΡΕΤΟΥΝΤΕΣ ΑΚΤΙΝΟΛΟΓΙΚΟ", 'hidden':False, 'geomField':False, 'tabCategory':TabCategory.tab3}

            

            ]
    
    for field in fields:

        # print field['name'], field['alias']
        objField = myfield(name=field['name'], alias=field['alias'], hidden=field['hidden'], geomField=field['geomField'], tabCategory=field['tabCategory'])
        self.kylayer.addField(objField)
    
    
    # ορισμός πρωτεύοντος κλειδιού, απαραίτητο όταν καλό layer από sql
    self.kylayer.setPkey('ky_pk_uid')
    self.kylayer.setFilterColumn('ky')      
    self.kylayer.setSortColumn('ky')      
    
    filterColumnIndex = 0  # με βάση την σειρά των πεδίων στην βάση
    sortColumnIndex = 0  # με βάση την σειρά των πεδίων στην βάση
    
   #############  #############  #############  #############  #############  #############

    
    self.dlg = per_iatreia_Dialog(self.iface, self.kylayer)
    
    self.dlg.setWindowTitle(u"Αναζήτηση κέντρων υγείας");
    self.dlg.setFocus(True)
    self.dlg.activateWindow()
    self.dlg.setStyle(QStyleFactory.create("plastique"))
    self.dlg.show()
    
    
  def deiktes3(self):
    # create and show the dialog 
    self.dlg = deiktes3_Dialog(self.iface)
    self.dlg.setWindowTitle(u"Δείκτες");
    self.dlg.setFocus(True)
    self.dlg.activateWindow()
    self.dlg.setStyle(QStyleFactory.create("plastique"))
    self.dlg.show()     
   
   

  def dbsettings(self):
    # create and show the dialog 
    self.dlg = dbSettings_Dialog()
    self.dlg.setFocus(True)
    self.dlg.activateWindow()
    self.dlg.setStyle(QStyleFactory.create("plastique"))
    self.dlg.show()


    
  
