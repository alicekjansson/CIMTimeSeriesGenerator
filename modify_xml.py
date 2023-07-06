# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 13:47:46 2023

@author: ielmartin
"""

# Script to add timeseries data to existing cim file ---TO BE INCLUDED IN MAIN SCRIPT/GUI---

import numpy as np
import xml.etree.ElementTree as ET
from import_cim import data_extract
from xml_functions import register_all_namespaces, conform_load_converter, load_ts2cim, gen_opsch2cim, gen_mea2cim, write_output


ns_dict = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'md':"http://iec.ch/TC57/61970-552/ModelDescription/1#",
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

# register namspaces for printing in output (see function)
ns_register = register_all_namespaces('20171002T0930Z_NL_EQ_3.xml')
# parse cim file
eq_xml = ET.parse('20171002T0930Z_NL_EQ_3.xml')
ssh_xml = ET.parse('20171002T0930Z_1D_NL_SSH_3.xml')
eq = eq_xml.getroot()
ssh = ssh_xml.getroot() 

#get cim data
loads, pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens = data_extract(eq, ssh, ns_dict)
gens = [pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens]


#---LOADS---

# some dummy load timeseries data (to be replaced by script)
timesteps = 24
tstep_length = 3600 # unit seconds
p_loads = np.random.rand(timesteps, loads.df['ID'].size)
q_loads = np.random.rand(timesteps, loads.df['ID'].size)    

# convert loads from EnergyConsumer class to ConformLoad class 
conform_load_converter(eq, ns_dict, loads)

# generate relevant cim classes to incorporate timeseries for loads
load_ts2cim(eq, ns_dict, ns_register, loads, p_loads, q_loads, timesteps, tstep_length)


#---GENERATORS---

unit_commitment = ['HydroGeneratingUnit', 'ThermalGeneratingUnit', 'NuclearGeneratingUnit']
for gen_type in gens:
    if gen_type: # Do only for selected generators 
    
        # some dummy gen timeseries data (to be replaced by script)
        timesteps = 24
        tstep_length = 3600 # unit seconds
        p_gens = np.random.rand(timesteps, gen_type.df['ID'].size)
    
        
        # for generators using the GenUnitOpSchedule class for timeseries
        if gen_type.element_type in unit_commitment:                  
            gen_opsch2cim(eq, ns_dict, ns_register, gen_type, p_gens, timesteps, tstep_length)
        
        # for generators using the Measurement class for timeseries
        else:
            gen_mea2cim(eq, ns_dict, ns_register, gen_type, p_gens, timesteps, tstep_length)
            

#---OUTPUT---
    
#output updated cim file
filename = 'output'
write_output(eq_xml, filename)
