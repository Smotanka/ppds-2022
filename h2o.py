"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/6-cvicenie-menej-klasicke-synchronizacne-problemy/"""

# Python v3.10
# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Semaphore
from fei.ppds import Mutex
from fei.ppds import Thread
from fei.ppds import print

from time import sleep


class SimpleBarrier:
    """
    Object that represents barrier synchronization method.
    """

    def __init__(self, n_threads):
        """"
        Creates instance of barrier.
            :param n_threads: int - number of threads
            :attrib threads: int - number of threads, with which this instance of barrier object will be working
            :attrib counter: int - simple counter, that holds number of threads
            :attrib mutex: Object - 'Mutex' lock object
            :attrib event: Object - 'Event' object that locks multiple threads
        """
        self.threads = n_threads
        self.counter = 0
        self.mutex = Mutex()
        self.event = Semaphore(0)

    def wait(self):
        """
        Method that implements barrier synchronization, 'wait' method waits for execution on all threads,
        this method is created to work in loop, where last thread unlocks threads from previous iteration
        """
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads:
            self.counter = 0
            self.event.signal(self.threads)
        self.mutex.unlock()


class Shared(object):
    """
    Shared object for synchronization, unique queues for hydrogen and oxygen
    """

    def __init__(self):
        """
        Create instance of Shared object with fifo 'Semaphore' objects for hydrogen and oxygen and 'SimpleBarrier'
        object for higher level of synchronization .
        """
        self.mutex = Semaphore()
        self.oxyQueue = Semaphore(0, insert='fifo')
        self.hydroQueue = Semaphore(0, insert='fifo')
        self.hydrogen = 0
        self.oxygen = 0
        self.barrier = SimpleBarrier(3)


def oxygen(shared):
    """
    Function representing oxygen
    :param shared: Object - 'Shared' object for synchronization
    :return:
    """
    shared.mutex.wait()  # to ensure data integrity
    shared.oxygen += 1
    # previous line ensure us that we have
    # one molecule of water, we just need two of H
    if shared.hydrogen < 2:
        shared.mutex.signal()
    else:  # We can create molecule
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)  # pop first molecule in semaphore
        shared.hydroQueue.signal(2)  # pop first two molecules in semaphore

    shared.oxyQueue.wait()  # we wait for 2 H and 1 O
    bond("O")  # create molecule
    shared.barrier.wait()
    shared.mutex.signal()


def hydrogen(shared):
    """
    Function representing hydrogen
    :param shared: Object - 'Shared' object for synchronization
    :return:
    """
    shared.mutex.wait()  # to ensure data integrity
    shared.hydrogen += 1

    if shared.hydrogen < 2 or shared.oxygen < 1:  # We need 2 molecules of H and one of O
        print("\n")
        shared.mutex.signal()
    else:  # We can create molecule
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)  # pop first molecule in semaphore
        shared.hydroQueue.signal(2)  # pop first two molecules in semaphore

    shared.hydroQueue.wait()
    bond("H")  # create molecule
    shared.barrier.wait()


def bond(text):
    """
    Creates water molecule
    :param text: string - string that represent which molucele is bonding
    :return:
    """
    print(text)


def init():
    # init
    shared = Shared()
    while True:
        sleep(.5)
        # Create molecules
        Thread(hydrogen, shared)
        Thread(oxygen, shared)


if __name__ == '__main__':
    init()
