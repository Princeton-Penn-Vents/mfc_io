print('Welcome to a simple python script to read and write to a LabJack')

print('Connecting to lab jack...')
import u3 #import the driver for the lab jack
d = u3.U3() #find the labjack and attach
print('Found a labjack!')

#Set up the addresses of the various pins
# Following example: https://labjack.com/support/software/examples/ud/labjackpython/modbus
AIN0_REGISTER = 0
AIN1_REGISTER = 2
DAC0_REGISTER = 5000

import numpy as np # import numpy, python's numberical library
import time # import timing library


sampling_freq = 10 #Hz (approximate)

Vout_array = np.array([])
Vin0_array = np.array([])
Vin1_array = np.array([])
timestamp_array = np.array([])

#setup file for writing:

from time import localtime, strftime
filename = strftime("%Y%m%d_%H%M", localtime()) + '.csv'


#Use this function to generate any arbitrary waveform output
from scipy import signal
def output_waveform(seconds):
    #Here we make a triangle wave
    peak_v = 5
    wave_form_step_size = 101
    triangle_wave = signal.triang(wave_form_step_size)
    period = 30 #seconds
    x = np.int(np.round(np.mod(seconds, period) / period * (wave_form_step_size-1)))

    voltage = triangle_wave[x] * peak_v
    return voltage


print("Hit Control-c at any point to quit")
print("WARNING: only use this software for SHORT recordings. Measurements are only saved at the end.")
start_time = time.time()  #seconds since 1970
try:
    while True:
        timestamp = time.time() - start_time
        timestamp_array = np.append(timestamp_array, timestamp)

        Vout = output_waveform(timestamp)
        d.writeRegister(DAC0_REGISTER, Vout)
        Vout_array = np.append(Vout_array, Vout)


        Vin0 = d.readRegister(AIN0_REGISTER)
        Vin0_array = np.append(Vin0_array, Vin0)

        Vin1 = d.readRegister(AIN1_REGISTER)
        Vin1_array = np.append(Vin1_array, Vin1)



        print("DAC0 %.3f V, AIN0 = %.3f V, AIN1 = %.3f V, Seconds = %.1f s" % (Vout, Vin0, Vin1, timestamp))

        # Wait one interval of the sampling rate
        time.sleep(1 / sampling_freq)

except KeyboardInterrupt:
    print("writing file " + filename)
    header = "DAC0, AIN0, AIN1, Time"
    np.savetxt(filename, np.transpose([Vout_array, Vin0_array, Vin1_array, timestamp_array]), header=header, delimiter=',')
    print("written!")
    pass
