An extremely simple script to read and write voltages from a labjack A to D.
This is designed to read the voltage from an Aalborg Mass Flow Controller.

A couple of different use cases are envisioned
MFC flow is read in by the LabJack on AIN0 and GND.

If an external source, like a function generator is driving the set point, that is read on AIN1 and GND.
If the computer is generating the setpoint, that is outputted on DAC0 and GND.

The script will read and write to the labjack at an approximate sample rate. To finish a run, type control-c. The voltages and teimstamps are saved in a CSV file.

Note currently saving only occurs at the very end. If you want to make long or overnight runs, let me know and I will modify the code.

TO INSTALL:

Download the exodriver for macos:
https://labjack.com/sites/default/files/Exodriver_NativeUSB_Setup.zip
and install.


Make sure you are running python 3.

cd into the LabJackPython-2.0.0 directory and run:
>> sudo python setup.py install
or if that doesnt' work
>> python setup.py install
