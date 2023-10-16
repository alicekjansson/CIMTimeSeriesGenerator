# -*- coding: utf-8 -*-
"""
Created on Mon Aug 21 15:51:50 2023

MIT License

Copyright (c) 2023 Alice Jansson, Martin Lundberg
"""

import pandas as pd
import numpy as np
import PySimpleGUI as sg
import xml.etree.ElementTree as ET
from import_cim import data_extract
from xml_functions import register_all_namespaces, write_output
from modify_xml import cim_timeseries
from profiles import aggregate_gen, aggregate_load, calculate_N, fig_maker, draw_figure, delete_fig_agg
from matplotlib.figure import Figure



ns_dict = {'cim':'http://iec.ch/TC57/2013/CIM-schema-cim16#',
      'entsoe':'http://entsoe.eu/CIM/SchemaExtension/3/1#',
      'md':"http://iec.ch/TC57/61970-552/ModelDescription/1#",
      'rdf':'{http://www.w3.org/1999/02/22-rdf-syntax-ns#}'}

#-----GUI------


def timeseries_settings_window(loads, gens):
    
    load_names = loads.df['name'].tolist()
    
    
    col1 = [
        [sg.Text('Choose bidding area:')],  
        [sg.Combo(['SE1','SE2','SE3','SE4'],key='ZONE',enable_events=True,default_value='SE4',size=(10, 1))],  
    ]
    col2 = [
        [sg.Text('Choose day:')],
        [sg.Combo(['Weekday','Weekend'],key='DAY',enable_events=True,default_value='Weekday',size=(10, 1))],  
    ]
    col3 = [
        [sg.Text('Choose season:')],
        [sg.Combo(['Winter','Autumn/Spring','Summer'],key='SEASON',enable_events=True,default_value='Winter',size=(10, 1))], 
    ]

    load_left = [
        [sg.Text("Loads")],
        [sg.Listbox(load_names,key='LOADS',select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, size=[100,50],enable_events=True)],
    ]
    r1=sg.Radio('Average (default)','load',enable_events=True, default=True, key='AVERAGE')
    r2=sg.Radio('Urban area','load',enable_events=True,key='URBAN')
    r3=sg.Radio('Rural area','load',enable_events=True,key='RURAL')
    r4=sg.Radio('Industrial area','load',enable_events=True,key='INDUSTRY')
    load_right = [
        [sg.Text("Select load case")],
        [r1],
        [r2],
        [r3],
        [r4]
    ]

    layout = [[sg.Text('Time Series Generator',font=('Helvetica',30))],
              [sg.HorizontalSeparator()],
              [sg.Text('General settings')],
              [sg.Column(col1,size=[150,50]),
               sg.Column(col2,size=[150,50]),
               sg.Column(col3,size=[150,50])],
              [sg.HorizontalSeparator()],
              [sg.Text('Load settings')],
              [sg.Column(load_left,size=[200,150]),
               sg.VerticalSeparator(),
               sg.Column(load_right,size=[200,150])],
              [sg.HorizontalSeparator()],
              [sg.Exit()]
              ]
    
    types=['Småhus Direktel','Småhus Hushållsel','Lägenhet','Industri']
    bids=['SE1','SE2','SE3','SE4']
    seasons=['Winter','Autumn/Spring','Summer']
    days=['Weekday','Weekend']

    
    
    window3 = sg.Window('Load Timeseries Generator', layout, finalize=True)
    
    return window3, types, bids, seasons, days


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
                if gen.gen_type == 'Hydro':
                    hydro_names.append(name)
                if gen.gen_type == 'Wind':
                    wp_names.append(name)
                if gen.gen_type == 'CHP':
                    chp_names.append(name)
                if gen.gen_type == 'Nuclear':
                    nucl_names.append(name)
              
                
            
    layout1 = [[sg.Text("Loads")],
              [sg.Listbox(load_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size =(20, 5), key ='load')],
              [sg.Text('Generators')],
              [sg.Text(gen_texts[0])],
              [sg.Listbox(pv_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size =(20, 5), key ='0pv')],
              [sg.Text(gen_texts[1])],
              [sg.Listbox(hydro_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size =(20, 5), key ='1hy')],
              [sg.Text(gen_texts[2])],
              [sg.Listbox(wp_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size =(20, 5), key ='2wp')],
              [sg.Text(gen_texts[3])],
              [sg.Listbox(chp_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size =(20, 5), key ='3chp')],
              [sg.Text(gen_texts[4])],
              [sg.Listbox(nucl_names, select_mode=sg.LISTBOX_SELECT_MODE_SINGLE, enable_events=True, size =(20, 5), key ='4nucl')]
              ]
    
    print_window = sg.MLine(size=(50,10), key='print')
    print = print_window.print
    layout2 = [  [sg.Text('Details')],
            [print_window],
            [sg.Text('Time Series')],
            [sg.Canvas(key='PLOT',background_color='white', size=(360,200))]]
    
    layout = [[sg.Column(layout1),sg.Column(layout2)],
              [sg.Exit()]
             ]
    
    window2 = sg.Window("Resource data viewer", layout, finalize=True)
    
    
    return window2, print



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
              [sg.Text('When generating daily profiles, model all undefined power plants as')],
              [sg.Radio('PV plants','def_plant',key='rd_pv'),
               sg.Radio('Hydro plants','def_plant',key='rd_hy'),
               sg.Radio('Wind plants','def_plant',key='rd_wp'),],
              [sg.Radio('Thermal/CHP plants (default)','def_plant',key='rd_chp',default='True'),
               sg.Radio('Nuclear plants','def_plant',key='rd_nucl'),],
              [sg.Button('Timeseries Settings', key = 'ts_generator')],
              [sg.Checkbox('Update EQ file with Daily Profiles', key = 'save_cim', default=True),sg.Checkbox('Save Daily Profiles in CSV file', key = 'save_csv', default=False)],
              [sg.Submit('Generate Timeseries', key='run'),sg.Button('View Resource Data', key = 'open'),
               sg.Exit()],
              [sg.HorizontalSeparator()],
              [sg.Text('Save new CIM (EQ) file as', size=(19, 1)), sg.Input('output_EQ',key='Name',size=(40, 1))],
              [sg.Text('Output folder', size=(19, 1)), sg.Input('./',key='loc',size=(40, 1)), sg.FolderBrowse()],        
              [sg.HorizontalSeparator()],
              [sg.Text('CSV Name', size=(12, 1)), sg.Input(key='Name1')],
              [sg.Text('CSV Location', size=(12, 1)), sg.Input('./Generated_csv',key='loc1'), sg.FolderBrowse()]            
              ]
    
    return sg.Window('CIM Timeseries Generator', layout, finalize=True)

