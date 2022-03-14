"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/4-cvicenie-vecerajuci-filozofi-atomova-elektraren-%f0%9f%8d%bd%ef%b8%8f/"""

# Python v3.10
# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Mutex
from fei.ppds import Thread
from fei.ppds import Semaphore
from fei.ppds import Event
from fei.ppds import print

from time import sleep
from random import randint

"""Disclaimer! This code is only transcript of pseudocode to Python language  made by Mgr. Ing. Matúš Jókay, PhD.
for more see: https://www.youtube.com/watch?v=DgI8E_bVfBA"""


class LightSwitch(object):
    """
        LightSwitch object that implement switching between semaphores.
    """

    def __init__(self):
        """
            Initialize 'LightSwitch' instance with counter and lock.
        """
        self.cnt = 0
        self.mutex = Mutex()

    def lock(self, sem):
        """
            Lock the all threads in 'semaphore' object
               :param sem: Object - Semaphore to lock
        """
        self.mutex.lock()
        counter = self.cnt
        self.cnt += 1
        if self.cnt == 1:
            sem.wait()
        self.mutex.unlock()
        return counter

    def unlock(self, sem):
        """
            Unlock the threads in 'semaphore' object
                :param sem: Object - Semaphore to unlock
        """
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()


class PowerPlant:
    """
        Shared class that wraps the synchronization objects
    """

    def __init__(self):
        self.turnstile = Semaphore(1)
        self.monitors = LightSwitch()
        self.sensors = LightSwitch()
        self.validData = Event()


def monitor(monitor_id, system_control, access_data):
    """
    Function that represent the monitor that read and actualize data on monitors

    :param monitor_id: int - Identification number of monitor function that is called by the 'Thread'
    :param system_control: Object - 'PowerPlant' class that encapsulates the synchronization objects
    :param access_data:  Object - 'Semaphore' object that simulates the shared data for monitors to show
    """

    # Wait for data
    system_control.validData.wait()
    # Read and show collected data
    while True:
        sleep(0.5)  # Data are accessed every 500 ms
        system_control.turnstile.wait()

        monitors_read = system_control.monitors.lock(access_data)
        system_control.turnstile.signal()

        print(f'monitor {monitor_id:02d}: {monitors_read:02d}')
        system_control.monitors.unlock(access_data)


def sensor(sensor_id, system_control, access_data):
    """

    Function that represent the sensors that collects data

    :param sensor_id: int - Identifier of current sensor called by 'Thread' object
    :param system_control: Object - 'PowerPlant' object for synchronization
    :param access_data: Object - 'Semaphore' object that simulates the shared data for monitors to show
    """

    # Collect Data
    while True:

        system_control.turnstile.wait()
        system_control.turnstile.signal()

        sensors_read = system_control.sensors.lock(access_data)
        write_time = randint(10, 15)  # Simulates the time needed to store data
        print(f'sensor {sensor_id:02d}:  {sensors_read:02d}, {write_time} ms')
        sleep(write_time / 1000)

        system_control.validData.signal()
        system_control.sensors.unlock(access_data)


def main():
    # init
    accessData = Semaphore(1)
    system = PowerPlant()
    monitors = [Thread(monitor, monitor_id, system, accessData) for monitor_id in range(2)]
    sensors = [Thread(sensor, sensor_id, system, accessData) for sensor_id in range(11)]

    # this line is redundant, is here only for good practice to safely let threads cease to exist
    [t.join() for t in monitors + sensors]


if __name__ == '__main__':
    main()
