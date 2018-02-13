from setuptools import setup

setup(
    name='map_input',
    version='0.1.1',
    description='Map keyboard & joystick buttons/axes to events',
    license='MIT',
    author='Jesse Kleve',
    author_email='jesse.kleve@gmail.com',
    packages=['map_input'],
    install_requires=['pygame'],
    scripts=['map_input/input.py'],
)
