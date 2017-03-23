class Message(object):
    def __init__(self, time_stamp):
        self.time_stamp = time_stamp

    def time_stamp(self):
        return self.time_stamp

    def emit(self):
        pass


class MessageQueue(object):
    def __init__(self, delay):
        self.time = 0
        self.data = []
        self.delay = delay

    def step_run(self, increment):
        self.time += increment
        for ele in self.data:
            if self.time - ele.time_stamp() > self.delay:
                ele.emit()

    def add_msg(self, msg):
        self.data.append(msg)



class ControllerMessage(Message):
    def __init__(self, intersection, sensor, q_length, time_stamp, c_lib):
        super(ControllerMessage, self).__init__(time_stamp)
        self.intersection = intersection
        self.sensor = sensor
        self.q_length = q_length
        self.c_lib = c_lib

    def emit(self):
        self.c_lib.handleTrafficSensorInput(self.sensor, self.q_length, self.intersection)


import traci


class SumoMessage(Message):
    def __init__(self, controller, lt_state, time_stamp):
        super(SumoMessage, self).__init__(time_stamp)
        self.controller = controller
        self.lt_state = lt_state

    def emit(self):
        traci.trafficlights.setRedYellowGreenState(self.controller , self.lt_state)