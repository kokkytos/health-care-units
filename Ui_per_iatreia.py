# -*- coding: utf-8 -*-
import os
import time

from PyQt4 import QtCore, QtGui, QtSql, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *

from frm_per_iatreia import Ui_MainWindow
from myfunctions import *
from mysettings import  *
from qgis.core import *
from types import *

# create the dialog for paradosiakoioikismoi
class per_iatreia_Dialog(QtGui.QMainWindow):
  '''Class to handle medical data'''  

  def __init__(self, iface, mylayer): 
      
   
    QtGui.QMainWindow.__init__(self) 
    
    self.iface=iface
    self.canvas = self.iface.mapCanvas()
       
    #self.kwargs_headers = kwargs_headers
    #self.args_hide=args_hide
    self.mytable=mylayer.name
    #self.layer=layer
    self.mylayer=mylayer
    self.primary_key=self.mylayer.keyfield

    
    
    assert type(self.primary_key.name) is StringType, "Primary key is not a string: %r" % self.primary_key
    

    
    self.fun_sql = None
    self.year= None
    
    
    
    # Set up the user interface from Designer. 
    self.ui = Ui_MainWindow ()
    self.ui.setupUi(self)
    
    self.db = QtSql.QSqlDatabase.database( "health_connection") #ανοίγει ταυτόχρονα και η σύνδεση:
    
    print "DB is already opened:", self.db.isOpen ()
    if not self.db.isOpen ():
            
        ok = self.db.open()
        if ok==True:
            print "Database just opened now!"
        else:
            print "Failed to open database!"
        
    ###########year##################################
        
    self.modelYear = QtSql.QSqlQueryModel(self)
    self.modelYear.setQuery('select distinct year from ky_data union select distinct year from pi_data union select distinct year from nosokomeia_data order by year',self.db)
    if self.modelYear.lastError().isValid(): 
             print("Error during year selection")

    self.ui.cboYear.setModel(self.modelYear)
    self.ui.cboYear.setModelColumn(0)
    self.ui.cboYear.setCurrentIndex(-1)
    
  
  


    self.lb=QLabel( )
    self.lb.setFrameStyle(QtGui.QFrame.Panel |QtGui.QFrame.Sunken)
    #add widget label to statusBar
    self.statusBar().addWidget(self.lb,0)
    
  
  
    #====================signals and slots ========================================================================================
    self.ui.cboYear.currentIndexChanged['QString'].connect(self.yearChanged)
    self.ui.lineEdit.textChanged.connect(self.setFilterPer_iatreia)
    self.ui.action_zoom.triggered.connect(lambda: self.zoomToPer_Iatreia(self.ui.tableView,self.proxyModel_per_iatreia, self.primary_key))
    
    self.ui.action_showmap.triggered.connect(self.displayonMap)
    #==============================================================================================================================
    
    
    self.ui.action_zoom.setEnabled(False)  # disable zoom button
    self.ui.action_showmap.setEnabled(False)  # disable show map button

  def displayonMap(self):       
        
        try:
            assert self.year != None

        except AssertionError as e:
            QMessageBox.information(None, u"Ενημέρωση!", u"Παρακαλώ επιλέξτε Έτος!")
            return
       
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        #print self.sqlsource.encode('utf-8')

                #fieldalias= {'0':"test", '1':"lll"}
        #self.setFieldsAlias(**fieldalias)
        geomfields= self.mylayer.getGeomFields()
        for geofield in geomfields:
            if geofield.name == "the_geom":
                break
        self.vlayer=addPostGISLayer(HOST,PORT,DBNAME,USERNAME, PASSWORD,'',u"(%s)" %self.fun_sql,u"%s-Έτος %s" %(self.mylayer.alias, str(self.year)),geofield.name , self.primary_key.name)

        #Set Attribute Editor Layout to TabLayout
        self.vlayer.setEditorLayout(QgsVectorLayer.TabLayout)
        #Define tabs
        

                
            
        tab1 = QgsAttributeEditorContainer(u"Δεδομένα", self.vlayer)
        tab2 = QgsAttributeEditorContainer(u"Γεωγραφικός εντοπισμός", self.vlayer)
        tab3 = QgsAttributeEditorContainer(u"Στατιστικά στοιχεία", self.vlayer)
        
          
        for field in self.mylayer.fields:
            self.vlayer.addAttributeAlias(self.vlayer.fieldNameIndex(field.name),field.alias) #set alias
            
            if field.ishidden()==True:
                if self.vlayer.fieldNameIndex(field.name) ==-1:
                    print "%s not found" %field.name 
                    continue
                self.vlayer.setEditType(int(self.vlayer.fieldNameIndex(field.name)), QgsVectorLayer.Hidden ) 
                print "%s is hidden" %field.name 
            else:
                widget = QgsAttributeEditorField(field.name,  self.vlayer.fieldNameIndex(field.name),  self.vlayer);
                if field.tabCategory==1:
                    tab1.addChildElement(widget) 
                if field.tabCategory==2:
                    tab2.addChildElement(widget) 
                if field.tabCategory==3:
                    tab3.addChildElement(widget) 
                  
          
             #Add to attributeEditorElements of layer
            self.vlayer.clearAttributeEditorWidgets()
            self.vlayer.addAttributeEditorWidget(tab1)
            self.vlayer.addAttributeEditorWidget(tab2)
            self.vlayer.addAttributeEditorWidget(tab3)

        #add to map
        QgsMapLayerRegistry.instance().addMapLayers([self.vlayer])
        QApplication.restoreOverrideCursor()

