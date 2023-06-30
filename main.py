# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:35:49 2023

@author: ielmartin
"""

import pandas as pd
import PySimpleGUI as sg
import xml.etree.ElementTree as ET
from import_cim import data_extract

ns = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}',
      'md':"http://iec.ch/TC57/61970-552/ModelDescription/1#"}


#-----GUI------
gui = 0

if gui == 1:
    layout = [[sg.Text('Enter the required CGMES CIM/XML files')],
              [sg.Text('EQ File', size=(8, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('SSH File', size=(8, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('Enter other input data')],
              [sg.Text('Data', size=(8, 1)), sg.Input()],
              [sg.Submit('Generate Timeseries')]]
    
    # Create the window
    window = sg.Window('CIM Timeseries Generator', layout)
    
    # Parse input files
    event, values = window.read()
    eq_xml = values[0]
    ssh_xml = values[1]
    eq = ET.parse(eq_xml).getroot()
    ssh = ET.parse(ssh_xml).getroot()        
            
    data_extract(eq, ssh, ns)
    print('success')
    
    window.close()
       
# --- NOT GUI
else:
    eq_xml = ET.parse('20171002T0930Z_NL_EQ_3.xml')
    ssh_xml = ET.parse('20171002T0930Z_1D_NL_SSH_3.xml')
    eq = eq_xml.getroot()
    ssh = ssh_xml.getroot()        
            
    data_extract(eq, ssh, ns)
    print('success1')
