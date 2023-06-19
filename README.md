# CIMProject


Förslag: Lastprofilsgenerator som efter användarens specifikationer skapar tidsserier kopplade till en nätmodell i CIM.
Funktionalitet 
1.	Användaren matar in nätmodell i CIM, och får ut (syntetiska) lastprofiler och produktionsprofiler för nätets bussar i CIM-format.
2.	Användaren kan välja önskad längd och upplösning på tidserierna. 
3.	Användaren kan definiera att få ut probabilistiska profiler istället för tidsserier. Detta görs genom att med post-processing göra om tidsserier till probabilistiska fördelningar (parameter-beskrivning).
4.	Vid inmatning av probabilistiska profiler görs dessa om till CIM-kompatibelt format så att probabilistisk analys kan köras på nätmodellen.
5.	Den CIM-modell (med syntetiska data) som användaren får ut kan importeras till PowerFactory, som kan användas som lastflödeslösare eller probabilistisk analys.

![image](https://github.com/alicekjansson/CIMProject/assets/128380748/c676b32e-d4f9-4519-9f5d-aeec8f0e2c17)

