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
    def __init__(self, n):
        self.semaphore = Event()
        self.n_place = n

    def thread_wait(self):
        self.semaphore.wait()

    def signal(self):
        self.semaphore.signal()

    def id(self):
        return self.n_place


class SharedCounter:
    def __init__(self, n_threads):
        self.counter = 0
        self.thread_array = [] * n_threads

    def add(self):
        self.counter += 1

    def print(self):
        print(self.thread_array)

    def sum(self):
        return self.counter

    def reset(self):
        self.counter = 0

    def append(self, barrier):
        if barrier not in self.thread_array:
            self.thread_array.append(barrier)

    def sort(self):
        return sorted(self.thread_array, key=lambda x: x.id())

    def free_all(self):
        mutex = Mutex()
        sorted_array = self.sort()
        for barrier in sorted_array:
            mutex.lock()
            barrier.signal()
            mutex.unlock()
        self.reset()


def compute_fibonacci(i, counter, mutex):
    bar = SimpleBarrier(i)
    sleep(randint(1, 10) / 10)
    mutex.lock()
    counter.add()
    counter.append(bar)
    mutex.unlock()
    if counter.sum() < THREADS:
        bar.thread_wait()
    else:
        counter.free_all()
    fib_seq[i + 2] = fib_seq[i] + fib_seq[i + 1]


THREADS = 10
fib_seq = [0] * (THREADS + 2)
fib_seq[1] = 1
counter = SharedCounter(THREADS)
count = []
mtx = Mutex()
threads = [Thread(compute_fibonacci, i, counter, mtx) for i in range(THREADS)]

[t.join() for t in threads]

print(fib_seq)
