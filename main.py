# -*- coding: utf-8 -*-
"""
Created on Thu Jun 29 14:35:49 2023

@author: ielmartin
"""

import pandas as pd
import numpy as np
import PySimpleGUI as sg
import xml.etree.ElementTree as ET
from import_cim import data_extract
from xml_functions import register_all_namespaces
from modify_xml import cim_timeseries

ns_dict = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'md':"http://iec.ch/TC57/61970-552/ModelDescription/1#",
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}



#-----GUI------

def resource_data_window(loads, gens, gen_texts):
    
    load_names = loads.df['name'].tolist()
    pv_names = []
    hydro_names = []
    wp_names = []
    chp_names = []
    nucl_names = []

    for gen in gens:
        if gen:
            for name in gen.df['name']:
                if gen.gen_type == 'PV':
                    pv_names.append(name)
                if gen.gen_type == 'HYDRO':
                    hydro_names.append(name)
                if gen.gen_type == 'WIND POWER':
                    wp_names.append(name)
                if gen.gen_type == 'CHP':
                    chp_names.append(name)
                if gen.gen_type == 'NUCLEAR':
                    nucl_names.append(name)
              
                
            
    layout1 = [[sg.Text("Loads")],
              [sg.Listbox(load_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size =(20, 5), key ='load')],
              [sg.Text('Generators')],
              [sg.Text(gen_texts[0])],
              [sg.Listbox(pv_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size =(20, 5), key ='pv')],
              [sg.Text(gen_texts[1])],
              [sg.Listbox(hydro_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size =(20, 5), key ='hy')],
              [sg.Text(gen_texts[2])],
              [sg.Listbox(wp_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size =(20, 5), key ='wp')],
              [sg.Text(gen_texts[3])],
              [sg.Listbox(chp_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size =(20, 5), key ='chp')],
              [sg.Text(gen_texts[4])],
              [sg.Listbox(nucl_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size =(20, 5), key ='nucl')]
              ]
    
    print_window = sg.MLine(size=(50,10), key='print')
    print = print_window.print
    layout2 = [  [sg.Text('Details')],
            [print_window]]
    
    layout = [[sg.Column(layout1),sg.Column(layout2)],
              [sg.Exit()]
             ]
    
    window2 = sg.Window("Resource data viewer", layout, finalize=True)
    
    if window2['load']:
        print(window2['load'])
              
    return window2



def start_window(gen_texts):
    sg.theme('LightGreen5')
    
    load_no = [sg.Text("-", key='loads'),sg.Text("Loads")]
    gen_no = []
    
    for i in range(len(gen_texts)):
            gen_no.append([sg.Text("-", key = gen_texts[i]),sg.Text(gen_texts[i], key= gen_texts[i]+'1' ),])
    

    layout  =[
        [sg.Text('Enter the required CGMES CIM/XML files')],
              [sg.Text('EQ File', size=(8, 1)), 
               sg.Input('./20171002T0930Z_NL_EQ_3.xml'), 
               sg.FileBrowse(),],
              [sg.Text('SSH File', size=(8, 1)), 
               sg.Input('./20171002T0930Z_1D_NL_SSH_3.xml'), 
               sg.FileBrowse(),],
              [sg.Submit('Extract Load and Generator Data', key='extract')],
            [sg.Text('The following resources have been found')],
              load_no,
              gen_no,
              [sg.Text('When generating timeseries, model all undefined power plants as')],
              [sg.Radio('PV plants','def_plant',key='rd_pv'),
               sg.Radio('Hydro plants','def_plant',key='rd_hy'),
               sg.Radio('Wind plants','def_plant',key='rd_wp'),],
              [sg.Radio('Thermal/CHP plants (default)','def_plant',key='rd_chp'),
               sg.Radio('Nuclear plants','def_plant',key='rd_nucl'),],
              [sg.Button('View resource data', key = 'open')],
              [sg.Submit('Generate timeseries', key='run'),
               sg.Exit()]
              ]
    
    return sg.Window('CIM Timeseries Generator', layout, finalize=True)

