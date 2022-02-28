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


# TODO
class SimpleBarrier:
    def __init__(self, n_threads):
        self.threads = n_threads
        self.counter = 0
        self.mutex = Mutex()
        self.semaphore = Event()

    def wait(self):
        self.mutex.lock()
        self.counter += 1
        if self.counter == self.threads:
            self.counter = 0
            self.semaphore.signal()
        self.mutex.unlock()
        self.semaphore.clear()
        self.semaphore.wait()
        self.semaphore.signal()


def compute_fibonacci(i, barrier, barrier_2, mutex):
    sleep(randint(1, 10) / 10)
    barrier.wait()
    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]
    barrier_2.wait()


THREADS = 10
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1

bar = SimpleBarrier(THREADS)
bar_2 = SimpleBarrier(THREADS)
mtx = Mutex()
threads = [Thread(compute_fibonacci, i, bar, bar_2, mtx) for i in range(THREADS)]
[t.join() for t in threads]

print(fib_seq)
