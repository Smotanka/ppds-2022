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
from enum import Enum


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
                :returns counter: int - Number of 'Semaphore' object that was by the lock method
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


class SensorType(Enum):
    """

    Enum class for the sensor types

    """
    P = 1
    H = 2
    T = 3


class PowerPlant:
    """
        Shared class that wraps the synchronization objects
    """
    def __init__(self):
        self.turnstile = Semaphore(1)
        self.monitors = LightSwitch()
        self.sensors = LightSwitch()
        self.validDataP = Event()
        self.validDataT = Event()
        self.validDataH = Event()


def monitor(monitor_id, system_control, access_data):
    """
    Function that represent the monitor that read and actualize data on monitors

    :param monitor_id: int - Identification number of monitor function that is called by the 'Thread'
    :param system_control: Object - 'PowerPlant' class that encapsulates the synchronization objects
    :param access_data:  Object - 'Semaphore' object that simulates the shared data for monitors to show
    """

    # Wait for all 3 types of sensors to provide data
    system_control.validDataP.wait()
    system_control.validDataT.wait()
    system_control.validDataH.wait()

    # Read and show the data
    while True:
        read_time = randint(40, 50)
        sleep(read_time / 1000)  # Simulates the time needed to access data

        system_control.turnstile.wait()

        monitors_read = system_control.monitors.lock(access_data)
        system_control.turnstile.signal()

        print(f'monitor {monitor_id:02d}: monitors read:{monitors_read:02d}, read time: {read_time:02d}')

        system_control.monitors.unlock(access_data)


def sensor(sensor_id, system_control, access_data, sensor_type):
    """

    Function that represent the sensors that collects data

    :param sensor_id: int - Identifier of current sensor called by 'Thread' object
    :param system_control: Object - 'PowerPlant' object for synchronization
    :param access_data: Object - 'Semaphore' object that simulates the shared data for monitors to show
    :param sensor_type: Enum - Type of sensor that is called by 'Thread' object
    """
    while True:

        system_control.turnstile.wait()
        system_control.turnstile.signal()
        sleep(randint(50, 60) / 1000)   # Collect data every 60 seconds

        sensors_read = system_control.sensors.lock(access_data)

        # Different sensor types have different wait times
        if sensor_type is SensorType.H:
            write_time = randint(20, 25)
        else:
            write_time = randint(10, 20)

        print(f'sensor {sensor_id:02d} of type {sensor_type.name}:  {sensors_read:02d}, {write_time} ms')
        sleep(write_time / 1000)  # Simulates the time needed to store data

        # For monitor function, that waits for all three sensor to collect data
        if sensor_type is SensorType.P:
            system_control.validDataP.signal()
        elif sensor_type is SensorType.T:
            system_control.validDataT.signal()
        else:
            system_control.validDataH.signal()

        system_control.sensors.unlock(access_data)


def main():
    # init
    accessData = Semaphore(1)
    system = PowerPlant()
    types = [SensorType.H, SensorType.P, SensorType.T]
    monitors = [Thread(monitor, monitor_id, system, accessData) for monitor_id in range(8)]
    sensors = [Thread(sensor, sensor_id, system, accessData, types[sensor_id]) for sensor_id in range(3)]

    # this line is redundant, is here only for good practice to safely let threads cease to exist
    [t.join() for t in monitors + sensors]


if __name__ == '__main__':
    main()
