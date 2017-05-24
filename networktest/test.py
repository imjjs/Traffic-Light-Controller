import ctypes
import sys
sys.path.append("/home/liy29/sumo-0.26.0/tools/")

import traci
from threading import Lock
import socket
import subprocess
import os
import time

import ast
import config

try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET


PORT_LOCK = Lock()
DEVNULL = open(os.devnull, "w")

selected_intersections =  ["Controller1/2" , "Controller2/2", "Controller1/1", "Controller2/1"]
phaseCodes = {
"Controller1/2":["GGggrrrrGGggrrrr", "yyggrrrryyggrrrr", "rrGGrrrrrrGGrrrr", "rryyrrrrrryyrrrr", "rrrrGGggrrrrGGgg", "rrrryyggrrrryygg", "rrrrrrGGrrrrrrGG", "rrrrrryyrrrrrryy"],
"Controller2/2":["GGggrrrrGGggrrrr", "yyggrrrryyggrrrr", "rrGGrrrrrrGGrrrr", "rryyrrrrrryyrrrr", "rrrrGGggrrrrGGgg", "rrrryyggrrrryygg", "rrrrrrGGrrrrrrGG", "rrrrrryyrrrrrryy"],
"Controller1/1":["GGggrrrrGGggrrrr", "yyggrrrryyggrrrr", "rrGGrrrrrrGGrrrr", "rryyrrrrrryyrrrr", "rrrrGGggrrrrGGgg", "rrrryyggrrrryygg", "rrrrrrGGrrrrrrGG", "rrrrrryyrrrrrryy"],
"Controller2/1":["GGggrrrrGGggrrrr", "yyggrrrryyggrrrr", "rrGGrrrrrrGGrrrr", "rryyrrrrrryyrrrr", "rrrrGGggrrrrGGgg", "rrrryyggrrrryygg", "rrrrrrGGrrrrrrGG", "rrrrrryyrrrrrryy"]
}


