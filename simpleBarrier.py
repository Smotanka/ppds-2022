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
from fei.ppds import Semaphore
from fei.ppds import Mutex
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
            @attrib(semaphore): Object - 'Semaphore' object that implements 'random', 'lifo', 'fifo queue

        """

        self.threads = n_threads
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)

    def wait(self):
        """

        Method that implements barrier synchronization, 'wait' method waits for execution on all threads,
        then method reset counter and free all threads.

        """

        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads:
            self.counter = 0
            self.semaphore.signal(self.threads)
        self.mutex.unlock()
        self.semaphore.wait()


def barrier_example(barrier, thread_id):
    """

    Function recreating example how to use barrier

        @param(barrier): Object - reference to an 'SimpleBarrier' object
        @param(thread_id): int - id that represent current working thread

    """

    sleep(randint(1, 10) / 10)
    print("thread %d before barrier" % thread_id)
    barrier.wait()
    print("thread %d after barrier" % thread_id)


THREADS = 5
sb_1 = SimpleBarrier(THREADS)
# creates array of size 'THREADS' and on each thread is called 'barrier_example' function
threads = [Thread(barrier_example, sb_1, i) for i in range(THREADS)]
[t.join() for t in threads]
