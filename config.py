class Param(object):
    def __init__(self, _controller, _phase):
        self.controller = _controller
        self.phase = _phase

    def __str__(self):
        return 'controller:' + self.controller + ', phase:' + str(self.phase)

ignore_sensors = []


morning_opt = [5, 0, 17, 1, 0, 0, 0, 13, 0, 26, 8, 3, 7, 19, 0, 26, 1, 20, 0]
