"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/"""

# Python v3.10
# Import threads and locks
# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Thread
from fei.ppds import Mutex
# Other Imports
from collections import Counter
from time import sleep
from random import randint


# 'Shared' class which will be called with multiple threads
class Shared:
    """Constructor with size argument that creates counter and elms array with size of argument size """

    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


# Mutex lock declaration
mutex = Mutex()


# Counter function that increments the element in 'elms' attribute on index with of obj.counter
def do_count(obj):
    # 1. case of using lock
    # mutex.lock()
    while obj.counter < obj.end:
        # 2. case of using lock
        mutex.lock()
        obj.elms[obj.counter] += 1
        # Putting to sleep one Thread,
        # because we want interpreter to switch to another Thread
        # Deeper explained at: https://www.youtube.com/watch?v=HNGZJ0MXSWI (01:00:00)
        sleep(randint(1, 10) / 1000)
        obj.counter += 1
        mutex.unlock()
    # mutex.unlock()


# Creating single instance of class 'Shared' with size of 'size'
size = 1000
shared = Shared(size)

# Assigning the 'Thread' index to t1 variable
# First argument is function which will be called on specific thread
# Other arguments are passed to function as first argument
t1 = Thread(do_count, shared)
t2 = Thread(do_count, shared)

t1.join()
t2.join()

# Counter elms in 'Shared' class
counter = Counter(shared.elms)
print(counter.most_common())