# function to generate gui windows and track events
def start_gui():
    extract_check = 0 # to check if cim data has been extracted from files
    
    gen_texts = ['PV plants', 'Hydro plants', 'Wind plants', 'Thermal/CHP plants', 'Nuclear plants', 'Undefined power plants']
    
    # start only the first gui when running the code
    window1, window2 = start_window(gen_texts), None
    while True:      
        window, event, values = sg.read_all_windows()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
           window.close()
           if window == window2:       # if closing win 2, mark as closed
               window2 = None
           elif window == window1:     # if closing win 1, exit program
               break
        
        # extracting data from CIM file
        elif event == 'extract':
            # Parse input files
            eq_file = values[0]
            ssh_file = values[1]
            eq_xml = ET.parse(eq_file)
            eq = eq_xml.getroot()
            ssh_xml = ET.parse(ssh_file)
            ssh=ssh_xml.getroot()        
            
            # Here, load and generator classes are created and populated with data      
            loads, pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens = data_extract(eq, ssh, ns_dict)
            gens = [pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens]
            
            # Update GUI with number of resources found of each type
            if loads:
                window['loads'].update(str(len(loads.df)))
            else:
                window['loads'].update('0')
           
            for i in range(len(gens)):
                if gens[i]:
                    window[gen_texts[i]].update(str(len(gens[i].df)))
                    if len(gens[i].df)==1:
                        name = gen_texts[i]
                        window[gen_texts[i]+'1'].update(name[:-1])
                else:
                    window[gen_texts[i]].update('0')
                         
            extract_check = 1
                    
        # second window with more detailed resource data    
        elif event == 'open' and not window2:
            if extract_check == 1:
                # check choice of classification of undefined generators (if any)
                if gens[-1]:
                    undef_gens.gen_type = "CHP"
                    if values['rd_pv']:
                        undef_gens.gen_type = "PV"
                    if values['rd_hy']:
                        undef_gens.gen_type = "HYDRO"
                    if values['rd_wp']:
                        undef_gens.gen_type = "WIND POWER"
                    if values['rd_chp']:
                        undef_gens.gen_type = "CHP"
                    if values['rd_nucl']:
                        undef_gens.gen_type = "NUCLEAR"
                window2 = resource_data_window(loads, gens, gen_texts)
               

         # generate timeseries       
        elif event == 'run':
            
            if extract_check == 1:
                
                
                #TIMESERIES DATA
                # timesteps = 24
                # tstep_length = 3600 # unit seconds
                # for load in loads:    
                #     load.ts_p = np.random.rand(timesteps)
                #     load.ts_qw= np.random.rand(timesteps)
                
                # for gen in gens:
                #     if gen:
                #         for unit in gen:
                            
                
                # register namspaces for printing in output (see function)
                ns_register = register_all_namespaces(eq_file)
                
           
                # generate cim file
                cim_timeseries(eq, eq_xml, ns_dict, ns_register, loads, gens)

                break
       
            
    window.close()
       
gui = 1
if gui == 1:
    start_gui()
# --- NOT GUI
else:
    eq_file = '20171002T0930Z_NL_EQ_3.xml'
    ssh_file = '20171002T0930Z_1D_NL_SSH_3.xml'
    eq_xml = ET.parse(eq_file)
    ssh_xml = ET.parse(ssh_file)
    eq = eq_xml.getroot()
    ssh = ssh_xml.getroot()        
    # Here, functions to generate timeseries    
    loads, pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens = data_extract(eq, ssh, ns_dict)
    gens = [pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens]
    
    # register namspaces for printing in output (see function)
    ns_register = register_all_namespaces(eq_file)
    
    # generate cim file
    indata = 'timeseries for loads and generators'
    cim_timeseries(eq, eq_xml, ns_dict, ns_register, loads, gens, indata)
    print('success ')
