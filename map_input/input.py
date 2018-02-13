import pygame
from multiprocessing import Manager, Process

_manager = Manager()
_mapping = _manager.dict()
event_queue = _manager.Queue()
_initialized = False
_joysticks = list()


def un_intialize():
    """Currently not used... the process stops by itself... maybe look into this?"""
    if _initialized:
        pygame.event.post(pygame.QUIT)

    pygame.quit()


def initialize(joystick=True):
    """Initialize pygame & joystick"""
    controller = 0  # TODO what to do here
    global _initialized

    if not _initialized:
        pygame.init()

        # Initialize a display so we can capture keyboard input too
        pygame.display.set_mode((10, 10))

        _initialized = True

    if joystick:
        if not pygame.joystick.get_init():
            pygame.joystick.init()

        if pygame.joystick.get_count() == 0:
            raise Exception('No controller found')
        else:
            _joysticks.append(pygame.joystick.Joystick(controller))
            _joysticks[len(_joysticks)-1].init()
            print('Controller \'{}\' connected'.format(_joysticks[0].get_name()))


class Input(object):
    TYPE = 0
    VALUE = 1
    CALLBACK = 1

    def __init__(self, mapping=None):
        self._mapping = mapping
        self._keyboard_map = mapping['keyboard']
        self._joystick_map = mapping['joystick']
        self._joystick_buttons = self._joystick_map['buttons']
        self._joystick_axes = self._joystick_map['axis']

    def run(self):
        types = {
            pygame.KEYDOWN: 'key_down',
            pygame.KEYUP: 'key_up',
            pygame.JOYBUTTONDOWN: 'key_down',
            pygame.JOYBUTTONUP: 'key_up',
        }

        while True:
            event = pygame.event.wait()

            if event.type == pygame.QUIT:
                break

            event_type = event.type
            data = None

            # Keyboard configuration: Map keys to an event
            if event_type in [pygame.KEYDOWN, pygame.KEYUP]:
                try:
                    key = event.unicode
                except AttributeError:
                    key = chr(event.key)

                # if the key and type is mapped in the mapping configuration, emit the event
                if key in self._keyboard_map and types[event_type] in self._keyboard_map[key]:
                    data = self._keyboard_map[key][types[event_type]]  # keyboard mapping takes raw values

            # Joystick configuration: Map joystick buttons to an event
            elif event_type in [pygame.JOYBUTTONUP, pygame.JOYBUTTONDOWN]:
                button = event.button

                # if the button and type is mapped in the mapping configuration, emit the event
                if button in self._joystick_buttons and types[event_type] in self._joystick_buttons[button]:
                    data = self._joystick_buttons[button][types[event_type]]  # joystick button mapping takes raw values

            # Joystick configuration: Map joystick axes to an event
            elif event_type == pygame.JOYAXISMOTION:
                axis = event.axis
                value = event.value

                if axis in self._joystick_axes:
                    mapped_data = self._joystick_axes[axis]
                    data = (mapped_data[Input.TYPE], mapped_data[Input.CALLBACK](value))

            if data is not None:
                event_queue.put(data)


class InputProcess(object):
    def __init__(self, mapping=None):
        initialize()
        i = Input(mapping)

        self.process = Process(target=i.run)

    def start(self):
        self.process.start()

    def stop(self):
        print('Terminating Input object')
        self.process.terminate()
        print('Joining Input object')
        self.process.join()
        print('Input object DONE')
