import test

class Param(object):
    def __init__(self, _controller, _phase):
        self.controller = _controller
        self.phase = _phase

    def __str__(self):
        return 'controller:' + self.controller + ', phase:' + self.phase
