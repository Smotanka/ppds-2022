"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F"""

# Python v3.10
from random import randint
from time import sleep
from fei.ppds import Thread
from fei.ppds import Mutex
from fei.ppds import Event
from fei.ppds import print


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
        self.event = Event()

    def wait(self):
        """

        Method that implements barrier synchronization, 'wait' method waits for execution on all threads,
        this method is created to work in loop, where last thread unlocks threads from previous iteration

        """
        self.event.clear()
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads:
            self.counter = 0
            self.event.signal()
        self.mutex.unlock()
        sleep(randint(1, 10) / 10)
        if self.counter < self.threads:
            self.event.wait()


def before_barrier(thread_id):
    """

    Function that prints all threads that are waiting on turn-stile to open.

        @param(thread_id): int - id that represent current working thread

    """

    sleep(randint(1, 10) / 10)  # Illustrates code execution
    print(f"before barrier {thread_id}")


def after_barrier(thread_id):
    """

    Function that prints all threads that are freed in turn-stile.

        @param(thread_id): int - id that represent current working thread

    """

    print(f"after barrier {thread_id}")
    sleep(randint(1, 10) / 10)  # Illustrates code execution


def barrier_cycle(barrier_1, barrier_2, thread_id):
    """

    Function recreating example how to use ATD barrier

        @param(barrier_1): Object - reference to an 'SimpleBarrier' object
        @param(barrier_2): Object - reference to an 'SimpleBarrier' object
        @param(thread_id): int - id that represent current working thread

    """
    while True:
        before_barrier(thread_id)
        barrier_1.wait()
        after_barrier(thread_id)
        barrier_2.wait()


THREADS = 5
sb_1 = SimpleBarrier(THREADS)
sb_2 = SimpleBarrier(THREADS)
# creates array of size 'THREADS' and on each thread is called 'barrier_cycle' function
threads = [Thread(barrier_cycle, sb_1, sb_2, i) for i in range(THREADS)]
[t.join() for t in threads]
