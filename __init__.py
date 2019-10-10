"""
/***************************************************************************
Name			 	 : ygeia
Description          : ygeia
Date                 : 16/Feb/14 
copyright            : (C) 2014 by Leonidas Liakos
email                : leonidas_liakos@yahoo.gr 
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""
def name(): 
  return "ygeia" 
def description():
  return "ygeia"
def version(): 
  return "Version 2.0" 
def qgisMinimumVersion():
  return "2."
def classFactory(iface): 
  
  from ygeiaplg import ygeiaCls 
  return ygeiaCls(iface)
