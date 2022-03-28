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
            @param(n_threads): int - number of threads
            @attrib(threads): int - number of threads, with which this instance of barrier object will be working
            @attrib(counter): int - simple counter, that holds number of threads
            @attrib(mutex): Object - 'Mutex' lock object
            @attrib(event): Object - 'Event' object that locks multiple threads
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
    def __init__(self):
        self.mutex = Semaphore()
        self.oxyQueue = Semaphore(0, insert='fifo')
        self.hydroQueue = Semaphore(0, insert='fifo')
        self.hydrogen = 0
        self.oxygen = 0
        self.barrier = SimpleBarrier(3)


def oxygen(shared):
    shared.mutex.wait()
    shared.oxygen += 1
    if shared.hydrogen < 2:
        shared.mutex.signal()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)
        shared.hydroQueue.signal(2)

    shared.oxyQueue.wait()
    bond("O")
    shared.barrier.wait()
    shared.mutex.signal()


def hydrogen(shared):
    shared.mutex.wait()
    shared.hydrogen += 1

    if shared.hydrogen < 2 or shared.oxygen < 1:
        print("\n")
        shared.mutex.signal()
    else:
        shared.oxygen -= 1
        shared.hydrogen -= 2
        shared.oxyQueue.signal(1)
        shared.hydroQueue.signal(2)

    shared.hydroQueue.wait()
    bond("H")
    shared.barrier.wait()


def bond(text):
    print(text)


def init():
    shared = Shared()
    while True:
        sleep(.5)
        Thread(hydrogen, shared)
        Thread(oxygen, shared)


def main():
    init()


if __name__ == '__main__':
    main()
