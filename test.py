from map_input.input import InputThread

# from collections import namedtuple
# Pitch = namedtuple('Pitch', 'value')

# ======================================
# controls.py
from enum import Enum


class Controls(Enum):
    YAW = 0
    PITCH = 1
    ROLL = 2
    THROTTLE = 3
    TEST = 10


class CommandEvent(Enum):
    ENTER_FLIGHT_MODE = 0
    EXIT_FLIGHT_MODE = 1

YAW = 0
PITCH = 1
ROLL = 2
THROTTLE = 3
TEST = 10
# ======================================


def convert_to_flight_units(x):
    return int(50*x + 50)


FULL_POSITIVE = convert_to_flight_units(1)
FULL_NEGATIVE = convert_to_flight_units(-1)
LEVEL = convert_to_flight_units(0)


mapping = {
    'keyboard': {
        'w': {  # key
            'key_down': (PITCH, FULL_NEGATIVE),  # event. these take raw values
            'key_up': (PITCH, LEVEL),  # event
        },
        's': {
            'key_down': (PITCH, FULL_POSITIVE),
            'key_up': (PITCH, LEVEL),
        },
        'a': {
            'key_down': (ROLL, FULL_NEGATIVE),
            'key_up': (ROLL, LEVEL),
        },
        'd': {
            'key_down': (ROLL, FULL_POSITIVE),
            'key_up': (ROLL, LEVEL),
        },
        'q': {
            'key_down': (YAW, FULL_NEGATIVE),
            'key_up': (YAW, LEVEL),
        },
        'e': {
            'key_down': (YAW, FULL_POSITIVE),
            'key_up': (YAW, LEVEL),
        },
        '1': {
            'key_down': (THROTTLE, 10),
        },
        '2': {
            'key_down': (THROTTLE, 20),
        },
        '3': {
            'key_down': (THROTTLE, 30),
        },
        '4': {
            'key_down': (THROTTLE, 40),
        },
        '5': {
            'key_down': (THROTTLE, 50),
        },
        '6': {
            'key_down': (THROTTLE, 60),
        },
        '7': {
            'key_down': (THROTTLE, 70),
        },
        '8': {
            'key_down': (THROTTLE, 80),
        },
        '9': {
            'key_down': (THROTTLE, 90),
        },
        '0': {
            'key_down': (THROTTLE, 100),
        },
        '`': {
            'key_down': (THROTTLE, 0),
        },
        '\\': {
            'key_down': (THROTTLE, 0),
        },
    },
    'joystick': {
        'axis': {
            0: (ROLL, convert_to_flight_units),
            1: (PITCH, convert_to_flight_units),  # this takes a callback
            3: (YAW, convert_to_flight_units),
            5: (THROTTLE, convert_to_flight_units),
        },
        'buttons': {
            1: {
                'key_down': (TEST, 1),
            }
        },
    },
}

mapping_two = {
    'keyboard': {},
    'joystick': {
        'axis': {
            0: (ROLL, convert_to_flight_units),
            1: (PITCH, convert_to_flight_units),  # this takes a callback
            3: (YAW, convert_to_flight_units),
            5: (THROTTLE, convert_to_flight_units),
        },
        'buttons': {
            1: {
                'key_down': (TEST, 1),
            }
        },
    },
}

non_flight = {
    'keyboard': {
        'f': {
            'key_down': (CommandEvent.ENTER_FLIGHT_MODE, ),
        },
    },
    'joystick': {
        'axis': {
        },
        'buttons': {
        },
    },
}

flight = {
    'keyboard': {
        'f': {
            'key_down': (CommandEvent.EXIT_FLIGHT_MODE, ),
        },
        'w': {  # key
            'key_down': (Controls.PITCH, FULL_NEGATIVE),  # event. these take raw values
            'key_up': (Controls.PITCH, LEVEL),  # event
        },
        's': {
            'key_down': (Controls.PITCH, FULL_POSITIVE),
            'key_up': (Controls.PITCH, LEVEL),
        },
        'a': {
            'key_down': (Controls.ROLL, FULL_NEGATIVE),
            'key_up': (Controls.ROLL, LEVEL),
        },
        'd': {
            'key_down': (Controls.ROLL, FULL_POSITIVE),
            'key_up': (Controls.ROLL, LEVEL),
        },
    },
    'joystick': {
        'axis': {
        },
        'buttons': {
        },
    },
}


class UserInput(object):
    def __init__(self, event_queue):
        self._input = None
        self.event_queue = event_queue

    def flight(self):
        self.stop()

        self._input = InputThread(self.event_queue, flight)
        self._input.start()

    def non_flight(self):
        self.stop()

        self._input = InputThread(self.event_queue, non_flight)
        self._input.start()

    def stop(self):
        if self._input is not None:
            self._input.stop()

    def run(self):
        while True:
            event = self.event_queue.get()
            print(event)

            if event[0] == CommandEvent.ENTER_FLIGHT_MODE:
                self.flight()
            if event[0] == CommandEvent.EXIT_FLIGHT_MODE:
                self.non_flight()


def test():
    from queue import Queue
    import signal
    import sys

    event_queue = Queue()

    ui = UserInput(event_queue)
    ui.non_flight()

    def signal_handler(sig_num, frame):
        print('captured signal')
        ui.stop()
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    ui.run()


if __name__ == '__main__':
    test()

