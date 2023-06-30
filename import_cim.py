# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 08:34:52 2023

@author: ielmartin
"""

import pandas as pd
from Grid_objects import GridObjects, Loads, Generators

 
def data_extract(eq, ssh, ns):           
    # create load class and extract required data     
    loads = Loads(eq, ssh, ns)
    
    # SEPARATE conform and nonconform loads?
    
    
    # if PVs in data create PV class and extract required data  
    element_type = 'SolarGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        pv_gens = Generators(eq, ssh, ns, element_type)
    # if Hydro in data create Hydro class and extract required data  
    element_type = 'HydroGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        hydro_gens = Generators(eq, ssh, ns, element_type)
    # if Wind in data create Wind class and extract required data  
    element_type = 'WindGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        wind_gens = Generators(eq, ssh, ns, element_type) 
    # if Thermal in data create Thermal class and extract required data  
    element_type = 'ThermalGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        thermal_gens = Generators(eq, ssh, ns, element_type)
    # if Nuclear in data create Nuclear class and extract required data  
    element_type = 'NuclearGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        nuclear_gens = Generators(eq, ssh, ns, element_type)       
    # if undefined generating units in data create undef class and extract required data  
    element_type = 'GeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        undef_gens = Generators(eq, ssh, ns, element_type)
        
    # INCLUDE ALSO EnergySource? only voltage angle?
        
    


        
        