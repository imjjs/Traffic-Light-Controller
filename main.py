import sys

import subprocess
import multiprocessing

import test
import time
import random
import config

CoreNumber = multiprocessing.cpu_count()

TestPeriod = 36000
testRange = (0, 30)
stepLength = 1

def mytestWarp(tup):
    para = tup[1]
    idx = tup[2]
    para[idx] = tup[0]
    speed = 0.0
    while True:
        try:
            speed = subprocess.check_output(["python", "test.py", str(para).replace(' ','')] )#, stdout= DEVNULL, stderr = DEVNULL)
        except subprocess.CalledProcessError as grepexc:
            print "error code", grepexc.returncode, grepexc.output
            continue
        break
    return (float(speed), int(tup[0]))


def start_process():
    pass

if __name__ == '__main__':
    #log.LogTime = time.time()
    #with open('logtime','w') as f:
    #    f.write(str(log.LogTime))
    count = 0
    dim = 19
    paraList = [5, 6, 13, 1, 1, 2, 22, 13, 9, 16, 20, 19, 6, 10, 4, 25, 1, 22, 0]
    #for i in range(dim):
    #    paraList.append(testRange[0])
    meta_param = test.findPhase()
    idx = 0
    while True:
        mark = False
        for idx in range(dim):
            #if not meta_param[idx].controller in config.blue:
            #    continue
            print idx
            pool = multiprocessing.Pool(processes = CoreNumber,
                                    initializer = start_process)
            inputList = []

            for i in range(testRange[0], testRange[1], stepLength):
                inputList.append((i, paraList, idx))

            result = pool.map(mytestWarp,inputList)
            #result = map(mytestWarp, inputList)
            pool.close()
            pool.join()

            f = open("intersection" + str(idx) + ".txt", "a")
            for i in result:
                print i[0], i[1]
                f.write(str(i[0]) +str(i[1])  + '\n')

            maxSpeed, maxThreshold = max(result, key = lambda x: x[0])
            f.write("final:"+ str(maxSpeed) + ',' + str(maxThreshold) + ',' + str(paraList))

            #minDuration, minWeThreshold, minNsThreshold = min(result, key = lambda x: x[0])
            #f.write("final:"+ str(minDuration) + ',' + str(minWeThreshold) + ',' + str(minNsThreshold))
            if paraList[idx] != maxThreshold:
                mark = True

            paraList[idx] = maxThreshold
            f.flush()
            time.sleep(10)
            print "sleeping at loot--------"
        if False == mark:
            break

    print paraList
    print count
