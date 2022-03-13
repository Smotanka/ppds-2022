from fei.ppds import Mutex, Semaphore, Thread, Event, print
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
                @param(sem) Object - Semaphore to lock
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
                @param(sem) Object - Semaphore to unlock
        """
        self.mutex.lock()
        self.cnt -= 1
        if self.cnt == 0:
            sem.signal()
        self.mutex.unlock()


class SensorType(Enum):
    P = 1
    H = 2
    T = 3


class PowerPlant:
    def __init__(self):
        self.turnstile = Semaphore(1)
        self.monitors = LightSwitch()
        self.sensors = LightSwitch()
        self.validDataP = Event()
        self.validDataT = Event()
        self.validDataH = Event()


def monitor(monitor_id, system_control, access_data):
    # monitor nemôže pracovať, kým nie je aspoň 1 platný údaj v úložisku
    system_control.validDataP.wait()
    system_control.validDataT.wait()
    system_control.validDataH.wait()

    while True:
        # monitor má prestávku 500 ms od zapnutia alebo poslednej aktualizácie
        # zablokujeme turniket, aby sme vyhodili čidlá z KO
        system_control.turnstile.wait()
        # získame prístup k úložisku
        monitors_read = system_control.monitors.lock(access_data)
        system_control.turnstile.signal()
        # prístup k údajom simulovaný nasledovným výpisom
        read_time = randint(40, 50)
        sleep(read_time / 1000)
        print(f'monitor {monitor_id:02d}: {monitors_read:02d}, read time: {read_time:02d}')

        # aktualizovali sme údaje, odchádzame z úložiska
        system_control.monitors.unlock(access_data)


def sensor(sensor_id, system_control, access_data, sensor_type):
    while True:

        # čidlá prechádzajú cez turniket, pokým ho nezamkne monitor
        system_control.turnstile.wait()
        system_control.turnstile.signal()
        sleep(randint(50, 60) / 1000)
        # získame prístup k úložisku
        sensors_read = system_control.sensors.lock(access_data)
        # prístup k údajom simulovaný čakaním v intervale 10 až 15 ms
        # podľa špecifikácie zadania informujeme o čidle a zápise, ktorý ide vykonať

        if sensor_type is SensorType.H:
            write_time = randint(20, 25)
        else:
            write_time = randint(10, 20)
        sleep(write_time / 1000)
        print(f'sensor {sensor_id:02d} of type {sensor_type.name}:  {sensors_read:02d}, {write_time} ms')

        # po zapísaní údajov signalizujeme, že údaj je platný

        if sensor_type is SensorType.P:
            system_control.validDataP.signal()
        elif sensor_type is SensorType.T:
            system_control.validDataT.signal()
        else:
            system_control.validDataH.signal()
        # a odchádzame z úložiska preč
        system_control.sensors.unlock(access_data)


def main():
    accessData = Semaphore(1)
    system = PowerPlant()
    types = [SensorType.H, SensorType.P, SensorType.T]
    monitors = [Thread(monitor, monitor_id, system, accessData) for monitor_id in range(8)]
    sensors = [Thread(sensor, sensor_id, system, accessData, types[sensor_id]) for sensor_id in range(3)]

    [t.join() for t in monitors + sensors]


if __name__ == '__main__':
    main()