# function to generate gui windows and track events
def start_gui():
    
    # initiate variables for tracking and storing data for correct GUI operation
    extract_check = 0 # to check if cim data has been extracted from files
    timeseries_check = 0 # to check that timeseries have been generated
    load_char = [] # for storing load characteristcs data
    selection = None
    fig_agg = None   
    gen_texts = ['PV plants', 'Hydro plants', 'Wind plants', 'Thermal/CHP plants', 'Nuclear plants', 'Undefined power plants']
    
    # start only the first (main) window when running the code
    window1, window2, window3 = start_window(gen_texts), None, None
    while True:      
        window, event, values = sg.read_all_windows()
        
        if event == "Exit" or event == sg.WIN_CLOSED:
           window.close()
           if window == window1:
               break                   # if closing win 1, exit program
           elif window == window2:    # if closing win 2, mark as closed   
               window2 = None
           elif window == window3:     # if closing win 3, mark as closed
               window3 = None
        
        ### --- MAIN WINDOW ---
        # extracting data from CIM file
        elif event == 'extract':
            # Parse input EQ and SSH files using ElementTree
            eq_file = values[0]
            ssh_file = values[1]
            eq_xml = ET.parse(eq_file)
            eq = eq_xml.getroot()
            ssh_xml = ET.parse(ssh_file)
            ssh=ssh_xml.getroot()        
            
            # Here, load and generator (python) classes are created and populated with data extracted from the parsed CIM files      
            loads, pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens = data_extract(eq, ssh, ns_dict)
            gens = [pv_gens, hydro_gens, wind_gens, thermal_gens, nuclear_gens, undef_gens]
            
            #default timeseries settings
            zone = 4
            season = 0
            day = 0
            
            #set any undefined generators as chp per default, change with user input
            if gens[-1]:
                undef_gens.gen_type = "CHP"
                if values['rd_pv']:
                    undef_gens.gen_type = "PV"
                if values['rd_hy']:
                    undef_gens.gen_type = "Hydro"
                if values['rd_wp']:
                    undef_gens.gen_type = "Wind"
                if values['rd_chp']:
                    undef_gens.gen_type = "CHP"
                if values['rd_nucl']:
                    undef_gens.gen_type = "Nuclear"
            
            # Update GUI with number of resources found of each type
            if loads:
                window['loads'].update(str(len(loads.df)))
                if not load_char:
                    load_char = ['AVERAGE']*len(loads.df) #list for saving load characteristics settings with default value
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
                       
            # mark data extract as completed             
            extract_check = 1
            
         # generate timeseries       
        elif event == 'run':
            all_timeseries=pd.DataFrame()
            if extract_check == 1:
                timeseries_check=1                                      
                #TIMESERIES DATA
                timesteps = 24
                tstep_length = 3600 # unit seconds
                
                
                #Load data
                if loads:
                    load_list = []
                    load_q_list = []
                    for n, load in enumerate(loads.df['name']):
                        if load_char[n] == 'AVERAGE':
                            dwellings=[0.94,0.03,0.03]
                        if load_char[n] == 'URBAN':
                            dwellings=[0.69,0.30,0.01]
                        if load_char[n] == 'RURAL':
                            dwellings=[0.96,0.01,0.03]
                        if load_char[n] == 'INDUSTRY':
                            dwellings=[0.88,0.02,0.10]
 
     
                        P_scale = float(loads.df.at[n, 'p'])
                        P_tot=[]
                        N_all=calculate_N(P_scale,dwellings)
                        for i,N in enumerate(N_all):
                            cat=i
                            P_tot.append(aggregate_load(cat,zone,season,day,N))
                        P_tot=(P_tot[0]+P_tot[1]+P_tot[2])/1000
                        load_list.append(P_tot)
                        all_timeseries[load]=P_tot
                        load_q_list.append(P_tot*np.tan(np.arccos(loads.df.at[n, 'cosphi'])))
                        
                    load_array = np.array(load_list)
                    load_array.shape = (load_array.size//len(loads.df['name']),len(loads.df['name']))
                    loads.ts_p = load_array
                    
                    load_q_array = np.array(load_q_list)
                    load_q_array.shape = (load_q_array.size//len(loads.df['name']),len(loads.df['name']))
                    loads.ts_q = load_q_array
                    
                 # generation data
                gen_ts=pd.read_csv(r'./SVK-Data/all_years.csv',sep=',').iloc[:,1:]
                for gen_type in gens:
                    if gen_type:
                        gen_list = []
                        for n, gen in enumerate(gen_type.df['name']):
                            P_scale = float(gen_type.df.at[n,'max_p'])
                            # Nuclear power data only exist in SE3
                            if gen_type.gen_type == 'Nuclear':
                                nuclear_zone=3
                                gen_profile=aggregate_gen(gen_ts,'Hour',gen_type.gen_type+' '+'SE'+str(nuclear_zone),P_scale)
                            else:
                                gen_profile=aggregate_gen(gen_ts,'Hour',gen_type.gen_type+' '+'SE'+str(zone),P_scale)
                            gen_list.append(gen_profile)
                            all_timeseries[gen]=gen_profile
                        gen_array = np.array(gen_list)
                        gen_array.shape = (gen_array.size//len(gen_type.df['name']),len(gen_type.df['name']))
                        gen_type.ts_p = gen_array
                
                
                check_cim = 0
                if values['save_cim']:    
                                 
                    # register namspaces for printing in output (see function)
                    ns_register = register_all_namespaces(eq_file)
                
           
                    # generate cim data
                    eq_xml = cim_timeseries(eq, eq_xml, ns_dict, ns_register, loads, gens, timesteps, tstep_length)
                    
                    # genterate new xml file
                    if not ( values['Name'] and values['loc']):
                        check_cim = 0
                    else:
                        xml_name=values['Name']
                        loc = '.'
                        if values['loc']:
                            loc=values['loc']
                        xml_file=str(loc)+'/'+str(xml_name)+'.xml'
                        write_output(eq_xml, xml_file)
                        check_cim = 1
                        
                check_csv = 0
                if values['save_csv']:
                    if not ( values['Name1'] and values['loc1']):
                        check_csv = 0
                    else:
                        name=values['Name1']
                        loc=values['loc1']
                        csv_loc=str(loc)+'/'+str(name)+'.csv'
                        if loads:
                            df1 = pd.DataFrame(load_array, columns = loads.df['name'])
                        else:
                            df1 = pd.DataFrame()
                        for n, gen_type in enumerate(gens):
                            if gen_type:
                                df2 = pd.DataFrame(gen_type.ts_p, columns = gen_type.df['name'])
                                df1 = pd.concat([df1,df2],axis = 1)
                            
                        df1.to_csv(csv_loc)
                        check_csv = 1
                
                if values['save_cim'] and values['save_csv']:
                    if check_cim == 1 and check_csv == 1:
                        sg.popup('CIM and CSV files succefully created')
                    else:
                        sg.popup('Add missing file information')
                if values['save_cim'] and not values['save_csv']:
                   
                    if check_cim == 1:
                        sg.popup('CIM file succefully created')
                    else:
                        sg.popup('Add missing file information')
                if values['save_csv'] and not values['save_cim']:
                    
                    if check_csv == 1:
                        sg.popup('CSV file succefully created')
                    else:
                        sg.popup('Add missing file information')
                
                        
                    
            # --- TIMESERIES SETTINGS WINDOW ----
        # new window to generate timeseries  
        elif event == 'ts_generator' and not window3:
            if extract_check == 1:
                window3, types, bids, seasons, days =  timeseries_settings_window(loads, gens)
                timeseries_check = 1
        
        elif event == 'ZONE':
            if values['ZONE']:
                choice=values['ZONE']                # Get user choice
                for i,d in enumerate(bids):
                    if choice == d:
                        zone=i+1
        elif event == 'SEASON':
            if values['SEASON']:
                choice=values['SEASON']                # Get user choice
                for i,d in enumerate(seasons):
                    if choice == d:
                        season=i
        elif event == 'DAY':
            if values['DAY']:
                choice=values['DAY']                # Get user choice
                for i,d in enumerate(days):
                    if choice == d:
                        day=i
                        
        
        elif event == 'LOADS':
                    
            selection = values[event]
            if selection:
                item = selection[0]
                for index, load in loads.df.iterrows():
                    if item == load['name']:
                        if load_char[index] == 'AVERAGE':
                            window3['AVERAGE'].update(value=True)
                        elif load_char[index]  == 'URBAN':
                            window3['URBAN'].update(value=True)
                        elif load_char[index]  == 'RURAL':
                            window3['RURAL'].update(value=True)
                        elif load_char[index]  == 'INDUSTRY':
                            window3['INDUSTRY'].update(value=True)   
        
        elif  event == 'AVERAGE' or event == 'URBAN' or event == 'RURAL' or event == 'INDUSTRY':
            if selection:
                item = selection[0]
                for index, load in loads.df.iterrows():
                    if item == load['name']:
                        if values['AVERAGE']:
                            load_char[index]  = 'AVERAGE'
                        if values['URBAN']:
                            load_char[index]    = 'URBAN'
                        if values['RURAL']:
                            load_char[index]    = 'RURAL'
                        if values['INDUSTRY']:
                            load_char[index]   = 'INDUSTRY'
                                             
            
            # ---RESOURCE DATA WINDOW
        # new window with more detailed resource data    
        elif event == 'open' and not window2:
            if extract_check == 1:
                    
                window2, print = resource_data_window(loads, gens, gen_texts)
        
        elif event == 'load':
            selection = values[event]
            if selection:
                window2['print'].update('')
                item = selection[0]
                print('Name = ' + item)
                for index, load in loads.df.iterrows():
                    if item == load['name']:
                        load_p = round(float(load['p']),2)
                        print('Active Power = '+ str(load_p) + ' MW')
                        pf = round(load['cosphi'],2)
                        print('Power Factor = '+ str(pf))
                        if timeseries_check==1:
                            if fig_agg is not None:
                                delete_fig_agg(fig_agg)
                            fig = fig_maker(all_timeseries[item],item)
                            fig_agg = draw_figure(window['PLOT'].TKCanvas, fig)
                        
        elif event == '0pv' or  event == '1hy' or event == '2wp' or event == '3chp' or event == '4nucl':
            selection = values[event]
            if selection:
                window2['print'].update('')
                item = selection[0]
                print('Name = ' + item)
                
                if gens[int(event[0])]:
                    for index, gen in gens[int(event[0])].df.iterrows():
                        if item == gen['name']:
                            gen_p = round(float(gen['init_p']),2)
                            max_p = round(float(gen['max_p']),2)
                            print('Active Power = '+ str(gen_p) + ' MW')
                            print('Maximum Operating Power = '+ str(max_p)+ ' MW')
                            if timeseries_check==1:
                                if fig_agg is not None:
                                    delete_fig_agg(fig_agg)
                                fig = fig_maker(all_timeseries[item],item)
                                fig_agg = draw_figure(window['PLOT'].TKCanvas, fig)

                # #undefined generators
                if gens[-1]:
                    for index, gen in gens[-1].df.iterrows():
                        if item == gen['name']:
                            gen_p = round(float(gen['init_p']),2)
                            max_p = round(float(gen['max_p']),2)
                            print('Active Power = '+ str(gen_p) + ' MW')
                            print('Maximum Operating Power = '+ str(max_p)+ ' MW')
                            if timeseries_check==1:
                                if fig_agg is not None:
                                    delete_fig_agg(fig_agg)
                                fig = fig_maker(all_timeseries[item],item)
                                fig_agg = draw_figure(window['PLOT'].TKCanvas, fig)
                           

    if fig_agg is not None:
        delete_fig_agg(fig_agg)        
    window.close()