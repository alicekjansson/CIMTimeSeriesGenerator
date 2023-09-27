# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:35:49 2023

@author: ielmartin
"""

#This is the main script which runs the program

import pandas as pd
import numpy as np
import PySimpleGUI as sg
import xml.etree.ElementTree as ET
from import_cim import data_extract
from xml_functions import register_all_namespaces, write_output
from modify_xml import cim_timeseries
from gui_functions import start_gui

ns_dict = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'md':"http://iec.ch/TC57/61970-552/ModelDescription/1#",
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}


gui = 1
if gui == 1:
    start_gui()
# --- NOT GUI
else:
    eq_file = '20171002T0930Z_NL_EQ_3.xml'
    ssh_file = '20171002T0930Z_1D_NL_SSH_3.xml'
    eq_xml = ET.parse(eq_file)
    ssh_xml = ET.parse(ssh_file)
    eq = eq_xml.getroot()
    ssh = ssh_xml.getroot()        
    # Here, functions to generate timeseries    
    loads, pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens = data_extract(eq, ssh, ns_dict)
    gens = [pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens]
    
    # register namspaces for printing in output (see function)
    ns_register = register_all_namespaces(eq_file)
    
    # generate cim file
    indata = 'timeseries for loads and generators'
    cim_timeseries(eq, eq_xml, ns_dict, ns_register, loads, gens, indata)
    print('success ')
