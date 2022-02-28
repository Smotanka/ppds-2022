"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/2-cvicenie-turniket-bariera-%f0%9f%9a%a7/?%2F"""

from random import randint
from time import sleep
from fei.ppds import Thread
from fei.ppds import Semaphore
from fei.ppds import Mutex
from fei.ppds import print
from threading import get_ident


class SimpleBarrier:
    def __init__(self, n_threads):
        self.threads = n_threads
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Semaphore(0)

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads:
            self.counter = 0
            self.semaphore.signal(self.threads)
        self.mutex.unlock()
        self.semaphore.wait()


def barrier_example(barrier, thread_id):
    sleep(randint(1, 10) / 10)
    print("thread %d before barrier" % thread_id)
    barrier.wait()
    print("thread %d after barrier" % thread_id)


THREADS = 5
sb_1 = SimpleBarrier(THREADS)
threads = [Thread(barrier_example, sb_1, i) for i in range(THREADS)]
[t.join() for t in threads]
