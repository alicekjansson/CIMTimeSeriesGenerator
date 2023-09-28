# CIM Project: A Timeseries Generator for Power System Models in CGMES format 

This code was written by Alice Jansson and Martin Lundberg at Div. of Industrial Electrical Engineering and Automation, LTH, within the KTH course FEN3251 Computer Applications in Power Systems in 2023. 

The goal of the project was to create a program which could:
- Read a CIM-file and identify loads and generator objects where the user could want to define time series
- Use a simple GUI program as the interface
- Let the user define which elements should be given time series, and how the time series are created
- Update the CIM file with the generated time series


The code is free to use, modify and distribute without restrictions according to the MIT license, see __license.txt__


## GUI Features

Import EQ and SSH CGMES CIM files and display extracted resource data

Model undefined generating units as thermal/hydro/pv/wind/nuclear units

Choose individual daily load profiles based on season/time of week/Swedish region/load case

 ## Running the Program 

Requirements: Python with PySimpleGUI

The GUI is initialized by running the script __main.py__. 

## Details

The project is based on the IEC 61970-301:2020 standard. The code was tested using EQ and SSH files from the ENTSO-E Test Configuration networks. 

### Importing EQ and SSH files, and extracting relevant data (import_cim.py, GridObjects.py)

The power system resource classes considered by the timeseries generator are
- EnergyConsumer
- GeneratingUnit
- PhotoVoltaicUnit
- HydroGeneratingUnit
- WindGeneratingUnit
- ThermalGeneratingUnit
- NuclearGeneratingUnit
  
(Note: additional resource classes exist, perhaps most notably SolarGeneratingUnit which represents a solar thermal plant)

Resource data is collected from the EQ and SSH files and stored in by type in instances of the GridObjects classes _Loads_ and _Generators_. _Loads_ is used to collect all instances of the EnergyConsumer class found in the CIM files and _Generators_ is used to group all other classes listed above by generator type. 

The following resource attributes are extracted and saved
- ID, name (all resources)
- p, q (Loads only)
- initialP, nominalP, maxOperatingP, minOpteratingP (Generators only)


### Generating CIM classes for Timeseries Data (modify_xml.py, xml_functions.py)

Three different approaches are used to represent timeseries for loads, conventional/dispatchable generators (thermal, hydro, nuclear), and nondispatchable generators (wind, pv). The reason for this is that the CIM standard has different classes to manage different types of time varying resources. 

Note that all IDs of new class instances are completely made-up, but in an incremental fashion, e.g., "_load_grp_no2_schedule_tp_id3" is the ID for the fourth timepoint (starting from 0) of the only load schedule class instance for LoadGroup instance number 2.  

#### Loads

All considered loads changes class from EnergyConsumer to ConformLoad with all attributes inherited. ConformLoad "represent loads that follow a daily load change pattern where the pattern can be 
used to scale the load with a system load" (IEC 61970-301:2020). 

For each ConformLoad instance, one ConformLoadGroup and one ConformLoadSchedule instance is then generated and associated to the ConformLoad in question.  

Timepoints are stored as instances of the RegularTimePoint class

Note that the use of the NonConformLoad class instead of ConformLoad would not make any difference in this particular case since one timeseries dataset is assigned to each load rather than having multiple loads being grouped and scaled to one and the same timeseries. 




#### Scheduled Generation
#### Nonscheduled Generation

### Generation of profiles

The functions for the generation of profiles are found in the script __profiles.py__. 

#### Loads

The generated load profiles are based on the publication "Belastningsberäkning med typkurvor" published by Svenska Elverksföreningen (now Energiföretagen) in 1991. Four standard load curves are used: 
- House with heating from electricity
- House with heating from other source
- Apartment building with heating from other source
- Small Industry with heating from electricity

For houses, a combination of 30 % houses with electric heating and 70 % without electric heating is used based on Swedish statistics. 

The code for calculating load profiles is found in the function _generate_timeseries_. A load profile is based on a standard load curve (defined above), transformed according to yearly energy use and temperature as defined in the report from 1991. Aggregation of load profiles to correct power level is done with the function _aggregate_load_. The number of objects is calculated based on defined power level of load.

#### Generation

The generation profiles are based on aggregated data per bidding area from SVK. Generation profiles are scaled with defined power level in the function _aggregate_gen_. Some code is available for adding a random factor to the generation, but not implemented in the original code.

### GUI (gui_functions.py)

The code building the GUI is in the script __gui_functions.py__.



