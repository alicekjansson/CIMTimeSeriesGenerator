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


##----LOADS----
def conform_load_converter(eq, ns, loads):
    # find all loads that are EnergyConsumers and will have a timeseries attached to them. Change the tag to ConformLoad
    # NOTE ConformLoad inherits all of the EnergyConsumer attributes AFAIK
    for element in eq.findall('cim:'+'EnergyConsumer',ns):
        if element.attrib.get(ns['rdf']+'ID') in str(loads.df['ID']):
            element.tag = QName(ns['cim'], 'ConformLoad')
    

    
def load_ts2cim(eq, ns_dict, ns_register, loads, timesteps, tstep_length):    
    #---iterate here to make one load group + schedule for every load
    grp_id_no = 0
    for load_element in eq.findall('cim:'+'ConformLoad',ns_dict): # find all ConformLoads and verify that they are the right ones (now df straight from cim import)
        load_id = load_element.attrib.get(ns_dict['rdf']+'ID')
        load_name = load_element.find('cim:IdentifiedObject.name',ns_dict).text
        
        if load_id in str(loads.df['ID']):     
            # create conform load group + conform load schedule instance and associate the schedule with load group (here a simplification: a schedule is associated to only ONE load group)   
            grp_id = 'load_grp_no' + str(grp_id_no)
            sch_id = grp_id + '_schedule'
              
            load_group(eq, ns_register, load_name, grp_id)
            load_schedule(eq, ns_register, load_name, sch_id, grp_id, tstep_length)
            
            # add timeseries and associate it with the load schedule
            tp_id_no = 0
            
            for seq_no in range(timesteps):
                tp_id = sch_id + '_' + 'tp_id' + str(tp_id_no)
                load_timepoint(eq, ns_register, sch_id, tp_id, seq_no, loads.ts_p[seq_no, grp_id_no], loads.ts_q[seq_no, grp_id_no])

                tp_id_no+=1
                
            # add LoadGroup ID to ConformLoad 
            SubElement(load_element, QName(ns_register['cim'], 'ConformLoad.LoadGroup'),  {QName(ns_register['rdf'], 'resource'): '#_' + grp_id })
            
            
            grp_id_no+=1
    

def load_group(eq, ns, load_name, grp_id):
    # add ConformLoadGroup instance
    load_grp = SubElement(eq, QName(ns['cim'], 'ConformLoadGroup'), {QName(ns['rdf'], 'ID'): '_' + grp_id })
    
    # add load group metadata
    load_grp_name = SubElement(load_grp, QName(ns['cim'], 'IdentifiedObject.name'))
    load_grp_name.text = load_name + '_group'
    load_grp_descript = SubElement(load_grp, QName(ns['cim'], 'IdentifiedObject.description'))
    load_grp_descript.text = grp_id
    


