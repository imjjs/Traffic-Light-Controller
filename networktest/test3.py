#/usr/bin/python
import re
import ctypes


t = 'handleTrafficSensorInput():	Sensor:S32	NumVehicles:1	controllerID: Controller1443088096	CurrentTime:119'

sensorPattern = re.compile(r'^handleTrafficSensorInput.+?Sensor\:(.+?)\tNumVehicles\:(\d+?)\tcontrollerID\:(.+?)\tCurrentTime\:(\d+)')
test = ctypes.cdll.LoadLibrary('build/libtest.so')

if __name__ == '__main__':
    #res = sensorPattern.match(t)
    #print res.group(1),res.group(2),res.group(3),res.group(4)
    inp = open('sumoInputForController.txt', 'r')
    lines = inp.readlines()
    test.test_init()

    for l in lines:
        res = sensorPattern.match(l)
        if res == None:
            continue
        sensor = str(res.group(1))
        qlength = int(res.group(2))
        controllerID = str(res.group(3))
        time = ctypes.c_float(float(res.group(4)))
        print sensor, qlength, controllerID, time
        #test.handleTrafficSensorInput(sensor,qlength,controllerID)
        test.handleTrafficSensorInput2('S11',0,'Controller202407913',ctypes.c_float(2.0))
        test.handleTrafficSensorInput2( sensor, qlength, controllerID, time)
