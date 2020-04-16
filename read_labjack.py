print('Welcome to a simple python script to read and write to a LabJack')

print('Connecting to lab jack...')
import u3 #import the driver for the lab jack
d = u3.U3() #find the labjack and attach
#Set up the addresses of the various pins
# Following example: https://labjack.com/support/software/examples/ud/labjackpython/modbus
AIN0_REGISTER = 0
AIN1_REGISTER = 2
print('Found a labjack!')




import numpy as np # import numpy, python's numberical library
import time # import timing library


sampling_freq = 10 #Hz (approximate)

Vin0_array = np.array([])
Vin1_array = np.array([])
timestamp_array = np.array([])

#setup file for writing:

from time import localtime, strftime
filename = strftime("%Y%m%d_%H%M", localtime()) + '.csv'


print("Hit Control-c at any point to quit")
try:
    while True:

        Vin0 = d.readRegister(AIN0_REGISTER)
        Vin0_array = np.append(Vin0_array, Vin0)

        Vin1 = d.readRegister(AIN1_REGISTER)
        Vin1_array = np.append(Vin1_array, Vin1)

        timestamp = time.time() #seconds since 1970
        timestamp_array = np.append(timestamp_array, timestamp)

        print("AIN0 = %.3f V, AIN1 = %.3f V, Seconds Since 1970 = %.1f s" % (Vin0, Vin1, timestamp))

        # Wait one interval of the sampling rate
        time.sleep(1 / sampling_freq)

except KeyboardInterrupt:
    print("writing file " + filename)
    np.savetxt(filename, np.transpose([Vin0_array, Vin1_array, timestamp_array]), delimiter=',')
    print("written!")
    pass
