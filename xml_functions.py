# -*- coding: utf-8 -*-
"""
Created on Tue Jul  4 09:19:37 2023

@author: ielmartin
"""

import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, QName


# register namespaces from original cim file to preserve them in modified file (function from stackoverflow)
def register_all_namespaces(filename):
    namespaces = dict([node for _, node in ET.iterparse(filename, events=['start-ns'])])
    for ns in namespaces:
        ET.register_namespace(ns, namespaces[ns])
    
    return namespaces


def conform_load_converter(eq, ns, loads):
    # find all loads that are EnergyConsumers and will have a timeseries attached to them. Change the tag to ConformLoad
    # NOTE ConformLoad inherits all of the EnergyConsumer attributes AFAIK
    for element in eq.findall('cim:'+'EnergyConsumer',ns):
        if element.attrib.get(ns['rdf']+'ID') in str(loads.df['ID']):
            element.tag = QName(ns['cim'], 'ConformLoad')
    

    
def load_ts2cim(eq, ns_dict, ns_register, loads, timesteps, p, q):    
    #---iterate here to make one load group + schedule for every load
    grp_id_no = 1
    for load_element in eq.findall('cim:'+'ConformLoad',ns_dict): # find all ConformLoads and verify that they are the right ones (now df straight from cim import)
        load_id = load_element.attrib.get(ns_dict['rdf']+'ID')
        
        if load_id in str(loads.df['ID']):     
            # create conform load group + conform load schedule instance and associate the schedule with load group (here a simplification: a schedule is associated to only ONE load group)   
            grp_id = 'load_grp_no' + str(grp_id_no)
            sch_id = grp_id + '_schedule'
              
            load_group(eq, ns_register, grp_id)
            load_schedule(eq, ns_register, sch_id, grp_id, timesteps)
            
            # add timeseries and associate it with the load schedule
            tp_id_no = 0
            
            for seq_no in range(timesteps):
                tp_id = sch_id + '_' + 'tp_id' + str(tp_id_no)
                load_timepoint(eq, ns_register, sch_id, tp_id, seq_no, p[seq_no], q[seq_no])

                tp_id_no+=1
                
            # add LoadGroup ID to ConformLoad 
            load_grp_name = SubElement(load_element, QName(ns_register['cim'], 'ConformLoad.LoadGroup'),  {QName(ns_register['rdf'], 'resource'): '#_' + grp_id })
             
            grp_id_no+=1
    

def load_group(eq, ns, grp_id):
    # add ConformLoadGroup instance
    load_grp = SubElement(eq, QName(ns['cim'], 'ConformLoadGroup'), {QName(ns['rdf'], 'ID'): '_' + grp_id })
    
    # add load group data
    load_grp_name = SubElement(load_grp, QName(ns['cim'], 'IdentifiedObject.name'))
    load_grp_name.text = 'load_group' + grp_id


def load_schedule(eq, ns, sch_id, grp_id, timesteps):
    # add ConformLoadSchedule instance
    load_sch = SubElement(eq, QName(ns['cim'], 'ConformLoadSchedule'), {QName(ns['rdf'], 'ID'): '_' + sch_id })
    
    # add schedule data
    load_sch_name = SubElement(load_sch, QName(ns['cim'], 'IdentifiedObject.name'))
    load_sch_name.text = 'load_timeseries' + sch_id
    
    load_group_id = SubElement(load_sch, QName(ns['cim'], 'ConformLoadSchedule.ConformLoadGroup'), {QName(ns['rdf'], 'resource'): '#_' + grp_id})

    # Why not Unitmultipliers in MicroGrid example???
    load_sch_unit1 = SubElement(load_sch, QName(ns['cim'], 'BasicIntervalSchedule.value1Unit'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitSymbol.W'})
    load_sch_unit2 = SubElement(load_sch, QName(ns['cim'], 'BasicIntervalSchedule.value2Unit'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitSymbol.VAr'})
    
    load_sch_tstep = SubElement(load_sch, QName(ns['cim'], 'RegularIntervalSchedule.timeStep'))
    load_sch_tstep.text = str(timesteps)



# create RegularTimePoint instances based on load profiles
def load_timepoint(eq, ns, sch_id, tp_id, seq_no, p, q):
    
    # add RegularTimePoint instance
    timepoint = SubElement(eq, QName(ns['cim'], 'RegularTimePoint'), {QName(ns['rdf'], 'ID'): '_' + tp_id })
    
    # add timepoint data
    tp_schedule = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.IntervalSchedule'), {QName(ns['rdf'], 'resource'): '#_' + sch_id})
    tp_seq_no = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.sequenceNumber'))
    tp_seq_no.text = str(seq_no)
    tp_val1 = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.value1'))
    tp_val1.text = str(p)
    tp_val2 = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.value2'))
    tp_val2.text = str(q)
    
    
def write_output(tree, filename):
    # create modified cim file
    root = tree.getroot()
    ET.indent(root, '    ') # indent added entries for better visuals
    tree.write(filename+'.xml', xml_declaration=True, encoding="UTF-8")
    