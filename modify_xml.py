# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 13:47:46 2023

@author: ielmartin
"""

# Script to add timeseries data to existing cim file ---TO BE INCLUDED IN MAIN SCRIPT/GUI---

import numpy as np
import xml.etree.ElementTree as ET
from import_cim import data_extract
from xml_functions import conform_load_converter, load_ts2cim, gen_opsch2cim, gen_mea2cim, write_output

def cim_timeseries(eq, eq_xml, ns_dict, ns_register, loads, gens, timesteps, tstep_length):
    
    #---LOADS---
    # convert loads from EnergyConsumer class to ConformLoad class 
    conform_load_converter(eq, ns_dict, loads)
    
    # generate relevant cim classes to incorporate timeseries for loads
    load_ts2cim(eq, ns_dict, ns_register, loads, timesteps, tstep_length)
    
    
    #---GENERATORS---
    
    unit_commitment = ['HydroGeneratingUnit', 'ThermalGeneratingUnit', 'NuclearGeneratingUnit']
    for gen_type in gens:
        if gen_type: # Do only for selected generators 
        
            # for generators using the GenUnitOpSchedule class for timeseries
            if gen_type.element_type in unit_commitment:                  
                gen_opsch2cim(eq, ns_dict, ns_register, gen_type, timesteps, tstep_length)
            
            # for generators using the Measurement class for timeseries
            else:
                gen_mea2cim(eq, ns_dict, ns_register, gen_type, timesteps, tstep_length)
    
    return eq_xml
    
    
