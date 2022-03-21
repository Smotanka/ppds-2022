"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F"""

# Python v3.10
# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Semaphore
from fei.ppds import Mutex
from fei.ppds import print
from fei.ppds import Thread

from time import sleep
from random import randint

# Constants
N = 10  # Savages
M = 6   # Meals
C = 4   # Cooks


class SimpleBarrier(object):
    """
    Object that represents barrier synchronization method.
    """

    def __init__(self, number):
        """
        Initialize Barrier
        :param number: int: - Number of threads
        """

        self.number = number
        self.counter = 0
        self.mutex = Mutex()
        self.barrier = Semaphore(0)

    def wait(self, savage_id=None, cook_id=None):
        """
        Wait method, that holds code execution until all threads called this method
        :param savage_id: int: - Identification number of the savage that called this method
        :param cook_id: int: - Identification number of the cook that called this method
        :return:
        """

        self.mutex.lock()
        self.counter += 1

        if savage_id:
            print(f"Savage {savage_id}: I am here ! We are {self.counter}")
        if cook_id:
            print(f"Cook {cook_id}: I am awake ! We are {self.counter}")

        if self.counter == self.number:

            if savage_id:
                print(f"Savage {savage_id}: I am here ! I am the last one, We can EAT!!!\n")
            if cook_id:
                print(f"Cook {cook_id}: I am Awake ! I am the last one, We can cook\n")

            self.counter = 0
            self.barrier.signal(self.number)

        self.mutex.unlock()
        self.barrier.wait()


class Shared(object):
    """
    Shared object whose purpose is to sync all the other processes
    """
    def __init__(self, m):
        """
        Initialize 'Shared' object
        :param m: int: - Number of servings
        """
        self.servings = m
        self.mutex = Mutex()
        self.mutexC = Mutex()
        self.full_pot = Semaphore(0)
        self.empty_pot = Semaphore(0)

        self.bar_savage_1 = SimpleBarrier(N)
        self.bar_savage_2 = SimpleBarrier(N)

        self.bar_cook_1 = SimpleBarrier(C)
        self.bar_cook_2 = SimpleBarrier(C)

        self.cooks = 0


def eat(i):
    """
    Simulates the code execution. This execution should be concurrent
    :param i: int: Identification number of the Savage that called this function
    :return:
    """
    print(f"Savage {i}: is eating")
    sleep(randint(0, 100) / 100)


def savage(i, shared):
    """
    Savage representation, this function waits for all the concurrent savages to wait before they start 'eating',
    that means all savages must eaten before next iteration starts.
    :param i: int: - Identification number of savage
    :param shared: object: - Shared synchronization object
    :return:
    """
    sleep(randint(0, 100) / 100)
    while True:
        shared.bar_savage_1.wait()
        shared.bar_savage_2.wait(savage_id=i)
        shared.mutex.lock()
        if shared.servings == 0:
            print(f"Savage {i}: pot is empty !\n")
            shared.empty_pot.signal(C)
            shared.full_pot.wait()
        print(f"Savage {i}: taking from pot")
        shared.servings -= 1
        shared.mutex.unlock()
        eat(i)


def cook(i, shared):
    """
    Cook function that are cooking the meals for savages, all cooks must be awake before they start cooking
    they cook until the pot is full, then they go for sleep and wait for pot to be empty.
    :param i: int: - Identification number of the cook
    :param shared: - Shared synchronization object
    :return:
    """
    shared.empty_pot.wait()
    while True:
        shared.bar_cook_1.wait()
        shared.bar_cook_2.wait(cook_id=i)
        # shared.empty_pot.wait()
        shared.mutexC.lock()
        shared.cooks += 1
        if shared.servings == M:
            shared.cooks = 0
            print(f"Cook {i}: pot is full\n")
            shared.full_pot.signal()
            shared.empty_pot.wait()

        sleep(randint(50, 200) / 100)
        shared.servings += 1
        print(f"Cook {i}: cooking --> dish {shared.servings}")
        shared.mutexC.unlock()

        # shared.cooks += 1
        # print(f"Cook {i}: I am awake, now we are {shared.cooks}")
        # sleep(randint(50, 200) / 100)
        # if shared.cooks == C:
        #     print(f"Cooks: We are cooking")
        #     shared.servings += M
        #     print(f"Cook {i}: pot is full\n")
        #     shared.full_pot.signal()
        #     shared.cooks = 0


def main():
    # init
    shared = Shared(0)
    tribe = [Thread(savage, i, shared) for i in range(N)]
    tribe += [Thread(cook, i, shared) for i in range(C)]
    for t in tribe:
        t.join()


if __name__ == "__main__":
    main()
