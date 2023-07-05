# -*- coding: utf-8 -*-
"""
Created on Mon Jul  3 13:47:46 2023

@author: ielmartin
"""

# Script to add timeseries data to existing cim file

import xml.etree.ElementTree as ET
from import_cim import data_extract
from xml_functions import register_all_namespaces, conform_load_converter, load_ts2cim, write_output



#---main part of script---

ns_dict = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'md':"http://iec.ch/TC57/61970-552/ModelDescription/1#",
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}


# register namspaces (see function)
ns_register = register_all_namespaces('20171002T0930Z_NL_EQ_3.xml')
# parse cim file
eq_xml = ET.parse('20171002T0930Z_NL_EQ_3.xml')
ssh_xml = ET.parse('20171002T0930Z_1D_NL_SSH_3.xml')
eq = eq_xml.getroot()
ssh = ssh_xml.getroot() 


#get cim data
loads, pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens = data_extract(eq, ssh, ns_dict)


# convert loads from EnergyConsumer class to ConformLoad class 
conform_load_converter(eq, ns_dict, loads)


# some dummy input data
timesteps = 3
p = [1, 2, 3]
q = [1, 2, 3]

# generate relevant cim classes to incorporate timeseries for loads
load_ts2cim(eq, ns_dict, ns_register, loads, timesteps, p, q)

#output updated cim file
filename = 'output'
write_output(eq_xml, filename)