intersection_info = {
    "Controller1/2": {
        "PhaseToState": {
            "0": "0101",
            "1": "0101",
            "2": "0101",
            "3": "0000",
            "4": "1010",
            "5": "1010",
            "6": "1010",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "e3_1/2_0/2to1/2",
            "e3_1/2_1/3to1/2",
            "e3_1/2_2/2to1/2",
            "e3_1/2_1/1to1/2"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller2/2": {
        "PhaseToState": {
            "0": "0101",
            "1": "0101",
            "2": "0101",
            "3": "0000",
            "4": "1010",
            "5": "1010",
            "6": "1010",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "e3_2/2_1/2to2/2",
            "e3_2/2_2/3to2/2",
            "e3_2/2_3/2to2/2",
            "e3_2/2_2/1to2/2"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller1/1": {
        "PhaseToState": {
            "0": "0101",
            "1": "0101",
            "2": "0101",
            "3": "0000",
            "4": "1010",
            "5": "1010",
            "6": "1010",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "e3_1/1_0/1to1/1",
            "e3_1/1_1/2to1/1",
            "e3_1/1_2/1to1/1",
            "e3_1/1_1/0to1/1"
        ],
        "threshold1": 3,
        "threshold2": 4
    },
    "Controller2/1": {
        "PhaseToState": {
            "0": "0101",
            "1": "0101",
            "2": "0101",
            "3": "0000",
            "4": "1010",
            "5": "1010",
            "6": "1010",
            "7": "0000"
        },
        "maxInterval": 600,
        "minInterval": 200,
        "phases": [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7"
        ],
        "sensors": [
            "e3_2/1_1/1to2/1",
            "e3_2/1_2/2to2/1",
            "e3_2/1_3/1to2/1",
            "e3_2/1_2/0to2/1"
        ],
        "threshold1": 3,
        "threshold2": 4
    }
    
}
sensor_num = {'S1':2, 'S2':2, 'S3':2, 'S4':3, 'S9':3, 'S10':3, 'S11':2, 'S12':3, 'S13':3, 'S14':2, 'S15':1, 'S24':2, 'S25':2, 'S26':2, 'S27':2, 'S32':3, 'S33':3, 'S34':2, 'S35':1}
test = ctypes.cdll.LoadLibrary('build/libtest.so')

def findPhase():
    ret = []
    for i in selected_intersections:
        phases = phaseCodes[i]
        for idx in range(len(phases)):
            phase = phases[idx]
            if 'y' in phase:
                continue
            obj = config.Param(i, idx)
            ret.append(obj)
    return ret


def get_open_port(howMany=1):
    """Return a list of n free port numbers on localhost"""
    results = []
    sockets = []
    i=0
    while i < howMany:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(('localhost', 0))
        # work out what the actual port number it's bound to is
        addr, port = s.getsockname()
        if port < 40000:
            s.close()
            continue
        results.append(port)
        sockets.append(s)
        i += 1
    for s in sockets:
        s.close()

    return results

def generator_ports():
    PORT_LOCK.acquire()
    ports = get_open_port(1)
    PORT_LOCK.release()
    return ports[0]


def durationAndDistance(port):
    xmlfile = open("tripinfo" + str(port) + ".xml", 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalDuration = 0
    totalDistance = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalDuration += float(child.attrib['duration'])
        totalDistance += float(child.attrib['routeLength'])
    xmlfile.close()
    os.remove("tripinfo" + str(port) + ".xml")
    return totalDistance/ totalDuration

import submap
def submapUtility(port, name):
    maps = submap.Submap.generate_submaps(os.path.join('submap', config.submap_region))
    distance, avg = submap.get_matric(maps, str(port) +'edge_info.xml')
    #os.remove(str(port) + 'edge_info.xml')
    #os.remove(str(port) + 'tripinfo.xml')
    #f = open("utility"+str(port)+".txt","w")
    #f.write(str(avg) + '\n' + str(distance))
    if 'global' == name:
        return avg
    else:
        return distance[name]


def avgSpeed(filename):
    xmlfile = open(filename, 'r')
    xmlTree = ET.parse(xmlfile)
    treeRoot = xmlTree.getroot()
    totalSpeed = 0
    carNumber = len(treeRoot)
    for child in treeRoot:
        totalSpeed += float(child.attrib['routeLength'])/float(child.attrib['duration'])
    avgspeed = totalSpeed * 1.0 / carNumber

    xmlfile.close()
    os.remove(filename)
    return avgspeed

def findSensors():
    ret = []
    for i in selected_intersections:
        sensors = intersection_info[i]['sensors']
        for s in sensors:
            ret.append(s)
    return ret

def simulationProcess(paraList, sumoMap, player, ignore = None):
    port = generator_ports()
    sumoProcess = subprocess.Popen(
        ["sumo", "-c", sumoMap, "--tripinfo-output", "tripinfo.xml",
         "--remote-port", str(port), "--output-prefix", str(port)], stdout= DEVNULL, stderr = DEVNULL)
    time.sleep(10)

    traci.init(port)
    meta_param = findPhase()
    #print "meta_param,", len(meta_param)
    #print "paraList,", len(paraList)
    assert(len(meta_param) == len(paraList))
    test.test_init()
    for idx in range(len(meta_param)):
        obj = meta_param[idx]
        ins_name = obj.controller
        ins_phase = obj.phase
        ins_threshold = paraList[idx]
        test.setThreshold(ins_name, ins_threshold, ins_phase)
        #test.debug()
    #print "after seeting threshold"
    for s in range(30000):
        traci.simulationStep()
        if not s % 10 == 0:
            continue
        for i in selected_intersections:
            sensors = intersection_info[i]['sensors']
            for s in sensors:
                if s in ignore:
                    continue
                data = 0
                # for t in range(sensor_num[s]):
                #     data += traci.areal.getLastStepVehicleNumber(s + '#' + str(t))
                data = traci.multientryexit.getLastStepVehicleNumber(s)
                #print "data:" + str(data) + ', sensor:' + str(s)
                test.handleTrafficSensorInput(s, data, i)
            res = test.nextClockTick(i)
            ltState = phaseCodes[i][res]
            traci.trafficlights.setRedYellowGreenState(i[10:], ltState)


    traci.close()
    sumoProcess.wait()
    time.sleep(10)

    return submapUtility(port, player)
    #return  durationAndDistance(port)

def simulationProcess2( sumoMap, ignore = None):
    port = generator_ports()
    sumoProcess = subprocess.Popen(
        ["sumo", "-c", sumoMap, "--tripinfo-output", "tripinfo.xml",
         "--remote-port", str(port), "--output-prefix", str(port)], stdout= DEVNULL, stderr = DEVNULL)
    time.sleep(10)

    traci.init(port)
    test.test_init()
    test.debug()
    for s in range(50000):
        traci.simulationStep()
        if not s % 10 == 0:
            continue
        for i in selected_intersections:
            sensors = intersection_info[i]['sensors']
            for s in sensors:
                if s in ignore:
                    continue
                data = 0
                # for t in range(sensor_num[s]):
                #     data += traci.areal.getLastStepVehicleNumber(s + '#' + str(t))
                data = traci.multientryexit.getLastStepVehicleNumber(s)
                #print "data:" + str(data) + ', sensor:' + str(s)
                test.handleTrafficSensorInput(s, data, i)
            res = test.nextClockTick(i)
            ltState = phaseCodes[i][res]
            traci.trafficlights.setRedYellowGreenState('tl' + i[10:], ltState)


    traci.close()
    sumoProcess.wait()
    time.sleep(10)

    return  durationAndDistance(port)

if __name__ == '__main__':
    #simulationProcess([0,5], '../sumo/Vanderbilt.sumo.cfg')
    ignore = config.ignore_sensors
    #print sys.argv[1]
    if len(sys.argv) == 5:
        ignore = ast.literal_eval(sys.argv[4])
    raw_para = sys.argv[1]
    para = ast.literal_eval(raw_para)
    if len(sys.argv) >= 4:
        print  simulationProcess(para, sumoMap = sys.argv[2], player = sys.argv[3], ignore = ignore)
    else:
        print  simulationProcess(para, sumoMap = './sumo/grid.sumo.cfg', player = 'global', ignore = ignore)
    #print  simulationProcess([0,5,2,3,7,4,1,6,4,9], './sumo/Vanderbilt.sumo.cfg')
