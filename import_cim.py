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
    element_type = 'EnergyConsumer'
    if eq.findall('cim:'+element_type,ns):
        loads = Loads(eq, ssh, ns)
    else:
        loads = False
    
    # Create conform and nonconform loads?
    # conform loads = loads/load grouos scale from one common profile. See full grid model
    # nonconform loads = individual profiles for each load/load group. See full grid model
    
    
    # if PVs in data create PV class and extract required data  
    element_type = 'PhotoVoltaicUnit'
    if eq.findall('cim:'+element_type,ns):
        gen_type = 'PV'
        pv_gens = Generators(eq, ssh, ns, element_type, gen_type)
    else:
        pv_gens = False
    # if Hydro in data create Hydro class and extract required data  
    element_type = 'HydroGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        gen_type = 'HYDRO'
        hydro_gens = Generators(eq, ssh, ns, element_type, gen_type)
    else:
        hydro_gens = False
    # if Wind in data create Wind class and extract required data  
    element_type = 'WindGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        gen_type = 'WIND POWER'
        wind_gens = Generators(eq, ssh, ns, element_type, gen_type)
    else:
        wind_gens = False
    # if Thermal in data create Thermal class and extract required data  
    element_type = 'ThermalGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        gen_type = 'CHP'
        thermal_gens = Generators(eq, ssh, ns, element_type, gen_type)
    else:
        thermal_gens = False
    # if Nuclear in data create Nuclear class and extract required data  
    element_type = 'NuclearGeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        gen_type = 'NUCLEAR'
        nuclear_gens = Generators(eq, ssh, ns, element_type, gen_type)
    else:
        nuclear_gens = False
    # if undefined generating units in data create undef class and extract required data  
    element_type = 'GeneratingUnit'
    if eq.findall('cim:'+element_type,ns):
        gen_type = 'UNDEFINED'
        undef_gens = Generators(eq, ssh, ns, element_type, gen_type)
    else:
        undef_gens = False
        
    # Manage slack gen?
    # External grids?    
    # INCLUDE ALSO EnergySource? only voltage angle?
    
    return loads, pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens
    


        
        