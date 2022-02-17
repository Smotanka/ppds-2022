"""Authors: Mgr. Ing. Matúš Jókay, PhD.
            Bc. Martin Smetanka
University:  Slovak Technical University in Bratislava
Faculty: Faculty of Electrical Engineering and Information Technology
Semester: Spring/Summer
Year: 2022
License: MIT
Assignment: https://uim.fei.stuba.sk/i-ppds/1-cvicenie-oboznamenie-sa-s-prostredim-%f0%9f%90%8d/"""

# Import threads
# Source: https://pypi.org/project/fei.ppds/
from fei.ppds import Thread


# 'Shared' class which will be called with multiple threads
class Shared:
    """Constructor with size argument that creates counter and elms array with size of argument size """
    def __init__(self, size):
        self.counter = 0
        self.end = size
        self.elms = [0] * size


# Counter function that increments the element in elms attribute on index with of obj.counter
def do_count(obj):
    while obj.counter != obj.end:
        obj.elms[obj.counter] += 1
        obj.counter += 1


# Creating single instance of class 'Shared' with size of 100_000
shared = Shared(100_000)

# Assigning the 'Thread' index to t1 variable
# First argument is function which will be called on specific thread
# Other arguments are passed to function as first argument
t1 = Thread(do_count, shared)
t1.join()
