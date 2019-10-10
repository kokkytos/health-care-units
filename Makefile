# Makefile for ygeia plugin 
UI_FILES = frm_per_iatreia.py frm_deiktes.py frm_dbSettings.py frm_map_settings.py

RESOURCE_FILES = resources.py

default: compile
	
compile: $(UI_FILES) $(RESOURCE_FILES)

%.py : %.qrc
	pyrcc4 -o $@  $<

%.py : %.ui
	pyuic4 -o $@ $<

