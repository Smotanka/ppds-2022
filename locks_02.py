"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/"""

# Python v3.10
# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Thread
from fei.ppds import Mutex

from collections import Counter
from time import sleep
from random import randint


class Shared:
    """ Object that is shared with multiple threads """

    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(obj):
    while True:
        mutex.lock()
        if obj.counter < obj.end:
            obj.elms[obj.counter] += 1

            """Putting to sleep one Thread,
            because we want interpreter to switch to another Thread
            Deeper explained at: https://www.youtube.com/watch?v=HNGZJ0MXSWI (01:00:00)"""

            sleep(randint(1, 10) / 1000)
            obj.counter += 1
            mutex.unlock()
        else:
            mutex.unlock()  # to prevent deadlock
            break


size = 1_000
shared = Shared(size)

mutex = Mutex()

t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)

t1.join()
t2.join()

counter = Counter(shared.elms)
print(counter.most_common())
