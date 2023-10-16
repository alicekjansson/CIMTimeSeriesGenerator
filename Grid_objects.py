# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:30:32 2023

MIT License

Copyright (c) 2023 Alice Jansson, Martin Lundberg
"""

import pandas as pd
import numpy as np


# superclass of all grid objects
class GridObjects:
    
    def __init__(self, eq, ssh, ns, element_type):

        # for each resource class instance save basic data such as ID and name of resources
        self.df=pd.DataFrame()
        self.element_type = element_type 
        self.eq_list= eq.findall('cim:'+element_type,ns)
        self.ssh_list= ssh.findall('cim:'+element_type,ns)
        self.df['ID']=[element.attrib.get(ns['rdf']+'ID') for element in self.eq_list]
        self.df['name']=[element.find('cim:IdentifiedObject.name',ns).text for element in self.eq_list]
        
# Loads class, extracting all EnergyConsumer instances         
class Loads(GridObjects):
    
    def __init__(self, eq, ssh, ns, element_type = "EnergyConsumer"):
        super().__init__(eq, ssh, ns, element_type)
        
        load_p = []
        load_q = []
        load_cosphi = []
        
        # for loads store active and reactive power from input SSH file, compute power factor for display in GUI
        for load_id in self.df['ID']:   
            for element in self.ssh_list:
                if '#' + load_id  == element.attrib.get(ns['rdf']+'about'):
                    p_val = element.find('cim:EnergyConsumer.p',ns).text
                    q_val = element.find('cim:EnergyConsumer.q',ns).text
                    load_p.append(p_val)
                    load_q.append(q_val)
                    p = float(p_val)
                    q = float(q_val)
                    load_cosphi.append(np.cos(np.arctan(q/p)))
                    
        self.df['p']=load_p
        self.df['q']=load_q
        self.df['cosphi']=load_cosphi

# Generators class, extracting all generator instances of types specified in import_cim.py
class Generators(GridObjects):
    
    def __init__(self,eq,ssh,ns, element_type, gen_type):
        super().__init__(eq, ssh, ns, element_type)
        
        self.gen_type = gen_type
        
        init_p = []
        nom_p = []
        max_p = []
        min_p = []
        
        # for generators store active power (initial/nominal/max/min) from input EQ file
        for element in self.eq_list:
            init_p.append(element.find('cim:GeneratingUnit.initialP',ns).text)
            nom_p.append(element.find('cim:GeneratingUnit.nominalP',ns).text)
            max_p.append(element.find('cim:GeneratingUnit.maxOperatingP',ns).text)
            min_p.append(element.find('cim:GeneratingUnit.minOperatingP',ns).text)
            
         
        self.df['init_p']=init_p
        self.df['nom_p']=nom_p
        self.df['max_p']=max_p
        self.df['min_p']=min_p
        