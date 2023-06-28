# -*- coding: utf-8 -*-
"""
Created on Mon Jun 19 08:34:52 2023

@author: ielmartin
"""

import pandas as pd
import PySimpleGUI as sg
import xml.etree.ElementTree as ET

ns = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}',
      'md':"http://iec.ch/TC57/61970-552/ModelDescription/1#"}


# superclass of all grid objects
class GridObjects:
    
    def __init__(self, eq, ssh, ns,element_type):

        self.df=pd.DataFrame()
        
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
    
    def __init__(self,eq,ssh,ns, element_type = "SynchronousMachine"):
        super().__init__(eq, ssh, ns, element_type)
        
        gen_power = []
        gen_max_power = []
        for gen_id in self.df['ID']:   
            for element in self.ssh_list:
                if '#' + gen_id  == element.attrib.get(ns['rdf']+'about'):
                    gen_power.append(element.find('cim:RotatingMachine.p',ns).text)
            
            for element in self.eq_list:
                if gen_id  == element.attrib.get(ns['rdf']+'ID'):
                    gen_max_power.append(element.find('cim:RotatingMachine.ratedS',ns).text)
            
        self.df['p']=gen_power
        self.df['max_p']=gen_max_power


#-----GUI------
gui = 1

if gui == 1:
    layout = [[sg.Text('Enter the required CGMES CIM/XML files')],
              [sg.Text('EQ File', size=(8, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('SSH File', size=(8, 1)), sg.Input(), sg.FileBrowse()],
              [sg.Text('Enter other input data')],
              [sg.Text('Data', size=(8, 1)), sg.Input()],
              [sg.Submit('Generate Timeseries')]]
    
    # Create the window
    window = sg.Window('CIM Timeseries Generator', layout)
    
    # Display and interact with the Window using an Event Loop
    while True:
        event, values = window.read()
        eq_xml = values[0]
        ssh_xml = values[1]
        eq = ET.parse(eq_xml).getroot()
        ssh = ET.parse(ssh_xml).getroot()        
                
                
        loads = Loads(eq,ssh,ns)
        gens = Generators(eq,ssh,ns)
        print('success')
        
        window.close()
       

else:
    eq_xml = ET.parse('20171002T0930Z_NL_EQ_3.xml')
    ssh_xml = ET.parse('20171002T0930Z_1D_NL_SSH_3.xml')
    eq = eq_xml.getroot()
    ssh = ssh_xml.getroot()        
            
            
    loads = Loads(eq,ssh,ns)
    gens = Generators(eq,ssh,ns) 

        
        