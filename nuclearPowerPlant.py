from fei.ppds import Mutex, Semaphore, Thread, Event, print
from time import sleep
from random import randint


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


class PowerPlant:
    def __init__(self):
        self.turnstile = Semaphore(1)
        self.monitors = LightSwitch()
        self.sensors = LightSwitch()
        self.validData = Event()


def monitor(monitor_id, system_control, access_data):
    # monitor nemôže pracovať, kým nie je aspoň 1 platný údaj v úložisku
    system_control.validData.wait()

    while True:
        # monitor má prestávku 500 ms od zapnutia alebo poslednej aktualizácie
        sleep(0.5)

        # zablokujeme turniket, aby sme vyhodili čidlá z KO
        system_control.turnstile.wait()
        # získame prístup k úložisku
        monitors_read = system_control.monitors.lock(access_data)
        system_control.turnstile.signal()

        # prístup k údajom simulovaný nasledovným výpisom
        print(f'monitor {monitor_id:02d}: {monitors_read:02d}')
        # aktualizovali sme údaje, odchádzame z úložiska
        system_control.monitors.unlock(access_data)


def sensor(sensor_id, system_control, access_data):
    while True:
        # čidlá prechádzajú cez turniket, pokým ho nezamkne monitor
        system_control.turnstile.wait()
        system_control.turnstile.signal()

        # získame prístup k úložisku
        sensors_read = system_control.sensors.lock(access_data)
        # prístup k údajom simulovaný čakaním v intervale 10 až 15 ms
        # podľa špecifikácie zadania informujeme o čidle a zápise, ktorý ide vykonať
        write_time = randint(10, 15)
        print(f'sensor {sensor_id:02d}:  {sensors_read:02d}, {write_time} ms')
        sleep(write_time / 1000)
        # po zapísaní údajov signalizujeme, že údaj je platný
        system_control.validData.signal()
        # a odchádzame z úložiska preč
        system_control.sensors.unlock(access_data)


def main():
    accessData = Semaphore(1)
    system = PowerPlant()
    monitors = [Thread(monitor, monitor_id, system, accessData) for monitor_id in range(2)]
    sensors = [Thread(sensor, sensor_id, system, accessData) for sensor_id in range(11)]

    [t.join() for t in monitors + sensors]


if __name__ == '__main__':
    main()
