# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:30:32 2023

@author: ielmartin
"""

import pandas as pd


# superclass of all grid objects
class GridObjects:
    
    def __init__(self, eq, ssh, ns, element_type):

        self.df=pd.DataFrame()
        self.element_type = element_type 
        self.eq_list= eq.findall('cim:'+element_type,ns)
        self.ssh_list= ssh.findall('cim:'+element_type,ns)
        self.df['ID']=[element.attrib.get(ns['rdf']+'ID') for element in self.eq_list]
        self.df['name']=[element.find('cim:IdentifiedObject.name',ns).text for element in self.eq_list]
        
        
class Loads(GridObjects):
    
    def __init__(self, eq, ssh, ns, element_type = "EnergyConsumer"):
        super().__init__(eq, ssh, ns, element_type)
        
        load_p = []
        load_q = []
        for load_id in self.df['ID']:   
            for element in self.ssh_list:
                if '#' + load_id  == element.attrib.get(ns['rdf']+'about'):
                    load_p.append(element.find('cim:EnergyConsumer.p',ns).text)
                    load_q.append(element.find('cim:EnergyConsumer.q',ns).text)
        self.df['p']=load_p
        self.df['q']=load_q
        
        
class Generators(GridObjects):
    
    def __init__(self,eq,ssh,ns, element_type):
        super().__init__(eq, ssh, ns, element_type)
        
        init_p = []
        nom_p = []
        max_p = []
        min_p = []
        
        for element in self.eq_list:
            init_p.append(element.find('cim:GeneratingUnit.initialP',ns).text)
            nom_p.append(element.find('cim:GeneratingUnit.nominalP',ns).text)
            max_p.append(element.find('cim:GeneratingUnit.maxOperatingP',ns).text)
            min_p.append(element.find('cim:GeneratingUnit.minOperatingP',ns).text)
            
         
        self.df['init_p']=init_p
        self.df['nom_p']=nom_p
        self.df['max_p']=max_p
        self.df['min_p']=min_p