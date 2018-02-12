from map_input.input import event_queue, InputProcess

# from collections import namedtuple
# Pitch = namedtuple('Pitch', 'value')

YAW = 0
PITCH = 1
ROLL = 2
THROTTLE = 3
TEST = 10


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


def test():
    i = InputProcess(mapping)
    i.start()

    j = 0

    while True:
        event = event_queue.get()
        print(event)
        j += 1
        if j > 10:
            break

    i.stop()
    print('exitting ...')

    i = InputProcess(mapping_two)
    i.start()

    j = 0

    while True:
        event = event_queue.get()
        print(event)
        j += 1
        if j > 10:
            break

    i.stop()
    print('exitting ...')


if __name__ == '__main__':
    test()
