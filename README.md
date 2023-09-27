# CIMProject

This code is written by Alice Jansson and Martin Lundberg at Div. Industrial Electrical Engineering and Automation, LTH, within the KTH course FEN3251 Computer Applications in Power Systems in 2023. 

The goal of the project was to create a program which could:
- Read a CIM-file and identify loads and generator objects where the user could want to define time series
- Use a simple GUI program as the interface
- Let the user define which elements should be given time series, and how the time series are created
- Update the CIM file with the generated time series

The program is run by the script __Main.py__. 

The GUI is implemented in the Python package PySimpleGUI. The code building the GUI is in the script __gui_functions.py__.

The generated load profiles are based on the publication "Belastningsberäkning med typkurvor" 
published by Svenska Elverksföreningen (now Energiföretagen) in 1991.



