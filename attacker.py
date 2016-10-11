import test
import sys
import ast
import subprocess
import multiprocessing
CoreNumber = multiprocessing.cpu_count()

def warp(tup):
    para = tup[0]
    s = tup[1]
    speed = subprocess.check_output(["python", "test.py", str(para).replace(' ','') , '"' + str(s) +'"'])
    return (speed, s)

def start_process():
    pass



if __name__ == '__main__':
    raw_para = sys.argv[1]
    para = ast.literal_eval(raw_para)
    sensors = test.findSensors()
    ret = []
    pool = multiprocessing.Pool(processes = CoreNumber,
                            initializer = start_process)
    inputList = []

    for s in sensors:
        tmp = []
        tmp.append(s)
        inputList.append((para, tmp))
    print inputList
    result = pool.map(warp,inputList)
    #result = map(mytestWarp, inputList)
    pool.close()
    pool.join()

    speed, sensor = min(result, key = lambda x: x[0])
    print speed, sensor
