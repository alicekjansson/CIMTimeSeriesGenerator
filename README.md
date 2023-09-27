# CIMProject

This code is written by Alice Jansson and Martin Lundberg at Div. Industrial Electrical Engineering and Automation, LTH, within the course FEN3251 Computer Applications in Power Systems in 2023. 

### Efter möte med Lars:
- Läs in CIM-fil och hitta de laster och generatorer där användaren skulle kunna vilja definiera tidsserier
- Använd enkel GUI som verktyg för programmet
- Användaren får välja vilka element som tidsserier ska skapas (eventuellt också mer input HUR de skapas)
- Kolla upp vilket dataformat tidsserierna ska skapas i! Utgå från befintlig CIM-standard pga koppling till PowerFactory
- Kolla upp om vår licens till PowerFactory så småningom kan utvidgas till att arbeta med CIM-format


### Ursprungligt förslag: 
Lastprofilsgenerator som efter användarens specifikationer skapar tidsserier kopplade till en nätmodell i CIM.
Funktionalitet 
1.	Användaren matar in nätmodell i CIM, och får ut (syntetiska) lastprofiler och produktionsprofiler för nätets bussar i CIM-format.
2.	Användaren kan välja önskad längd och upplösning på tidserierna. 
3.	Användaren kan definiera att få ut probabilistiska profiler istället för tidsserier. Detta görs genom att med post-processing göra om tidsserier till probabilistiska fördelningar (parameter-beskrivning).
4.	Vid inmatning av probabilistiska profiler görs dessa om till CIM-kompatibelt format så att probabilistisk analys kan köras på nätmodellen.
5.	Den CIM-modell (med syntetiska data) som användaren får ut kan importeras till PowerFactory, som kan användas som lastflödeslösare eller probabilistisk analys.

![image](https://github.com/alicekjansson/CIMProject/assets/128380748/c676b32e-d4f9-4519-9f5d-aeec8f0e2c17)