#==============================================================================================================================      
  def setFieldsAlias(self, **kwargs):
    for key, value in kwargs.iteritems():
        self.vlayer.addAttributeAlias(int(key),value)
        
#==============================================================================================================================           
  def yearChanged(self,year):

   # ====================Περιφερειακά ιατρεία ή κέντρα υγεία====================================================================================   
    
    QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
    self.year= int(year)
    self.fun_sql = "select * from %s(%i)" % (self.mytable, self.year)
    
   
    self.per_iatreiaModel = QtSql.QSqlQueryModel(self)
    self.per_iatreiaModel.setQuery(self.fun_sql,self.db)
    
    self.sortColumn=self.per_iatreiaModel.record().indexOf(self.mylayer.SortColumn.name)
    self.filterColumn=self.per_iatreiaModel.record().indexOf(self.mylayer.FilterColumn.name)
    
    for field in self.mylayer.fields:
        columnindex=self.per_iatreiaModel.record().indexOf(field.name)
        self.per_iatreiaModel.setHeaderData(int(columnindex), QtCore.Qt.Horizontal, field.alias)


    
    #===========================================================================
    # if self.kwargs_headers is not None:
    #     for key, value in self.kwargs_headers.iteritems():
    #         self.per_iatreiaModel.setHeaderData(int(key), QtCore.Qt.Horizontal, value)
    #        
    #===========================================================================

    
    
    #self.per_iatreiaModel.select()
    self.proxyModel_per_iatreia = QtGui.QSortFilterProxyModel()
    self.proxyModel_per_iatreia.setSourceModel(self.per_iatreiaModel)
    self.proxyModel_per_iatreia.setFilterKeyColumn(self.filterColumn)



    
    self.ui.tableView.setModel(self.proxyModel_per_iatreia)
    self.ui.tableView.setVisible(False)
    self.ui.tableView.resizeColumnsToContents()
    self.ui.tableView.setVisible(True)
    self.ui.tableView.setSortingEnabled(True)
    self.ui.tableView.setAlternatingRowColors(True)
    self.ui.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
    self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
    self.ui.tableView.verticalHeader().setVisible(False)
    self.ui.tableView.sortByColumn(self.sortColumn, QtCore.Qt.AscendingOrder)#κάνω το sort στο tableview γιατί στο QSortFilterProxyModel δεν δουλεύει όταν το datasource είναι QSqlQueryModel

    
    # Hide some columns
    for field in self.mylayer.fields:
        if field.ishidden()==True:
            columnIndex = self.per_iatreiaModel.record().indexOf(field.name)
            self.ui.tableView.setColumnHidden(columnIndex, True) 
      
    QApplication.restoreOverrideCursor()
    # Hide some columns
    #===========================================================================
    # self.columnsToHide = self.args_hide
    # for column in self.columnsToHide:
    #     self.ui.tableView.setColumnHidden(column, True) 
    if self.proxyModel_per_iatreia.rowCount()>0:
        self.ui.action_zoom.setEnabled(True)  # disable zoom button
        self.ui.action_showmap.setEnabled(True)  # disable show map button
    if self.proxyModel_per_iatreia.rowCount()==0:
        self.ui.action_zoom.setEnabled(False)  # disable zoom button
        self.ui.action_showmap.setEnabled(False)  # disable show map button
    
    self.lb.setText(u"Σύνολο εγγραφών:%s" %self.proxyModel_per_iatreia.rowCount())
    self.ui.tableView.selectionModel().selectionChanged.connect (self.zoomNow)
    #===========================================================================
  #==============================================================================================================================           
  def setFilterPer_iatreia(self,newtext):
      myfilter =u".*{!s}".format(newtext)
      filterString = QtCore.QRegExp(myfilter,QtCore.Qt.CaseInsensitive,QtCore.QRegExp.RegExp)
      self.proxyModel_per_iatreia.setFilterRegExp(filterString)

  #==============================================================================================================================      
  def zoomNow(self, currentListItem, previousListItem):
    if self.ui.checkBox.isChecked():
        self.zoomToPer_Iatreia(self.ui.tableView,self.proxyModel_per_iatreia, self.primary_key.name)
  
  #==============================================================================================================================    
  

  def zoomToPer_Iatreia(self, myview, mymodel,  searchfield):
      try:
          
         #αναζήτηση αν υπάρχει ήδη το συγκεκριμένο layer πριν ανοίξει η φόρμα με τους δείκτες
        print (u"%s-Έτος %s" %(self.mylayer.alias, str(self.year)))
        layers_by_name = QgsMapLayerRegistry.instance().mapLayersByName (u"%s-Έτος %s" %(self.mylayer.alias, str(self.year)))
        
        if len(layers_by_name)>=1: # αν βρεθεί ένα η παραπάνω layer με το ίδιο όνομα τότε παρε το πρώτο
            zoomlayer=layers_by_name[len(layers_by_name)-1]


        if len(layers_by_name)==0: # αν βρεθεί τότε
            raise AttributeError
        


         
        listviewindex =myview.selectionModel().selection()
        columnindexbyName=self.per_iatreiaModel.record().indexOf(self.mylayer.keyfield.name)
        myindex = mymodel.index(listviewindex.indexes()[0].row(),columnindexbyName) #6= index of column KODIKOS in model
        KODIKOS = mymodel.data(myindex,0)
        print KODIKOS, zoomlayer
        
        #self.zoomTo(self.layerPI, searchfield, KODIKOS)
        self.zoomTo(zoomlayer, str(self.mylayer.keyfield.name), KODIKOS)


    
      except IndexError:
          QMessageBox.information(None, u"Ενημέρωση!", u"Παρακαλώ επιλέξτε ένα στοιχείο από την αντίστοιχη λίστα")
      except AttributeError:
          QMessageBox.information(None, u"Ενημέρωση!", u"Το θεματικό επίπεδο δεν εντοπίστηκε. Παρακαλώ οπτικοποιήστε τo θεματικό επίπεδο!")
    
  
  def zoomTo(self, layer, searchfield, value):
      #first clear any selection on map canvas

      
      try:
        self.it = layer.getFeatures( QgsFeatureRequest().setFilterExpression ( u'"%s" = \'%s\'' % (searchfield,str(value)) ) )
        
        if len(list(self.it) )==0:
            QMessageBox.information(None,u"Ενημέρωση!",u"Δεν βρέθηκε το αντικείμενο στο θεματικό επίπεδο:%s!" %layer.name())
            return
            
        del self.it
        self.it = layer.getFeatures( QgsFeatureRequest().setFilterExpression (u'"%s" = \'%s\'' % (searchfield,str(value)) ) )     
        
        self.iface.setActiveLayer(layer)
        layer.setSelectedFeatures( [ f.id() for f in self.it ] )
      
        box = layer.boundingBoxOfSelected()
        self.iface.mapCanvas().setExtent(box)
        self.iface.mapCanvas().refresh()

        
        #self.canvas.zoomToSelected()
      except AttributeError:
        QMessageBox.information(None,u"Ενημέρωση!",u"Δεν βρέθηκε το απαραίτητο θεματικό επίπεδο ή δεν είναι ενεργό")
    
  #=============================================================================



    