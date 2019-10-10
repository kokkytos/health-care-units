# -*- coding: utf-8 -*-
from types import *

class TabCategory(object):
        tab1 = 1
        tab2 = 2
        tab3 = 3




class myfield:
    def __init__(self, name, alias, hidden=False, geomField=False, tabCategory=TabCategory.tab1):
        self.name = name
        self.alias = alias
        self.hidden = hidden
        self.geomField = geomField
        self.tabCategory = tabCategory

        
    def hide(self):
        self.hidden = True
    def ishidden(self):
        return self.hidden
    def isgeomField(self):
        return self.geomField


class mylayer:
    def __init__(self, name, alias):
        self.name = name
        self.fields = []
        self.keyfield = None
        self.FilterColumn = None
        self.SortColumn = None
        self.alias = alias
        self.geomField = []
        self.sql = None
        self.year = None

    
    def addField(self, field):
        self.fields.append(field)
        
        
    def setPkey(self, name):
        for field in self.fields:
            if field.name == name:
                self.keyfield = field
                return self.keyfield
            
            
    def setFilterColumn(self, name):
        for field in self.fields:
            if field.name == name:
                self.FilterColumn = field
                return self.FilterColumn
            
    def setSortColumn(self, name):
        for field in self.fields:
            if field.name == name:
                self.SortColumn = field
                return self.SortColumn          
                                
    def getGeomFields(self):
        for field in self.fields:
            if field.isgeomField() == True:
                self.geomField.append(field)
        return self.geomField
        
    def getFieldbyName(self, name):
        for field in self.fields:
            if field.name == name:
                return field
                
    def setSql(self, sql):
        self.sql = sql
    
    def getSql(self):
        return self.sql
   
    def setYear(self, year):
        assert type(year) is IntType, "Year is not an integer: %r" % id
        self.year = int(year)
    
    def getYear(self):
        return self.year     
