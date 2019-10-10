# -*- coding: utf-8 -*-
from PyQt4 import QtCore, QtGui, QtSql, QtNetwork
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtNetwork import *
from Ui_map_settings import frm_map_settins_Dialog
from frm_deiktes import Ui_MainWindow
from myfunctions import *
from mysettings import  *
from qgis.core import *
import ConfigParser
import os
import time
import ast
from genericthread import GenericThread
import deiktesnames


# create the dialog for paradosiakoioikismoi
class deiktes3_Dialog(QtGui.QMainWindow):
    '''Class to handle medical data'''       
        
    def __init__(self, iface): 
      
        QtGui.QMainWindow.__init__(self) 
    
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.deiktisModel = QtSql.QSqlQueryModel(self)
    
         # Set up the user interface from Designer. 
        self.ui = Ui_MainWindow ()
        self.ui.setupUi(self)
    
        self.db = QtSql.QSqlDatabase.database("health_connection")  # ανοίγει ταυτόχρονα και η σύνδεση:

        print "DB is already opened:", self.db.isOpen ()
        if not self.db.isOpen ():
            
            ok = self.db.open()
            if ok == True:
                print "Database just opened now!"
            else:
                print "Failed to open database!"


        self.ui.action_zoom.triggered.connect(lambda: self.zoomToKY(self.ui.tableView, self.proxyModel_deiktis))

        self.ui.action_showmap.triggered.connect(self.displayonMap)

        self.ui.action_zoom.setIconText(u'Εστίαση στο επιλεγμένο στοιχείο της λίστας')
        self.ui.action_zoom.setToolTip(u'Εστίαση στο επιλεγμένο στοιχείο της λίστας')
        self.ui.action_zoom.setStatusTip(u'Εστίαση στο επιλεγμένο στοιχείο της λίστας')     
        
        self.ui.action_showmap.setIconText(u'Οπτικοποίηση δείκτη στον χάρτη')
        self.ui.action_showmap.setToolTip(u'Οπτικοποίηση δείκτη στον χάρτη')
        self.ui.action_showmap.setStatusTip(u'Οπτικοποίηση δείκτη στον χάρτη')     
                
        self.ui.action_zoom.setEnabled(False)  # disable zoom button
        self.ui.action_showmap.setEnabled(False)  # disable show map button
        
         ###########year##################################
        
        self.modelYear = QtSql.QSqlQueryModel(self)
        
        self.modelYear.setQuery('select distinct year from ky_data union select distinct year from pi_data union select distinct year from nosokomeia_data order by year',self.db)
        if self.modelYear.lastError().isValid(): 
             print("Error during year selection")

        self.ui.cboYear.setModel(self.modelYear)
        self.ui.cboYear.setModelColumn(0)
        self.ui.cboYear.setCurrentIndex(0)
        
        self.ui.cboYear.currentIndexChanged['QString'].connect(self.yearChanged)
        
        self.year=self.modelYear.record(0).value(0)
        print "Year:%s" %self.year

        #QTREEVIEW
        self.ui.treeView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels([u'ΔΕΙΚΤΕΣ', 'col2', 'col3'])
        self.ui.treeView.setModel(self.model)
        self.ui.treeView.setUniformRowHeights(True)

        self.modelEidikotites = QtSql.QSqlQueryModel(self)
        self.modelEidikotites.setQuery('select distinct eidikotita from iatroi',self.db)
        if self.modelEidikotites.lastError().isValid(): 
             print("Error during data selection")

        #build indexes dynamic from sql in postgresql
        for row in range(self.modelEidikotites.rowCount()):

            deiktis_dict={}

            deiktis_dict['label']=u"Σύνολο Ιδιωτών Ιατρών (Ειδικότητας:{!s}) ανά κάτοικο (‰)".format(self.modelEidikotites.record(row).value(0))
            deiktis_dict['sql']=u'''select elstatid2011 ,u_description , deiktis  from fun_deiktis_21122('%s')''' % self.modelEidikotites.record(row).value(0)
            deiktis_dict['hideColumns']=[0]
            #deiktis_dict['zoomToLayer']='kentra_ygeias'
            deiktis_dict['SearchField']='elstatid2011'
            deiktis_dict['OnlyAdd']=False
            deiktis_dict['perYearData']=False

            deiktesnames.deiktes[u"Δείκτες Επάρκειας Υγειονομικής Κάλυψης (ανά δήμο)"].append(deiktis_dict)

        counter=0
        for k,v in sorted(deiktesnames.deiktes.iteritems()):
            name= k
            subcategories= v
            #print name, subcategories
            parent1 = QStandardItem(QIcon(":/plugins/ygeia/icons/1412622185_first_aid_kit.png"),name)
            
            for value in subcategories:
                dic= value
        
                child = QStandardItem(QIcon(":/plugins/ygeia/icons/1412622284_bullet_go.png"), dic['label'])
                child.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled)
        
                child2=QStandardItem(dic['sql'])
                child3=QStandardItem(str(dic['hideColumns']))
                #child4=QStandardItem(dic['zoomToLayer'])
                child4=QStandardItem(str(dic['SearchField']))
                child5=QStandardItem(str(dic['OnlyAdd']))
                child6=QStandardItem(str(dic['perYearData']))

                parent1.appendRow([child,child2,child3,child4,child5,child6])
                parent1.setFlags(Qt.ItemIsSelectable | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled  )
        
            self.model.appendRow(parent1)
            self.ui.treeView.setFirstColumnSpanned(counter, self.ui.treeView.rootIndex(), True)
            #index = self.model.indexFromItem(parent1)
            #self.ui.treeView.expand(index)
            counter+=1
        
        #hide columns
        self.ui.treeView.setColumnHidden ( 1,True)
        self.ui.treeView.setColumnHidden ( 2,True)
        self.ui.treeView.setAlternatingRowColors(True)

        self.ui.treeView.header().hide()
        #self.ui.treeView.connect(self.ui.treeView.selectionModel(), SIGNAL("selectionChanged(QItemSelection, QItemSelection)"), self.on_selection_changed)
        self.ui.treeView.selectionModel().selectionChanged.connect(self.on_selection_changed)      

        #self.ui.frame.hide()
        self.ui.groupBox.setStyleSheet("QGroupBox::title {font-weight:bold; background-color: rgb(255,250,205); border:1px solid rgb(40, 40, 40);padding: 3 3px; }")
        
        self.lb=QLabel( )
        self.lb.setFrameStyle(QtGui.QFrame.Panel |QtGui.QFrame.Sunken)
        self.statusBar().addWidget(self.lb,0)
        self.lb.hide()
        
        self.status_txt = QtGui.QLabel()
        movie = QtGui.QMovie(":/plugins/ygeia/icons/Progressbar.gif")

        self.status_txt.setMovie(movie)
        movie.start()
        self.statusBar().addWidget(self.status_txt,1)
        self.status_txt.hide()   

    #==============================================================================================================================           
    def yearChanged(self,year):

      self.year = int(year)
      QMessageBox.warning(None,u"Ενημέρωση!",u"Παρακαλώ επιλέξτε δείκτη για το έτος %s." % str(self.year))      
   
    #==============================================================================================================================           
    def on_selection_changed(self,next, previous):
        try:
            QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

            self.label = unicode(self.model.data(next.indexes ()[0], 0))
            sql = unicode(self.model.data(next.indexes ()[1], 0))
            hidecolumns = ast.literal_eval(unicode(self.model.data(next.indexes ()[2], 0)))
            #zoomToLayer = self.model.data(next.indexes ()[3], 0)
            SearchField = unicode(self.model.data(next.indexes ()[3], 0))
            OnlyAdd = ast.literal_eval(unicode(self.model.data(next.indexes ()[4], 0)))
            
            perYearData= ast.literal_eval(unicode(self.model.data(next.indexes ()[5], 0)))
            
            if not perYearData:
                self.ui.cboYear.setDisabled(True)
                self.lb.setText(u"Ο δείκτης δεν περιλαμβάνει χρονοσειρές")
                self.sqlsource = sql # the table name or sql query string
                 #add widget label to statusBar

            else:
                self.ui.cboYear.setDisabled(False)
                self.lb.setText(u"Έτος: %s" %str(self.year))
                self.sqlsource = sql+"(%s)"%self.year  # the table name or sql query string
            
            self.sqlsourceformap=u"(%s)" %geomSql(self.sqlsource )#the table name or sql query string    

            print "perYearData: ", perYearData
            
            print 'Search Field:',SearchField
            
            #print self.year
              
            """Handler called when a index is chosen from the combo box"""
          
            self.styled_layer = None  # πρέπει να γίνει έτσι γιατί αλλιώς το zoom θα παέι σε λάθος layer

            self.itemtext = self.label
            self.itemdata = sql

            self.columnsToHide = hidecolumns  # columns to hide
            #self.zoomlayername = zoomToLayer  # layer to zoom
    
            self.zoomsearchfield = SearchField  # field with id to search
          
            self.OnlyAdd = OnlyAdd  # just add in map canvas of classify, True=add, False=Classify

    
            # initialize threads and disconnect and reconnect signals to fuctions
            self.genericThread3 = GenericThread(self.loadmydata)
            #self.disconnect(self, QtCore.SIGNAL("sendpositions"), self.write_kml)
            self.disconnect(self, QtCore.SIGNAL("dataloaded"), self.setupmyview)

            #self.connect(self, QtCore.SIGNAL("updateprogressbar"), lambda i: self.progressbar.setValue(i))
            self.connect(self, QtCore.SIGNAL("dataloaded"), self.setupmyview)

            self.lb.show()
            
            self.genericThread3.start()

            self.status_txt.show()

            #self.loadmydata()

            #self.setupmyview()
     
        except IndexError:
            print 'Category title selected'
        finally:
            QApplication.restoreOverrideCursor()
      
      
    def alginfo(self):
        QMessageBox.information(None, u"Ενημέρωση!", u"Υπολογισμός δείκτη σε εξέλιξη...") 
    
    def loadmydata(self):
        
        self.ui.treeView.setSelectionMode(QAbstractItemView.NoSelection)# disable selection on qtreeview items
        self.ui.treeView.selectionModel().selectionChanged.disconnect(self.on_selection_changed)
        self.ui.treeView.selectionModel().selectionChanged.connect(self.alginfo)


        self.deiktisModel.setQuery(self.sqlsource, self.db)
    
    
        if self.deiktisModel.lastError().isValid(): 
            print self.deiktisModel.lastError();
            print self.deiktisModel.lastError().text() 
            
        while self.deiktisModel.canFetchMore():
            self.deiktisModel.fetchMore()

        self.emit(QtCore.SIGNAL('dataloaded'))
        
    def setupmyview(self):

        self.proxyModel_deiktis = QtGui.QSortFilterProxyModel()
        self.proxyModel_deiktis.setSortLocaleAware(True)
        self.proxyModel_deiktis.setSourceModel(self.deiktisModel)


    
        self.ui.tableView.setModel(self.proxyModel_deiktis)
        self.ui.tableView.setVisible(False)
        self.ui.tableView.resizeColumnsToContents()
        self.ui.tableView.setVisible(True)
        self.ui.tableView.setSortingEnabled(True)
        self.ui.tableView.setSelectionMode(QtGui.QAbstractItemView.SingleSelection)
        self.ui.tableView.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.ui.tableView.sortByColumn(2, QtCore.Qt.DescendingOrder)  # κάνω το sort στο tableview γιατί στο QSortFilterProxyModel δεν δουλεύει όταν το datasource είναι QSqlQueryModel
        self.ui.tableView.verticalHeader().setVisible(False)
        self.ui.tableView.setAlternatingRowColors(True)

        # Rename column headers
        for column,value in deiktesnames.columnnames.iteritems():
            columnindex = self.deiktisModel.record().indexOf(column)
            if columnindex>=0:
                self.proxyModel_deiktis.setHeaderData(columnindex, Qt.Horizontal, value)

        # First show again all columns
        for column in range(self.proxyModel_deiktis.columnCount()):
            self.ui.tableView.setColumnHidden(column, False)
               
        # And then ...
             
        # Hide some columns          
        for column in self.columnsToHide:
            self.ui.tableView.setColumnHidden(column, True)
          
        self.ui.action_zoom.setEnabled(True)  # enable zoom 
        self.ui.action_showmap.setEnabled(True)  # enable show map button
            
        self.ui.groupBox.setTitle(u'Δείκτης: %s-Έτος: %s' % (self.label,str(self.year)))

        self.status_txt.hide()

        self.ui.treeView.selectionModel().selectionChanged.disconnect(self.alginfo)
        self.ui.treeView.selectionModel().selectionChanged.connect(self.on_selection_changed)
        self.ui.treeView.setSelectionMode(QAbstractItemView.SingleSelection) # enable selection on qtreeview items

    def displayonMap(self):

        print self.sqlsourceformap.encode('utf-8')
        self.vlayer=addPostGISLayer(HOST,PORT,DBNAME,USERNAME, PASSWORD,'',self.sqlsourceformap ,self.itemtext + "-(%s)"%self.year,'the_geom' , self.zoomsearchfield)
        for column, name in deiktesnames.columnnames.iteritems():
             columnindex=self.vlayer.fieldNameIndex(column)
             self.vlayer.addAttributeAlias(columnindex,name)

        if self.OnlyAdd:
             self.styled_layer = self.vlayer
             QgsMapLayerRegistry.instance().addMapLayers([self.vlayer])
             return
           
        self.dlg = frm_map_settins_Dialog()

        result = self.dlg.exec_()
        
        numClasses=self.dlg.ui.spinBox.value()
        index=self.dlg.ui.comboBox.currentIndex()
        classMethod =self.dlg.ui.comboBox.itemData(index)

        if result==1:

            if self.vlayer.isValid():
                self.styled_layer = applyGraduatedSymbologyStandardMode(self.vlayer, u'deiktis', numClasses, classMethod)
                
                if classMethod==3:
                   self.styled_layer = updatecolors(self.styled_layer, u'deiktis')
            
                QgsMapLayerRegistry.instance().addMapLayers( [self.styled_layer] ) 

    def zoomToKY(self, myview, mymodel):
      try:

        #αναζήτηση αν υπάρχει ήδη το συγκεκριμένο layer πριν ανοίξει η φόρμα με τους δείκτες
        layers_by_name = QgsMapLayerRegistry.instance().mapLayersByName (self.itemtext)
        
        if len(QgsMapLayerRegistry.instance().mapLayersByName (self.itemtext))==1: # αν βρεθεί τότε
            zoomlayer=layers_by_name[0]
        else: # αν δεν βρεθεί τότε αν έχει προστεθεί από την τρέχουσα φόρμα όρισε το zoom layer στο layer αυτό
            zoomlayer=self.styled_layer      

        self.iface.setActiveLayer(zoomlayer) 
         
        listviewindex = myview.selectionModel().selection()
        myindex = mymodel.index(listviewindex.indexes()[0].row(), 0)  # 6= index of column KODIKOS in model
        KODIKOS = mymodel.data(myindex, 0)
        
        self.zoomTo(zoomlayer, str(self.zoomsearchfield), KODIKOS)

      except IndexError:
          QMessageBox.information(None, u"Ενημέρωση!", u"Παρακαλώ επιλέξτε ένα στοιχείο από την αντίστοιχη λίστα")
      except AttributeError:
          QMessageBox.information(None, u"Ενημέρωση!", u"Το θεματικό επίπεδο \"%s\"-(%s) -δεν εντοπίστηκε. Παρακαλώ οπτικοποιήστε τον δείκτη!" %(self.itemtext,self.year))

    def zoomTo(self, layer, searchfield, value):
      try:
        self.it = layer.getFeatures(QgsFeatureRequest().setFilterExpression (u'"%s" = \'%s\'' % (searchfield, str(value))))

        if len(list(self.it)) == 0:
            QMessageBox.information(None, u"Ενημέρωση!", u"Δεν βρέθηκε το αντικείμενο στο θεματικό επίπεδο:%s!" % layer.name())
            return
            
        del self.it
        self.it = layer.getFeatures(QgsFeatureRequest().setFilterExpression (u'"%s" = \'%s\'' % (searchfield, str(value))))     
        
        layer.setSelectedFeatures([ f.id() for f in self.it ])
        self.canvas.zoomToSelected()
      except AttributeError:
        QMessageBox.information(None, u"Ενημέρωση!",u"Το θεματικό επίπεδο \"%s\"-(%s) -δεν εντοπίστηκε. Παρακαλώ οπτικοποιήστε τον δείκτη!" %(self.itemtext,self.year))




    