def load_schedule(eq, ns, load_name, sch_id, grp_id, tstep_length):
    # add ConformLoadSchedule instance
    load_sch = SubElement(eq, QName(ns['cim'], 'ConformLoadSchedule'), {QName(ns['rdf'], 'ID'): '_' + sch_id })
    
    # add schedule metadata
    load_sch_name = SubElement(load_sch, QName(ns['cim'], 'IdentifiedObject.name'))
    load_sch_name.text = load_name +'_timeseries'
    
    SubElement(load_sch, QName(ns['cim'], 'ConformLoadSchedule.ConformLoadGroup'), {QName(ns['rdf'], 'resource'): '#_' + grp_id})

    # Why not Unitmultipliers in MicroGrid example???
    SubElement(load_sch, QName(ns['cim'], 'BasicIntervalSchedule.value1Unit'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitSymbol.W'})
    SubElement(load_sch, QName(ns['cim'], 'BasicIntervalSchedule.value2Unit'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitSymbol.VAr'})
    
    load_sch_tstep = SubElement(load_sch, QName(ns['cim'], 'RegularIntervalSchedule.timeStep'))
    load_sch_tstep.text = str(tstep_length)


# create RegularTimePoint instances based on load profiles
def load_timepoint(eq, ns, sch_id, tp_id, seq_no, p, q):
    
    # add RegularTimePoint instance
    timepoint = SubElement(eq, QName(ns['cim'], 'RegularTimePoint'), {QName(ns['rdf'], 'ID'): '_' + tp_id })
    
    # add timepoint data
    SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.IntervalSchedule'), {QName(ns['rdf'], 'resource'): '#_' + sch_id})
    tp_seq_no = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.sequenceNumber'))
    tp_seq_no.text = str(seq_no)
    tp_val1 = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.value1'))
    tp_val1.text = str(p)
    tp_val2 = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.value2'))
    tp_val2.text = str(q)
    

##---GENERATORS (Unit commitment timeseries)---
def gen_opsch2cim(eq, ns_dict, ns_register, gens, timesteps, tstep_length):
    #---iterate here to make one op schedule for every gen
    op_id_no = 0
    for gen_element in eq.findall('cim:'+gens.element_type,ns_dict): 
        gen_id = gen_element.attrib.get(ns_dict['rdf']+'ID')
        gen_name = gen_element.find('cim:IdentifiedObject.name',ns_dict).text
        
        if gen_id in str(gens.df['ID']):     
            # create gen op schedule instance 
            op_id = 'gen_unit_commit_no' + str(op_id_no) + '_schedule'
            sch_id = op_id 
              
            gen_op_schedule(eq, ns_register, gen_name, sch_id, tstep_length)
            # add timeseries and associate it with the gen op schedule
            tp_id_no = 0
            
            for seq_no in range(timesteps):
                tp_id = sch_id + '_' + 'tp_id' + str(tp_id_no)
                gen_opsch_timepoint(eq, ns_register, sch_id, tp_id, seq_no, gens.ts_p[seq_no, op_id_no])

                tp_id_no+=1
                
            # add GenUnitOpSchedule ID to generator 
            SubElement(gen_element, QName(ns_register['cim'], 'GeneratingUnit.GenUnitOpSchedule'),  {QName(ns_register['rdf'], 'resource'): '#_' + op_id })
             
            op_id_no+=1


def gen_op_schedule(eq, ns, gen_name, sch_id, tstep_length):
    # add GenUnitOpSchedule instance
    op_sch = SubElement(eq, QName(ns['cim'], 'GenUnitOpSchedule'), {QName(ns['rdf'], 'ID'): '_' + sch_id })
    
    # add schedule metadata
    op_sch_name = SubElement(op_sch, QName(ns['cim'], 'IdentifiedObject.name'))
    op_sch_name.text = gen_name + '_timeseries'
    op_sch_descript = SubElement(op_sch, QName(ns['cim'], 'IdentifiedObject.description'))
    op_sch_descript.text = sch_id
    
    # Why not Unitmultipliers in MicroGrid example???
    SubElement(op_sch, QName(ns['cim'], 'BasicIntervalSchedule.value1Unit'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitSymbol.none'})
    SubElement(op_sch, QName(ns['cim'], 'BasicIntervalSchedule.value2Unit'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitSymbol.W'})
     
    op_sch_tstep = SubElement(op_sch, QName(ns['cim'], 'RegularIntervalSchedule.timeStep'))
    op_sch_tstep.text = str(tstep_length)

def gen_opsch_timepoint(eq, ns, sch_id, tp_id, seq_no, p):
    
    # add RegularTimePoint instance
    timepoint = SubElement(eq, QName(ns['cim'], 'RegularTimePoint'), {QName(ns['rdf'], 'ID'): '_' + tp_id })
    
    # add timepoint data
    SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.IntervalSchedule'), {QName(ns['rdf'], 'resource'): '#_' + sch_id})
    tp_seq_no = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.sequenceNumber'))
    tp_seq_no.text = str(seq_no)
    tp_val1 = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.value1'))
    tp_val1.text = str(3) # 3 = unit must run at fixed power value
    tp_val2 = SubElement(timepoint, QName(ns['cim'], 'RegularTimePoint.value2'))
    tp_val2.text = str(p)

##---GENERATORS (Measurement timeseries)---

def gen_mea2cim(eq, ns_dict, ns_register, gens, timesteps, tstep_length):
    #---iterate here to make one analog measurement series for every gen
    meas_id_no = 0
    for gen_element in eq.findall('cim:'+gens.element_type,ns_dict): 
        gen_id = gen_element.attrib.get(ns_dict['rdf']+'ID')
        gen_name = gen_element.find('cim:IdentifiedObject.name',ns_dict).text
        
        if gen_id in str(gens.df['ID']):     
            # create Analog measurement instance 
            meas_id = 'gen_meas_series_no' + str(meas_id_no)
            sch_id = meas_id
              
            gen_meas(eq, ns_register, gen_name, gen_id, sch_id, tstep_length)
            # add timeseries (analog values) and associate it with the Analog measurement
            tp_id_no = 0
            
            for seq_no in range(timesteps):
                tp_id = sch_id + '_' + 'tp_id' + str(tp_id_no)
                meas_value(eq, ns_register, sch_id, tp_id, tp_id_no, gens.ts_p[seq_no, meas_id_no])

                tp_id_no+=1
                
            # add GenUnitOpSchedule ID to generator 
           # SubElement(gen_element, QName(ns_register['cim'], 'GeneratingUnit.GenUnitOpSchedule'),  {QName(ns_register['rdf'], 'resource'): '#_' + op_id })
             
            meas_id_no+=1

def gen_meas(eq, ns, gen_name, gen_id, sch_id, tstep_length):
    # add Analog (measurement) instance
    meas = SubElement(eq, QName(ns['cim'], 'Analog'), {QName(ns['rdf'], 'ID'): '_' + sch_id })
    
    # add gen id to Analog measurement NOTE in order to define exact measurement location a Measurement.Terminal association must also be made
    SubElement(meas, QName(ns['cim'], 'Measurement.PowerSystemResource'), {QName(ns['rdf'], 'ID'): '#_' + gen_id })
    
    # add measurement metadata
    meas_name = SubElement(meas, QName(ns['cim'], 'IdentifiedObject.name'))
    meas_name.text = gen_name + '_timeseries'
    meas_descript = SubElement(meas, QName(ns['cim'], 'IdentifiedObject.description'))
    meas_descript.text = 'sTimestep=' + str(tstep_length) 
    
    # Why not Unitmultipliers in MicroGrid example???
    SubElement(meas, QName(ns['cim'], 'Measurement.unitMultiplier'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitMultiplier.M'})
    SubElement(meas, QName(ns['cim'], 'Measurement.unitSymbol'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#UnitSymbol.W'})
    
    SubElement(meas, QName(ns['cim'], 'Measurement.phases'), {QName(ns['rdf'], 'resource'): 'http://iec.ch/TC57/2013/CIM-schema-cim16#PhaseCode.ABC'})
    meas_type = SubElement(meas, QName(ns['cim'], 'Measurement.measurementType'))
    meas_type.text = 'ThreePhaseActivePower'
    
def meas_value(eq, ns, sch_id, tp_id, tp_id_no, p):
    # add measurement point instance
    meas_point = SubElement(eq, QName(ns['cim'], 'AnalogValue'), {QName(ns['rdf'], 'ID'): '_' + tp_id })
    
    # add measurement value metadata
    meas_val_name = SubElement(meas_point, QName(ns['cim'], 'IdentifiedObject.name'))
    meas_val_name.text = 'VALUE_NO ' + str(tp_id_no) 
    meas_descript = SubElement(meas_point, QName(ns['cim'], 'IdentifiedObject.description'))
    meas_descript.text = 'sequenceNumber ' + str(tp_id_no)
    
    # add measurement point data
    SubElement(meas_point, QName(ns['cim'], 'AnalogValue.Analog'), {QName(ns['rdf'], 'resource'): '#_' + sch_id})
    meas_val = SubElement(meas_point, QName(ns['cim'], 'AnalogValue.value'))
    meas_val.text = str(p)
    
      

##---OUTPUTS---   
def write_output(tree, file):
    # create modified cim file
    root = tree.getroot()
    ET.indent(root, '    ') # indent added entries for better visuals
    tree.write(file, xml_declaration=True, encoding="UTF-8")
    