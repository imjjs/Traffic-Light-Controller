import test
import sys
import ast
import subprocess
import multiprocessing
CoreNumber = multiprocessing.cpu_count()

def warp(tup):
    para = tup[0]
    s = tup[1]
    #print ' '.join(["python", "test.py", str(para).replace(' ','') , '"' + str(s) +'"'])
    #speed = subprocess.check_output(["python", "test.py", "'" + str(para).replace(' ','') + "'" , '"' + str(s) +'"'])
    while True:
        try:
            speed = float(subprocess.check_output(["python", "test.py", str(para).replace(' ', ''), './sumo/Vanderbilt.sumo.cfg', 'global', str(s).replace(' ', '')]))
        except subprocess.CalledProcessError as grepexc:
            print "error code", grepexc.returncode, grepexc.output
            continue
        break

    #speed = test.simulationProcess(para,  './sumo/Vanderbilt.sumo.cfg', s)
    return (speed, s)

def start_process():
    pass



if __name__ == '__main__':
    raw_para = sys.argv[1]
    num = int(sys.argv[2])
    para = ast.literal_eval(raw_para)
    sensors = test.findSensors()
    ignore = []
    for n in range(num):
        ret = []
        pool = multiprocessing.Pool(processes = CoreNumber,
                                initializer = start_process)
        inputList = []

        for s in sensors:
            tmp = ignore + [s]
            inputList.append((para, tmp))

        result = pool.map(warp,inputList)
    #    result = map(warp, inputList)
        pool.close()
        pool.join()
        speed, sensor = min(result, key = lambda x: x[0])
        print speed, sensor
        ignore = sensor
    print ignore
