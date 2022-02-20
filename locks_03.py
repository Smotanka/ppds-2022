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


class Shared:
    """ Object that is shared with multiple threads """

    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


def do_count(obj):
    while obj.counter < obj.end:
        obj.elms[obj.counter] += 1
        obj.counter += 1


def lock_thread(function, *args):
    mutex = Mutex()
    mutex.lock()
    thread = Thread(function, *args)
    mutex.unlock()
    return thread.join()


size = 1_000_000
shared = Shared(size)

lock_thread(do_count, shared)
lock_thread(do_count, shared)

counter = Counter(shared.elms)
print(counter.most_common())
