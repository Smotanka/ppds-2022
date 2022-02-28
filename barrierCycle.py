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
from fei.ppds import Event
from fei.ppds import print
from threading import get_ident


class SimpleBarrier:
    def __init__(self, n_threads):
        self.threads = n_threads
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Event()

    def wait(self):
        self.semaphore.clear()
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads:
            self.counter = 0
            self.semaphore.signal()
        self.mutex.unlock()
        sleep(randint(1, 10) / 10)
        if self.counter < self.threads:
            self.semaphore.wait()


def before_barrier(thread_id):
    sleep(randint(1, 10) / 10)
    print(f"pred barierou {thread_id}")


def after_barrier(thread_id):
    print(f"za barierou {thread_id}")
    sleep(randint(1, 10) / 10)


def barrier_cycle(barrier_1, barrier_2, thread_id):
    while True:
        before_barrier(thread_id)
        barrier_1.wait()
        after_barrier(thread_id)
        barrier_2.wait()


THREADS = 5
sb_1 = SimpleBarrier(THREADS)
sb_2 = SimpleBarrier(THREADS)
threads = [Thread(barrier_cycle, sb_1, sb_2, i) for i in range(THREADS)]
[t.join() for t in threads]
